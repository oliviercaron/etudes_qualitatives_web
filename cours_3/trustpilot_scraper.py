# trustpilot_scraper.py
import re
import time
import json
import math
import random
import argparse
from urllib.parse import urlparse, urlunparse, parse_qs, urlencode
from typing import Any, List, Dict, Optional

import pandas as pd
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

# Exemple de commande pour démarrer le script depuis Console/Terminal
# python trustpilot_scraper.py --url "https://fr.trustpilot.com/review/www.carrefour.fr?languages=fr" --start-page 1 --end-page 0 --max-pages 0 --out carrefour_fr_only.csv --format csv --delay 1.8

# ---------- Sélecteurs (tolérants) ----------
SELECTORS = {
    "review_card": "article[data-review-id], section[data-service-review-card]",
    "review_id_attr": "data-review-id",

    # Note affichée généralement via <img aria-label="Noté 4 sur 5"> (FR) / "Rated 4 out of 5" (EN)
    "rating_role": (
        "img[aria-label*='Noté'], img[aria-label*='Rated'], "
        "img[alt*='Noté'], img[alt*='Rated']"
    ),

    # Titre & corps
    "title": "h2, h3, a[data-review-title-typography]",
    "body": "[data-service-review-text-typography], section:has([data-service-review-text-typography]) p, p",

    # Dates
    "time_published": "time[datetime]",
    "date_of_experience_label": (
        "p:has-text('Date d’expérience'), p:has-text('Date of experience'), "
        "span:has-text('Date d’expérience'), span:has-text('Date of experience')"
    ),
    "date_of_experience_time": "time",

    # Auteur
    "author_name": "[data-consumer-name], a[href*='/users/']",
    "author_location": "div:has-text('Location') + div, span:has-text('·')",

    # Badges/réponses
    "verified_badge": "svg[aria-label*='Vérifié'], svg[aria-label*='Verified']",
    "company_reply": (
        "section:has(h3:has-text('Réponse')), "
        "section:has-text('Company reply'), "
        "section:has-text('Réponse de l’entreprise')"
    ),

    # Interactions
    "helpful": "button:has-text('Utile'), button:has-text('Helpful')",

    # Pagination
    "next_page_btn": "nav[aria-label='Pagination'] a[aria-label='Next page']:not([aria-disabled='true'])",

    # Cookies (plusieurs CMP possibles)
    "cookie_accept": (
        "[data-testid='uc-accept-all-button'], "
        "button:has-text('Tout accepter'), button:has-text('Accepter tout'), "
        "button:has-text('Accept all'), button:has-text('I agree'), "
        "#onetrust-accept-btn-handler, "
        "button[aria-label*='accept']"
    ),
}

# ---------- Helpers ----------
def normalize_url_add_languages_all(url: str) -> str:
    """Ajoute languages=all si absent, pour ne pas perdre d'avis par défaut."""
    parsed = urlparse(url)
    q = parse_qs(parsed.query)
    if "languages" not in q:
        q["languages"] = ["all"]
    new_query = urlencode(
        {k: v[0] if isinstance(v, list) and len(v) == 1 else v for k, v in q.items()},
        doseq=True
    )
    return urlunparse(parsed._replace(query=new_query))

def safe_text(el) -> str:
    try:
        return (el.inner_text() or "").strip()
    except Exception:
        return ""

def safe_attr(el, attr: str) -> Optional[str]:
    try:
        return el.get_attribute(attr)
    except Exception:
        return None

def click_if_visible(page, selector: str, timeout: int = 3000) -> bool:
    try:
        page.locator(selector).first.click(timeout=timeout)
        return True
    except Exception:
        return False

def get_helpful_count(btn_text: str) -> Optional[int]:
    if not btn_text:
        return None
    m = re.search(r"\((\d+)\)", btn_text)
    return int(m.group(1)) if m else None

def parse_rating_from_aria_or_alt(el) -> Optional[float]:
    if not el:
        return None
    aria = safe_attr(el, "aria-label") or ""
    alt = safe_attr(el, "alt") or ""
    txt = aria or alt
    if not txt:
        return None
    m = re.search(r"(\d+(?:[.,]\d+)?)", txt)
    return float(m.group(1).replace(",", ".")) if m else None

# ---------- JSON-LD ----------
def parse_reviews_from_jsonld(page) -> List[Dict]:
    """
    Extrait les objets Review depuis les <script type="application/ld+json">.
    """
    reviews_raw: List[Dict] = []
    scripts = page.query_selector_all("script[type='application/ld+json']")
    for s in scripts:
        raw = (s.inner_text() or "").strip()
        if not raw:
            continue

        blocks: List[Any] = []
        try:
            blocks = [json.loads(raw)]
        except Exception:
            try:
                raw_fixed = "[" + raw.replace("}{", "},{") + "]"
                blocks = json.loads(raw_fixed)
            except Exception:
                continue

        if isinstance(blocks, dict):
            blocks = [blocks]
        if not isinstance(blocks, list):
            continue

        def walk(obj: Any):
            if isinstance(obj, dict):
                if obj.get("@type") == "Review":
                    reviews_raw.append(obj)
                if isinstance(obj.get("@graph"), list):
                    for it in obj["@graph"]:
                        walk(it)
                for v in obj.values():
                    walk(v)
            elif isinstance(obj, list):
                for it in obj:
                    walk(it)

        for b in blocks:
            walk(b)

    mapped: List[Dict] = []
    for r in reviews_raw:
        author = r.get("author") or {}
        rr = r.get("reviewRating") or {}

        mapped.append({
            "review_id": (r.get("@id") or "").rpartition("/")[-1] or None,
            "title": r.get("headline") or None,
            "body": r.get("reviewBody") or None,
            "rating": float(str(rr.get("ratingValue")).replace(",", ".")) if rr.get("ratingValue") is not None else None,
            "date_published": r.get("datePublished") or None,
            "date_of_experience": None,  # rarement dans JSON-LD
            "author_name": (author.get("name") if isinstance(author, dict) else None),
            "author_location": None,
            "verified_order": None,
            "company_reply_present": None,
            "helpful_count": None,
            "review_url": r.get("@id") if isinstance(r.get("@id"), str) and r.get("@id").startswith("http") else None,
            "in_language": r.get("inLanguage"),
            "page_url": page.url,
        })
    return mapped

# ---------- Scraping d'une page ----------
def scrape_page(page, url: str, debug_html: bool = False, page_index: int = 1) -> List[Dict]:
    page.goto(url, wait_until="domcontentloaded", timeout=90000)

    # Cookies
    click_if_visible(page, SELECTORS["cookie_accept"], timeout=6000)

    # 1) JSON-LD d'abord (rapide et fiable)
    jsonld_reviews = parse_reviews_from_jsonld(page)
    if jsonld_reviews:
        return jsonld_reviews

    # 2) Fallback DOM
    try:
        page.wait_for_selector(SELECTORS["review_card"], timeout=30000)
    except Exception:
        if debug_html and page_index == 1:
            with open("debug_trustpilot.html", "w", encoding="utf-8") as f:
                f.write(page.content())
            print("[DEBUG] Aucune carte détectée. HTML sauvegardé dans debug_trustpilot.html")
        return []

    reviews: List[Dict] = []
    for card in page.query_selector_all(SELECTORS["review_card"]):
        rid = safe_attr(card, SELECTORS["review_id_attr"])

        rating_el = card.query_selector(SELECTORS["rating_role"])
        rating = parse_rating_from_aria_or_alt(rating_el)

        title_el = card.query_selector(SELECTORS["title"])
        title = safe_text(title_el)

        body_el = card.query_selector(SELECTORS["body"])
        body = safe_text(body_el)

        time_el = card.query_selector(SELECTORS["time_published"])
        date_published = safe_attr(time_el, "datetime") if time_el else None

        doe_label = card.locator(SELECTORS["date_of_experience_label"])
        if doe_label.count() > 0:
            doe_time = doe_label.nth(0).locator(SELECTORS["date_of_experience_time"])
            date_of_experience = (
                doe_time.first.get_attribute("datetime") if doe_time.count() > 0
                else safe_text(doe_label.nth(0))
            )
        else:
            date_of_experience = None

        author_el = card.query_selector(SELECTORS["author_name"])
        author_name = safe_text(author_el)

        author_loc_el = card.query_selector(SELECTORS["author_location"])
        author_location = safe_text(author_loc_el)

        verified = card.query_selector(SELECTORS["verified_badge"]) is not None
        replied = card.query_selector(SELECTORS["company_reply"]) is not None

        helpful_el = card.query_selector(SELECTORS["helpful"])
        helpful_count = get_helpful_count(safe_text(helpful_el)) if helpful_el else None

        # Lien vers l'avis, si dispo
        review_url = None
        link = card.query_selector("a[href*='#review']") or card.query_selector("a[href*='/reviews/']")
        if link:
            href = safe_attr(link, "href")
            if href and href.startswith("http"):
                review_url = href

        reviews.append({
            "review_id": rid,
            "title": title or None,
            "body": body or None,
            "rating": rating,
            "date_published": date_published,
            "date_of_experience": date_of_experience,
            "author_name": author_name or None,
            "author_location": author_location or None,
            "verified_order": verified,
            "company_reply_present": replied,
            "helpful_count": helpful_count,
            "review_url": review_url,
            "in_language": None,   # non dispo côté DOM
            "page_url": url,
        })
    return reviews

# ---------- Pagination robuste ----------
def paginate_and_scrape(
    start_url: str,
    max_pages: int = 0,
    headless: bool = True,
    delay_s: float = 1.0,
    start_page: int = 1,
    end_page: int = 0,
    debug_html: bool = False,
) -> List[Dict]:
    """
    max_pages=0 : pas de limite interne.
    end_page=0   : jusqu'à la dernière page disponible.
    """
    data: List[Dict] = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)
        context = browser.new_context(
            locale="en-US",
            user_agent=("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                        "AppleWebKit/537.36 (KHTML, like Gecko) "
                        "Chrome/126.0.0.0 Safari/537.36"),
        )
        page = context.new_page()

        # Prépare l'URL
        url = normalize_url_add_languages_all(start_url)
        if re.search(r"[?&]page=\d+", url):
            url = re.sub(r"([?&]page=)\d+", rf"\g<1>{start_page}", url)
        else:
            sep = "&" if ("?" in url) else "?"
            url = f"{url}{sep}page={start_page}"

        page_num = start_page
        pages_done = 0

        while True:
            # Forcer la numérotation si ?page= présent dans l'URL
            if re.search(r"[?&]page=\d+", url):
                url = re.sub(r"([?&]page=)\d+", rf"\g<1>{page_num}", url)

            try:
                page_reviews = scrape_page(page, url, debug_html=debug_html, page_index=page_num - start_page + 1)
            except PlaywrightTimeoutError:
                break

            if not page_reviews:
                # plus rien trouvé => stop
                break

            data.extend(page_reviews)
            pages_done += 1

            # Limite max_pages (sécurité)
            if max_pages and pages_done >= max_pages:
                break

            # Borne end_page si définie
            if end_page and page_num >= end_page:
                break

            # --------- STRATÉGIE DE PASSAGE À LA PAGE SUIVANTE ---------

            # 1) Essayer un href via rel="next" / a[rel=next] / bouton pagination
            next_href = page.evaluate("""
            () => {
              const l1 = document.querySelector('link[rel="next"]');
              if (l1 && l1.href) return l1.href;
              const a1 = document.querySelector('a[rel="next"]');
              if (a1 && a1.href) return a1.href;
              const a2 = document.querySelector("nav[aria-label='Pagination'] a[aria-label='Next page']:not([aria-disabled='true'])");
              return (a2 && a2.href) ? a2.href : null;
            }
            """)
            if next_href:
                page.goto(next_href, wait_until="domcontentloaded", timeout=60000)
                page_num += 1
                url = page.url
                time.sleep(delay_s + random.uniform(0, 0.9))
                continue

            # 2) Fallback: incrémenter ?page=N manuellement
            m = re.search(r'([?&])page=(\d+)', url)
            if m:
                cur = int(m.group(2))
                trial_url = re.sub(r'([?&]page=)\d+', rf'\g<1>{cur+1}', url)
            else:
                sep = '&' if ('?' in url) else '?'
                trial_url = f"{url}{sep}page={page_num+1}"

            prev_title = page.title()
            prev_path_q = urlparse(url).path + "?" + (urlparse(url).query or "")

            page.goto(trial_url, wait_until="domcontentloaded", timeout=60000)
            curr_title = page.title()
            curr_path_q = urlparse(page.url).path + "?" + (urlparse(page.url).query or "")

            # Si la page n'a pas réellement avancé, stop.
            if curr_title == prev_title and curr_path_q == prev_path_q:
                break

            page_num += 1
            url = page.url
            time.sleep(delay_s + random.uniform(0, 0.9))

        browser.close()

    return data

# ---------- CLI ----------
def main():
    parser = argparse.ArgumentParser(description="Scraper Trustpilot (Playwright).")
    parser.add_argument("--url", required=True, help="URL Trustpilot de la page marque/distributeur.")
    parser.add_argument("--max-pages", type=int, default=0, help="Nombre max de pages (0 = illimité).")
    parser.add_argument("--out", default="trustpilot_reviews.csv", help="Fichier de sortie.")
    parser.add_argument("--format", choices=["csv", "jsonl"], default="csv", help="Format de sortie.")
    parser.add_argument("--headless", action="store_true", help="Lancer en headless.")
    parser.add_argument("--delay", type=float, default=1.0, help="Délai (s) entre pages.")
    parser.add_argument("--start-page", type=int, default=1, help="Page de départ (par défaut 1).")
    parser.add_argument("--end-page", type=int, default=0, help="Dernière page à scraper (0 = jusqu’à la fin).")
    parser.add_argument("--debug-html", action="store_true", help="Sauver la 1ère page en HTML si 0 avis détecté.")

    args = parser.parse_args()

    rows = paginate_and_scrape(
        args.url,
        max_pages=args.max_pages,
        headless=args.headless,
        delay_s=args.delay,
        start_page=args.start_page,
        end_page=args.end_page,
        debug_html=args.debug_html,
    )

    if not rows:
        print("Aucun avis trouvé. Vérifiez l’URL, la langue (paramètre ?languages=...) ou les sélecteurs.")
        return

    df = pd.DataFrame(rows).drop_duplicates(subset=["review_id"], keep="first")

    if args.format == "csv":
        df.to_csv(args.out, index=False)
    else:
        with open(args.out, "w", encoding="utf-8") as f:
            for r in rows:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")

    print(f"OK ✅  {len(df)} avis sauvegardés dans: {args.out}")

if __name__ == "__main__":
    main()

# Études qualitatives sur le web (Netnographie)

Ce dépôt contient les supports de cours (slides **Quarto / reveal.js**) et les scripts associés au module **Études qualitatives sur le web (IAE Créteil – M2 Marketing Digital)**.

---

## 📅 Séances & supports

| Séance | Thème | Slides | Scripts et références|
|--------|-------|--------|------------------|
| **Séance 1** | Introduction & **Netnographie** | [📑 cours_1.html](https://oliviercaron.github.io/etudes_qualitatives_web/cours_1/cours_1.html) | **Éthique & cadre** : [AoIR – Ethics 3.0 (PDF)](https://aoir.org/reports/ethics3.pdf) · [Robots.txt – standard](https://www.robotstxt.org/robotstxt.html) |
| **Séance 2** | Introduction à **R / Python / Quarto** & traitement des données | [📑 cours_1.html](https://oliviercaron.github.io/etudes_qualitatives_web/cours_1/cours_1.html) | **R** : [R for Data Science (2e)](https://r4ds.hadley.nz/) · [Tidyverse – Manipulation de données](https://juba.github.io/tidyverse/06-tidyverse.html) · [Grammaire des graphiques & ggplot](https://benaventc.github.io/DataScienceBook/introduction-%C3%A0-la-grammaire-des-graphiques-et-%C3%A0-ggplot.html#introduction-%C3%A0-la-grammaire-des-graphiques-et-%C3%A0-ggplot) · [Bonnes pratiques R et Git](https://inseefrlab.github.io/formation-bonnes-pratiques-git-R/slides/light.html#/title-slide) <br> **Python** : [Tutoriel Python officiel](https://docs.python.org/3/tutorial/) · [pandas – docs](https://pandas.pydata.org/docs/) · [PEP8 – style](https://peps.python.org/pep-0008/) <br> **Quarto** : [Docs](https://quarto.org/docs/) |
| **Séance 3** | **Scraping** des données en ligne (statique & dynamique) | [📑 cours_3.html](https://oliviercaron.github.io/etudes_qualitatives_web/cours_3/cours_3.html) | **Exemples (repo)** : [trustpilot_scraper.py]((https://github.com/oliviercaron/etudes_qualitatives_web/blob/main/cours_3/trustpilot_scraper.py) · [test_scrap_api_decathlon.ipynb](https://github.com/oliviercaron/etudes_qualitatives_web/blob/main/cours_3/test_scrap_api_decathlon.ipynb) · [test_scrap_marketing_jobs.R](https://github.com/oliviercaron/etudes_qualitatives_web/blob/main/cours_3/test_scrap_marketing_jobs.R) <br> **R** : [rvest](https://rvest.tidyverse.org/) · [httr2](https://httr2.r-lib.org/) · [polite (rOpenSci)](https://github.com/dmi3kno/polite) · [RSelenium](https://github.com/ropensci/RSelenium) <br> **Python** : [requests](https://requests.readthedocs.io/) · [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) · [Selenium](https://www.selenium.dev/documentation/webdriver/) · [Playwright](https://playwright.dev/python/) · [Scrapy – tuto](https://docs.scrapy.org/en/latest/intro/tutorial.html) |
| **Séance 4** | **Analyse exploratoire** & statistiques lexicales | [📑 cours_4.html](https://oliviercaron.github.io/etudes_qualitatives_web/cours_4/cours_4.html) | **Intro** : [Première analyse quantitative](https://benaventc.github.io/NLPBook/une-premi%C3%A8re-analyse-quantitative.html) · [Annotation syntaxique](https://oliviercaron.github.io/systematic_lit_review/nlp_techniques.html) <br> **Quanteda (R)** : [Quickstart](https://quanteda.io/articles/quickstart.html) · [Tutoriel Monroe](https://burtmonroe.github.io/TextAsDataCourse/Tutorials/TADA-IntroToQuanteda.nb.html) · [Bookdown Lukito](https://bookdown.org/josephine_lukito/j381m_tutorials/id_25-quanteda.html#id_25-quanteda) <br> **Autres (R)** : [tidytext – le livre](https://www.tidytextmining.com/) · [Text mining & nuages de mots (FR)](https://www.sthda.com/french/wiki/text-mining-et-nuage-de-mots-avec-le-logiciel-r-5-etapes-simples-a-savoir) <br> **Python** : [spaCy – usage](https://spacy.io/usage) · [textacy](https://textacy.readthedocs.io/) |
| **Séance 5** | **Analyse de sentiment** : des dictionnaires au Machine Learning | [📑 cours_5.html](https://oliviercaron.github.io/etudes_qualitatives_web/cours_5/cours_5.html) | **R** : [Analyse de sentiment – NLPBook](https://benaventc.github.io/NLPBook/analyse-du-sentiment.html) · [tidymodels – classification](https://www.tidymodels.org/learn/) <br> **Lexiques** : [NRC Emotion Lexicon](https://saifmohammad.com/WebPages/NRC-Emotion-Lexicon.htm) · [VADER (EN)](https://github.com/cjhutto/vaderSentiment) <br> **Python** : [scikit-learn – texte](https://scikit-learn.org/stable/tutorial/text_analytics/working_with_text_data.html) |
| **Séance 6** | **Topic modeling et représentations vectorielles** (LDA, STM, embeddings) | [📑 cours_6.html](https://oliviercaron.github.io/etudes_qualitatives_web/cours_6/cours_6.html) | **R** : [LDA – Passages CNRS](https://ouvrir.passages.cnrs.fr/wp-content/uploads/2019/07/rapp_topicmodel.html) · [LDA / STM – NLPBook](https://benaventc.github.io/NLPBook/topic.html#lda-une-application-aux-commentaires-trip-advisor) · [STM (exemple)](https://oliviercaron.github.io/systematic_lit_review/SLR_stm.html#structural-topic-model-stm) · Packages : [topicmodels](https://cran.r-project.org/package=topicmodels) · [stm](https://cran.r-project.org/package=stm) · [LDAvis](https://CRAN.R-project.org/package=LDAvis) <br> **Python** : [Gensim – LDA](https://radimrehurek.com/gensim/) · [scikit-learn – Topics (LSA/NMF)](https://scikit-learn.org/stable/modules/decomposition.html#lsi-and-nmf) · [BERTopic (documentation)](https://maartengr.github.io/BERTopic/) · [BERTopic (exemple)](https://oliviercaron.github.io/systematic_lit_review/topic_modeling.html#detect-interpretable-topics-with-bertopic) · [sentence-transformers](https://www.sbert.net/) · [pyLDAvis](https://pyldavis.readthedocs.io/en/latest/) |
| **Séance 7** | **Transformers & LLMs** | [📑 cours_7.html](https://oliviercaron.github.io/etudes_qualitatives_web/cours_7/cours_7.html) | **Hugging Face** : [Course](https://huggingface.co/learn/nlp-course) · [Transformers – docs](https://huggingface.co/docs/transformers/index) · [Datasets – docs](https://huggingface.co/docs/datasets/) <br> **FR** : [spaCy – modèles FR](https://spacy.io/models/fr) · [CamemBERT (présentation)](https://camembert-model.fr/publication/camembert/) |

---

## 💡 Ressources pour apprendre à coder (R & Python)

- **R** : [R for Data Science](https://r4ds.hadley.nz/) · [Style guide tidyverse](https://style.tidyverse.org/) · [Cheat sheets Posit](https://posit.co/resources/cheatsheets/)
- **Python** : [Tutoriel officiel](https://docs.python.org/3/tutorial/) · [pandas – documentation](https://pandas.pydata.org/docs/) · [PEP8](https://peps.python.org/pep-0008/)
- **Scraping** : [rvest](https://rvest.tidyverse.org/) · [requests](https://requests.readthedocs.io/) · [Selenium](https://www.selenium.dev/documentation/webdriver/) · [Playwright](https://playwright.dev/python/) · [Scrapy](https://docs.scrapy.org/)
- **NLP (R)** : [quanteda – Quickstart](https://quanteda.io/articles/quickstart.html) · [Tutoriel quanteda (Monroe)](https://burtmonroe.github.io/TextAsDataCourse/Tutorials/TADA-IntroToQuanteda.nb.html) · [Quanteda – bookdown (Lukito)](https://bookdown.org/josephine_lukito/j381m_tutorials/id_25-quanteda.html#id_25-quanteda) · [tidytext – le livre](https://www.tidytextmining.com/) · [Text mining & nuage de mots (FR)](https://www.sthda.com/french/wiki/text-mining-et-nuage-de-mots-avec-le-logiciel-r-5-etapes-simples-a-savoir)
- **NLP (Python)** : [spaCy – usage](https://spacy.io/usage) · [NLTK](https://www.nltk.org/)

---

## 📊 Visualisation de données

- [Fundamentals of Data Visualization – Claus O. Wilke](https://clauswilke.com/dataviz/)
- [Modern Data Visualization with R – Robert Kabacoff](https://rkabacoff.github.io/datavis/)
- [Data Visualization: A practical introduction – Kieran Healy](https://socviz.co/index.html#preface)
- **Cheatsheets utiles** : [Posit – Cheat Sheets](https://rstudio.github.io/cheatsheets/)

---

## 🧰 Organisation du dépôt

Le dépôt est organisé par séance. Chaque dossier `cours_n` contient ses propres données dans un sous-dossier `data/` ainsi que les slides, scripts et ressources liés à la séance.

## 🚀 Utilisation

- Les **slides** sont accessibles directement via GitHub Pages (liens ci-dessus).  
- Les **scripts** peuvent être ouverts et exécutés dans **R** ou **Python** selon leur extension (`.R`, `.qmd`, `.ipynb`, `.py`).  
- Tous les documents sont générés avec **[Quarto](https://quarto.org/)**.  

---

## 📖 Licence

Ces supports sont mis à disposition pour un usage pédagogique dans le cadre du **M2 Marketing Digital**.  
Toute réutilisation ou diffusion en dehors de ce contexte doit citer l’auteur : **Olivier Caron**.

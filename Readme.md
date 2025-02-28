# Analyse Sentimentale des Critiques de Films

## Description

Ce projet NLP analyse les critiques de spectateurs pour les 50 meilleurs films d'Allociné, détermine leur sentiment et génère des résumés automatiques des opinions pour chaque film.

## Fonctionnalités
 
. Scraping de critiques depuis Allociné  
. Prétraitement des textes en français  
. Analyse de sentiment avec BERT/CamemBERT  
. Génération de résumés avec BART  
. Extraction de mots-clés par TF-IDF  
. Interface Streamlit pour visualiser les résultats  
 
## Technologies

- Python, NLTK, Transformers  
- Pandas, Scikit-learn
- BeautifulSoup (scraping)
- Streamlit (interface)

## Structure
├── Allocine_movie_reviews.ipynb  &nbsp;&nbsp;&nbsp;     # Notebook du Scraping des critiques  
├── Sentimental_analysis.ipynb   &nbsp;&nbsp;&nbsp;   # Notebook principal  
├── interface.py                    &nbsp;&nbsp;&nbsp;      # Interface Streamlit  
├── requirements.txt      &nbsp;&nbsp;&nbsp;          # Dépendances  
└── README.md            &nbsp;&nbsp;&nbsp;          # Documentation   

## Installation
```bash
pip install -r requirements.txt
streamlit run app.py #faut tourner les notebooks avant.
```

## Auteurs
- Yassine Ben Abdallah
- Jihed Bhar

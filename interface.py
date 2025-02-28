import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import unicodedata

# Configuration de la page
st.set_page_config(
    page_title="Analyse Sentimentale des Critiques de Films",
    page_icon="🎬",
    layout="wide"
)

# Titre et description
st.title("📽️ Analyse Sentimentale des Critiques de Films")
st.markdown("Cette application présente les résultats d'une analyse de sentiment sur des critiques de films d'Allociné.")


def fix_encoding(text):
    # Fonction pour corriger les caractères mal encodés
    if isinstance(text, str):
        # Corrections spécifiques courantes
        replacements = {
            "Ã©": "é", "Ã¨": "è", "Ã¢": "â", "Ã®": "î", 
            "Ã´": "ô", "Ã»": "û", "Ã«": "ë", "Ã¯": "ï",
            "Ã§": "ç", "Ã": "à", "Ã": "À"
        }
        
        for wrong, right in replacements.items():
            text = text.replace(wrong, right)
            
        # Normalisation générale
        text = unicodedata.normalize('NFC', text)
        
        # Corrections manuelles spécifiques
        if "EvadÃ©s" in text:
            text = text.replace("EvadÃ©s", "Évadés")
        if "communautÃ©" in text:
            text = text.replace("communautÃ©", "communauté")
            
    return text






# Fonction pour charger les données
@st.cache_data
def load_data():
    # Chargez votre DataFrame avec les sentiments
    # Remplacez ce chemin par celui de votre fichier
    if os.path.exists('critiques_films_sentiments.csv'):
        return pd.read_csv('critiques_films_sentiments.csv')
    else:
        # Créer un exemple de DataFrame si le fichier n'existe pas
        st.warning("Fichier de données non trouvé. Chargement de données d'exemple.")
        import numpy as np
        films = ["Forrest Gump", "Le Parrain", "Pulp Fiction", "La Liste de Schindler", 
                "Le Seigneur des Anneaux", "Star Wars", "Psychose", "Parasite", "Inception", "Your Name"]
        sentiments = np.random.uniform(0.5, 0.53, size=150)
        critiques = ["Exemple de critique " + str(i) for i in range(150)]
        film_titles = [films[i//15] for i in range(150)]  # 15 critiques par film
        df = pd.DataFrame({
            'film_title': film_titles,
            'critique': critiques,
            'sentiment': sentiments
        })
    df['film_title'] = df['film_title'].apply(fix_encoding)
    return df

# Charger les données
df = load_data()

# Sidebar
st.sidebar.title("Options")
view_mode = st.sidebar.radio("Mode d'affichage", ["Par film", "Par critique"])

# Calculer les statistiques par film
film_stats = df.groupby('film_title')['sentiment'].agg(['mean', 'std', 'min', 'max', 'count']).reset_index()
film_stats = film_stats.rename(columns={
    'mean': 'sentiment_moyen', 
    'std': 'écart_type',
    'min': 'minimum',
    'max': 'maximum',
    'count': 'nombre_critiques'
})

# Mode d'affichage par film
if view_mode == "Par film":
    st.header("Analyse Sentimentale par Film")
    
    # Graphique des sentiments moyens
    st.subheader("Score de sentiment moyen par film")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # Trier les films par sentiment moyen
        sorted_films = film_stats.sort_values(by='sentiment_moyen', ascending=False)
        
        fig, ax = plt.subplots(figsize=(10, 8))
        sns.barplot(x='sentiment_moyen', y='film_title', data=sorted_films, ax=ax)
        ax.set_title("Films classés par score de sentiment moyen")
        ax.set_xlabel("Score de sentiment moyen")
        ax.set_ylabel("Film")
        st.pyplot(fig)
    
    with col2:
        st.metric("Nombre de films", str(len(film_stats)))
        st.metric("Film le mieux noté", sorted_films.iloc[0]['film_title'])
        st.metric("Film le moins bien noté", sorted_films.iloc[-1]['film_title'])
        
        # Écart entre le meilleur et le pire score
        score_range = sorted_films.iloc[0]['sentiment_moyen'] - sorted_films.iloc[-1]['sentiment_moyen']
        st.metric("Écart de scores", f"{score_range:.4f}")
    
    # Tableau des statistiques
    st.subheader("Statistiques détaillées par film")
    st.dataframe(film_stats.sort_values(by='sentiment_moyen', ascending=False), use_container_width=True)

# Mode d'affichage par critique
else:
    st.header("Analyse Sentimentale par Critique")
    
    # Sélection du film
    selected_film = st.selectbox("Choisir un film", sorted(df['film_title'].unique()))
    
    # Filtrer les critiques du film sélectionné
    film_critiques = df[df['film_title'] == selected_film]
    
    # Afficher les statistiques pour ce film
    film_stat = film_stats[film_stats['film_title'] == selected_film].iloc[0]
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Score moyen", f"{film_stat['sentiment_moyen']:.4f}")
    with col2:
        st.metric("Écart-type", f"{film_stat['écart_type']:.4f}")
    with col3:
        st.metric("Score minimum", f"{film_stat['minimum']:.4f}")
    with col4:
        st.metric("Score maximum", f"{film_stat['maximum']:.4f}")
    
    # Distribution des scores pour ce film
    st.subheader(f"Distribution des scores pour {selected_film}")
    fig, ax = plt.subplots(figsize=(10, 4))
    sns.histplot(film_critiques['sentiment'], kde=True, ax=ax)
    ax.set_xlabel("Score de sentiment")
    ax.set_ylabel("Nombre de critiques")
    st.pyplot(fig)
    
    # Afficher les critiques avec leur score
    st.subheader("Critiques et scores")
    
    # Trier par score (descendant)
    sorted_critiques = film_critiques.sort_values(by='sentiment', ascending=False)
    
    for i, row in enumerate(sorted_critiques.itertuples()):
        expander = st.expander(f"Critique {i+1} - Score: {row.sentiment:.4f}")
        with expander:
            st.write(row.critique)

# Pied de page
st.sidebar.markdown("---")
st.sidebar.info("Projet NLP - Analyse de critiques de films")
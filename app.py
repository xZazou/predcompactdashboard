import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Analyse Talc", layout="wide")

st.title("🧪 Dashboard : Détection du Talc")

# Lien vers ton fichier Excel
url = "https://raw.githubusercontent.com/gevargas/predcompact/main/375_cosmetikwatch_19_08_2025.xlsx"

@st.cache_data
def load_data():
    data = pd.read_excel(url)
    # Cette ligne magique enlève les espaces et les erreurs de noms
    data.columns = data.columns.str.strip()
    return data

try:
    df = load_data()

    st.subheader("Aperçu des données")
    st.write(f"Nombre de produits : {len(df)}")
    
    # On affiche toutes les colonnes disponibles pour ne pas se tromper
    st.dataframe(df.head(10))

    # Graphique simple
    st.subheader("Répartition des produits")
    # On prend la 4ème colonne (souvent la catégorie) pour le graphique
    col_graph = df.columns[3] 
    fig, ax = plt.subplots()
    df[col_graph].value_counts().head(10).plot(kind='bar', ax=ax)
    st.pyplot(fig)

except Exception as e:
    st.error(f"Erreur de lecture du fichier : {e}")

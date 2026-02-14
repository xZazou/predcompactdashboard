import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Analyse Talc", layout="wide")

st.title("🧪 Dashboard : Détection du Talc dans les Cosmétiques")
st.write("Cet outil analyse la composition des produits pour prédire la présence de Talc.")

# Chargement des données directement depuis ton lien GitHub
url = "https://raw.githubusercontent.com/gevargas/predcompact/main/375_cosmetikwatch_19_08_2025.xlsx"

@st.cache_data
def load_data():
    return pd.read_excel(url)

df = load_data()

# --- INTERFACE ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("Aperçu des données")
    st.write(f"Nombre de produits analysés : {len(df)}")
    st.dataframe(df[['Nom du produit', 'Marque', 'Catégorie']].head(10))

with col2:
    st.subheader("Répartition par catégorie")
    fig, ax = plt.subplots()
    df['Catégorie'].value_counts().plot(kind='pie', autopct='%1.1f%%', ax=ax)
    st.pyplot(fig)

st.success("L'application est prête !")

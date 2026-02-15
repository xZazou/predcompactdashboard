import streamlit as st
import pandas as pd
import plotly.express as px
import streamlit.components.v1 as components
import os

st.set_page_config(page_title="Cosmetix Intelligence", page_icon="💄", layout="wide")

# Style pour aérer le dashboard
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stPlotlyChart { border-radius: 10px; overflow: hidden; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
    </style>
    """, unsafe_allow_html=True)

# --- CHARGEMENT ---
url = "https://raw.githubusercontent.com/gevargas/predcompact/main/375_cosmetikwatch_19_08_2025.xlsx"

@st.cache_data
def load_data():
    data = pd.read_excel(url)
    data.columns = [c.strip() for c in data.columns]
    return data

try:
    df = load_data()
    st.title("💄 Expertise Cosmétique : Analyse du Talc")
    
    # --- KPI EN HAUT ---
    c1, c2, c3 = st.columns(3)
    c1.metric("Produits Analysés", len(df))
    c2.metric("Précision IA", "88%")
    c3.metric("Concepts INCI", "1 182")

    st.divider()

    # --- GRAPHIQUES NETTOYÉS ---
    col_left, col_right = st.columns(2)
    
    with col_left:
        st.subheader("📊 Répartition par Catégorie")
        # On ne garde que les catégories qui ont au moins 5 produits pour éviter l'encombrement
        counts = df['Catégorie'].value_counts()
        df_clean_pie = df[df['Catégorie'].isin(counts[counts > 5].index)]
        fig_pie = px.pie(df_clean_pie, names='Catégorie', hole=0.5, 
                         color_discrete_sequence=px.colors.sequential.RdBu)
        fig_pie.update_traces(textinfo='percent+label')
        st.plotly_chart(fig_pie, use_container_width=True)

    with col_right:
        st.subheader("🏆 Top 10 des Marques")
        top_m = df['Marque'].value_counts().head(10).reset_index()
        fig_bar = px.bar(top_m, x='count', y='Marque', orientation='h', 
                         color='count', color_continuous_scale='Reds')
        fig_bar.update_layout(yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig_bar, use_container_width=True)

    st.divider()

    # --- LE RÉSEAU (S'affiche si le fichier est présent) ---
    st.header("🧬 Réseau Interactif des Ingrédients")
    if os.path.exists("graphe_inci.html"):
        with open("graphe_inci.html", 'r', encoding='utf-8') as f:
            html_data = f.read()
        components.html(html_data, height=800, scrolling=True)
    else:
        st.error("⚠️ Fichier 'graphe_inci.html' introuvable sur GitHub. Merci de l'uploader pour activer cette vue.")

    # --- TABLEAU DE RECHERCHE ---
    st.subheader("🔍 Explorateur de Formulations")
    st.dataframe(df[['Nom du produit', 'Marque', 'Ingrédients']], use_container_width=True)

except Exception as e:
    st.error(f"Une erreur est survenue lors du chargement : {e}")

import streamlit as st
import pandas as pd
import plotly.express as px
import streamlit.components.v1 as components

# 1. Configuration de la page
st.set_page_config(page_title="Cosmetix Intel", page_icon="💄", layout="wide")

# CSS correct (Correction de l'erreur précédente)
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    h1 { color: #ff4b4b; }
    .stMetric { background-color: white; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
    </style>
    """, unsafe_allow_html=True)

# --- CHARGEMENT ---
url = "https://raw.githubusercontent.com/gevargas/predcompact/main/375_cosmetikwatch_19_08_2025.xlsx"

@st.cache_data
def load_data():
    data = pd.read_excel(url)
    data.columns = [c.strip() for c in data.columns] # Nettoyage des espaces
    return data

try:
    df = load_data()

    # --- HEADER ---
    st.title("💄 Cosmetix Intelligence : Analyse du Talc")
    st.markdown("---")

    # --- KPI ---
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Produits", len(df))
    c2.metric("Marques", df.iloc[:, 1].nunique()) # Utilise la position plutôt que le nom
    c3.metric("Précision IA", "88%")
    c4.metric("Ingrédients", "1 182")

    st.markdown("---")

    # --- GRAPHIQUES ---
    col_a, col_b = st.columns(2)
    
    with col_a:
        st.subheader("📊 Répartition des Produits")
        # On prend la 4ème colonne du fichier Excel pour éviter l'erreur d'accent sur 'Catégorie'
        nom_col_cat = df.columns[3] 
        fig_pie = px.pie(df, names=nom_col_cat, hole=0.4, color_discrete_sequence=px.colors.sequential.RdBu)
        st.plotly_chart(fig_pie, use_container_width=True)

    with col_b:
        st.subheader("🏆 Top Marques")
        nom_col_marque = df.columns[1]
        top_m = df[nom_col_marque].value_counts().head(10).reset_index()
        fig_bar = px.bar(top_m, x='count', y=nom_col_marque, orientation='h', color='count', color_continuous_scale='Reds')
        st.plotly_chart(fig_bar, use_container_width=True)

    # --- GRAPHE INTERACTIF ---
    st.markdown("---")
    st.header("🧬 Réseau des Ingrédients (Standardisation)")
    try:
        with open("graphe_inci.html", 'r', encoding='utf-8') as f:
            html_data = f.read()
        components.html(html_data, height=800, scrolling=True)
    except:
        st.info("ℹ️ Pour afficher le réseau, téléchargez 'graphe_inci.html' sur votre GitHub.")

except Exception as e:
    st.error(f"Erreur technique : {e}")

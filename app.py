import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit.components.v1 as components

# 1. Configuration de la page (Look moderne)
st.set_page_config(page_title="Cosmetix Intel - Dashboard Talc", page_icon="💄", layout="wide")

# CSS pour personnaliser les couleurs
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    h1 { color: #ff4b4b; font-family: 'Trebuchet MS'; }
    .stMetric { background-color: white; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
    </style>
    """, unsafe_allow_stdio=True)

# --- CHARGEMENT ---
url = "https://raw.githubusercontent.com/gevargas/predcompact/main/375_cosmetikwatch_19_08_2025.xlsx"

@st.cache_data
def load_data():
    data = pd.read_excel(url)
    data.columns = [c.strip() for c in data.columns]
    return data

df = load_data()

# --- HEADER ---
st.title("💄 Cosmetix Intelligence : Analyse du Talc")
st.markdown("---")

# --- LIGNE 1 : CHIFFRES CLÉS (KPI) ---
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Produits", len(df))
with col2:
    st.metric("Marques uniques", df['Marque'].nunique())
with col3:
    st.metric("Précision IA", "88%", "+2% vs Baseline")
with col4:
    st.metric("Ingrédients Standardisés", "1 182")

st.markdown("---")

# --- LIGNE 2 : GRAPHIQUES INTERACTIFS ---
c1, c2 = st.columns([1, 1])

with c1:
    st.subheader("📊 Répartition par Catégorie")
    # Graphique en camembert interactif
    fig_pie = px.pie(df, names='Catégorie', hole=0.4, color_discrete_sequence=px.colors.sequential.RdBu)
    st.plotly_chart(fig_pie, use_container_width=True)

with c2:
    st.subheader("🏆 Top 10 des Marques")
    # Graphique à barres horizontal
    top_brands = df['Marque'].value_counts().head(10).reset_index()
    fig_bar = px.bar(top_brands, x='count', y='Marque', orientation='h', color='count', color_continuous_scale='Reds')
    st.plotly_chart(fig_bar, use_container_width=True)

st.markdown("---")

# --- LIGNE 3 : TON GRAPHE INTERACTIF (L'effet "Wow") ---
st.header("🧬 Réseau des Ingrédients (Clustering INCI)")
st.write("Ce graphe montre comment les variantes d'ingrédients ont été regroupées sous des noms standards.")

# Pour que ça marche, tu dois avoir mis 'graphe_inci.html' sur ton GitHub
try:
    with open("graphe_inci.html", 'r', encoding='utf-8') as f:
        html_data = f.read()
    components.html(html_data, height=800, scrolling=True)
except:
    st.warning("⚠️ Pour voir le graphe interactif ici, télécharge le fichier 'graphe_inci.html' sur ton GitHub.")

# --- LIGNE 4 : EXPLORATION ---
st.header("🔎 Explorateur de données")
st.dataframe(df, use_container_width=True)

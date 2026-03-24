import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Beans and Pods Analysis", layout="wide")

sns.set_style("whitegrid")


def load_data():
    df = pd.read_csv("BeansDataSet.csv")
    df["Channel"] = df["Channel"].astype(str)
    df["Region"] = df["Region"].astype(str)
    return df


df = load_data()

product_cols = ["Robusta", "Arabica", "Espresso", "Lungo", "Latte", "Cappuccino"]
df["TotalSales"] = df[product_cols].sum(axis=1)

# Sidebar
st.sidebar.title("Navigation")
page = st.sidebar.radio("Aller vers", [
    "Accueil",
    "Exploration",
    "Statistiques descriptives",
    "Visualisations",
    "Recommandations"
])

# Style principal
st.markdown("""
    <style>
    .main-title {
        font-size: 2.2rem;
        font-weight: 700;
        color: #2E4053;
        margin-bottom: 0.3rem;
    }
    .subtitle {
        font-size: 1.1rem;
        color: #5D6D7E;
        margin-bottom: 1.5rem;
    }
    .section-title {
        font-size: 1.4rem;
        font-weight: 600;
        color: #1F618D;
        margin-top: 1rem;
        margin-bottom: 0.8rem;
    }
    </style>
""", unsafe_allow_html=True)

if page == "Accueil":
    st.markdown('<div class="main-title">Projet Jordan IA1 - Beans and Pods</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Application Streamlit pour l’analyse des ventes et l’aide à la décision marketing.</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    col1.metric("Nombre de lignes", df.shape[0])
    col2.metric("Nombre de colonnes", df.shape[1])
    col3.metric("Ventes totales", f"{df['TotalSales'].sum():,.0f}")

    st.markdown('<div class="section-title">Aperçu du dataset</div>', unsafe_allow_html=True)
    st.dataframe(df.head(10), use_container_width=True)

elif page == "Exploration":
    st.markdown('<div class="main-title">Exploration des données</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Vue d’ensemble du dataset, types de variables et valeurs manquantes.</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-title">Dataset complet</div>', unsafe_allow_html=True)
    st.dataframe(df, use_container_width=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="section-title">Types des colonnes</div>', unsafe_allow_html=True)
        st.write(df.dtypes.astype(str))

    with col2:
        st.markdown('<div class="section-title">Valeurs manquantes</div>', unsafe_allow_html=True)
        st.write(df.isnull().sum())

elif page == "Statistiques descriptives":
    st.markdown('<div class="main-title">Statistiques descriptives</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Résumé statistique des ventes par produit.</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-title">Résumé statistique</div>', unsafe_allow_html=True)
    st.dataframe(df[product_cols + ["TotalSales"]].describe(), use_container_width=True)
 # total ventes
    st.markdown('<div class="section-title">Total des ventes</div>', unsafe_allow_html=True)
    total = df.sum(numeric_only=True)
    st.write(total)

elif page == "Visualisations":
    st.markdown('<div class="main-title">Visualisations</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Analyse visuelle des performances par produit, canal et région.</div>', unsafe_allow_html=True)

    product_totals = df[product_cols].sum().sort_values(ascending=False)

    st.markdown('<div class="section-title">Ventes totales par produit</div>', unsafe_allow_html=True)
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(x=product_totals.index, y=product_totals.values, ax=ax)
    ax.set_title("Ventes totales par produit", fontsize=14, fontweight="bold")
    ax.set_ylabel("Montant total")
    ax.set_xlabel("Produit")
    plt.xticks(rotation=20)
    st.pyplot(fig)

    channel_totals = df.groupby("Channel")["TotalSales"].sum()

    st.markdown('<div class="section-title">Ventes totales par canal</div>', unsafe_allow_html=True)
    fig, ax = plt.subplots(figsize=(8, 4))
    sns.barplot(x=channel_totals.index, y=channel_totals.values, ax=ax)
    ax.set_title("Ventes totales par canal", fontsize=14, fontweight="bold")
    ax.set_ylabel("Montant total")
    ax.set_xlabel("Canal")
    st.pyplot(fig)

    region_totals = df.groupby("Region")["TotalSales"].sum()

    st.markdown('<div class="section-title">Ventes totales par région</div>', unsafe_allow_html=True)
    fig, ax = plt.subplots(figsize=(8, 4))
    sns.barplot(x=region_totals.index, y=region_totals.values, ax=ax)
    ax.set_title("Ventes totales par région", fontsize=14, fontweight="bold")
    ax.set_ylabel("Montant total")
    ax.set_xlabel("Région")
    st.pyplot(fig)

     # Graphique par région groupées
    fig, ax = plt.subplots()
    df.groupby("Region").sum(numeric_only=True).plot(kind="bar", ax=ax)
    plt.title("Ventes par région")
    st.pyplot(fig)

       # Heatmap
    st.subheader("Corrélation")
    corr = df.corr(numeric_only=True)

    fig, ax = plt.subplots()
    sns.heatmap(corr, annot=True, cmap="coolwarm", ax=ax)
    st.pyplot(fig)

elif page == "Recommandations":
    st.markdown('<div class="main-title">Recommandations marketing</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Actions proposées à partir de l’analyse des ventes.</div>', unsafe_allow_html=True)

    st.info("Prioriser la région South pour les campagnes marketing.")
    st.success("Promouvoir Robusta dans les magasins.")
    st.warning("Promouvoir Arabica, Espresso et Latte en ligne.")
    st.info("Créer des offres groupées selon les préférences des clients.")
    st.success("Collecter davantage de données clients pour améliorer les campagnes.")
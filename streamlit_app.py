import math
import streamlit as st
import numpy as np
import pandas as pd

st.set_page_config(page_title="Analytics Calcio Auto", page_icon="⚽", layout="wide")

st.title("⚽ Analytics Calcio con Dati Ufficiali")
st.markdown("Seleziona il campionato per caricare le partite ufficiali e le medie gol storiche aggiornate.")

# Mappatura dei campionati principali da Football-Data.co.uk
CAMPIONATI = {
    "🇮🇹 Serie A (Italia)": "I1",
    "🇬🇧 Premier League (Inghilterra)": "E0",
    "🇪🇸 La Liga (Spagna)": "SP1",
    "🇩🇪 Bundesliga (Germania)": "D1",
    "🇫🇷 Ligue 1 (Francia)": "F1",
    "🇳🇱 Eredivisie (Olanda)": "N1"
}

st.sidebar.header("⚙️ Selezione Campionato")
campionato_scelto = st.sidebar.selectbox("Scegli Campionato", list(CAMPIONATI.keys()))

@st.cache_data(ttl=3600)
def carica_dati(codice_league):
    url = f"https://www.football-data.co.uk/mmz4281/2425/{codice_league}.csv"
    try:
        df = pd.read_csv(url)
        df = df[['HomeTeam', 'AwayTeam', 'FTHG', 'FTAG']].dropna()
        return df
    except Exception as e:
        return None

df_dati = carica_dati(CAMPIONATI[campionato_scelto])

if df_dati is not None and not df_dati.empty:
    squadre = sorted(list(set(df_dati['HomeTeam']).union(set(df_dati['AwayTeam']))))
    
    # Calcolo medie gol reali nel campionato
    medie_casa = df_dati.groupby('HomeTeam')['FTHG'].mean()
    medie_trasferta = df_dati.groupby('AwayTeam')['FTAG'].mean()
    media_generale_casa = df_dati['FTHG'].mean()
    media_generale_trasferta = df_dati['FTAG'].mean()
    
    st.sidebar.header("⚽ Selezione Partita")
    squadra_casa = st.sidebar.selectbox("Squadra in Casa", squadre, index=0)
    squadra_ospite = st.sidebar.selectbox("Squadra in Trasferta", squadre, index=min(1, len(squadre)-1))
    
    # Stima dinamica della media gol prevista
    att_casa = medie_casa.get(squadra_casa, media_generale_casa) / media_generale_casa
    def_ospite = medie_trasferta.get(squadra_ospite, media_generale_trasferta) / media_generale_trasferta
    lambda_casa = max(0.2, att_casa * def_ospite * media_generale_casa)
    
    att_ospite = medie_trasferta.get(squadra_ospite, media_generale_trasferta) / media_generale_trasferta
    def_casa = medie_casa.get(squadra_casa, media_generale_casa) / media_generale_casa
    lambda_ospite = max(0.2, att_ospite * def_casa * media_generale_trasferta)
    
    st.sidebar.divider()
    st.sidebar.subheader("📈 Medie Gol Attese (Auto)")
    media_casa = st.sidebar.number_input(f"Media Gol {squadra_casa}", value=float(round(lambda_casa, 2)), step=0.05)
    media_ospite = st.sidebar.number_input(f"Media Gol {squadra_ospite}", value=float(round(lambda_ospite, 2)), step=0.05)

    def poisson_pmf(k, mu):
        return (mu**k * math.exp(-mu)) / math.factorial(k)

    matrice = np.zeros((6, 6))
    for i in range(6):
        for j in range(6):
            matrice[i, j] = poisson_pmf(i, media_casa) * poisson_pmf(j, media_ospite)

    prob_1 = float(np.sum(np.tril(matrice, -1)))
    prob_x = float(np.sum(np.diag(matrice)))
    prob_2 = float(np.sum(np.triu(matrice, 1)))

    st.header(f"{squadra_casa} vs {squadra_ospite}")

    c1, c2, c3 = st.columns(3)
    c1.metric(f"Vittoria {squadra_casa} (1)", f"{prob_1*100:.1f}%", f"Fair Quota: {1/prob_1:.2f}")
    c2.metric("Pareggio (X)", f"{prob_x*100:.1f}%", f"Fair Quota: {1/prob_x:.2f}")
    c3.metric(f"Vittoria {squadra_ospite} (2)", f"{prob_2*100:.1f}%", f"Fair Quota: {1/prob_2:.2f}")

    st.divider()

    st.subheader("📌 Top 5 Risultati Esatti Più Probabili")
    risultati = []
    for i in range(6):
        for j in range(6):
            risultati.append({"Risultato": f"{i} - {j}", "Probabilità": f"{matrice[i, j]*100:.2f}%"})

    df_res = pd.DataFrame(risultati).sort_values(by="Probabilità", ascending=False).head(5)
    st.dataframe(df_res, use_container_width=True, hide_index=True)

else:
    st.error("Impossibile scaricare i dati per questo campionato. Riprova più tardi.")

import math
import streamlit as st
import numpy as np
import pandas as pd

st.set_page_config(page_title="Analytics Calcio & Nazionali", page_icon="⚽", layout="wide")

st.title("⚽ Calcolatore Probabilità (Club & Nazionali)")
st.markdown("Seleziona una Competizione di Club o le Nazionali per calcolare le probabilità di vittoria e le Fair Quote.")

CAMPIONATI = {
    "🇮🇹 Serie A (Italia)": ("club", "I1"),
    "🇬🇧 Premier League (Inghilterra)": ("club", "E0"),
    "🇪🇸 La Liga (Spagna)": ("club", "SP1"),
    "🇩🇪 Bundesliga (Germania)": ("club", "D1"),
    "🇫🇷 Ligue 1 (Francia)": ("club", "F1"),
    "🇳🇱 Eredivisie (Olanda)": ("club", "N1"),
    "🌍 Nazionali (Amichevoli / Qualificazioni)": ("nations", "NAT")
}

st.sidebar.header("⚙️ Selezione Categoria")
campionato_scelto = st.sidebar.selectbox("Scegli Campionato", list(CAMPIONATI.keys()))
tipo_comp, codice_league = CAMPIONATI[campionato_scelto]

DATI_NAZIONALI = {
    "Italia": (1.65, 1.25),
    "Francia": (2.10, 1.50),
    "Germania": (2.00, 1.40),
    "Inghilterra": (2.05, 1.45),
    "Spagna": (2.15, 1.55),
    "Portogallo": (1.90, 1.35),
    "Argentina": (1.85, 1.30),
    "Brasile": (2.10, 1.45),
    "Olanda": (1.95, 1.40),
    "Belgio": (1.80, 1.30),
    "Croazia": (1.50, 1.20),
    "Svizzera": (1.45, 1.15),
    "Uruguay": (1.55, 1.20),
    "Colombia": (1.50, 1.10),
    "Giappone": (1.60, 1.25)
}

@st.cache_data(ttl=3600)
def carica_dati_club(codice):
    url = f"https://www.football-data.co.uk/mmz4281/2425/{codice}.csv"
    try:
        df = pd.read_csv(url)
        return df[['HomeTeam', 'AwayTeam', 'FTHG', 'FTAG']].dropna()
    except Exception as e:
        return None

if tipo_comp == "club":
    df_dati = carica_dati_club(codice_league)
    if df_dati is not None and not df_dati.empty:
        squadre = sorted(list(set(df_dati['HomeTeam']).union(set(df_dati['AwayTeam']))))
        medie_casa = df_dati.groupby('HomeTeam')['FTHG'].mean()
        medie_trasferta = df_dati.groupby('AwayTeam')['FTAG'].mean()
        media_gen_casa = df_dati['FTHG'].mean()
        media_gen_trasferta = df_dati['FTAG'].mean()
        
        st.sidebar.header("⚽ Selezione Partita")
        s_casa = st.sidebar.selectbox("Squadra Casa", squadre, index=0)
        s_ospite = st.sidebar.selectbox("Squadra Trasferta", squadre, index=min(1, len(squadre)-1))
        
        att_casa = medie_casa.get(s_casa, media_gen_casa) / media_gen_casa
        def_ospite = medie_trasferta.get(s_ospite, media_gen_trasferta) / media_gen_trasferta
        lambda_casa = max(0.2, att_casa * def_ospite * media_gen_casa)
        
        att_ospite = medie_trasferta.get(s_ospite, media_gen_trasferta) / media_gen_trasferta
        def_casa = medie_casa.get(s_casa, media_gen_casa) / media_gen_casa
        lambda_ospite = max(0.2, att_ospite * def_casa * media_gen_trasferta)
    else:
        st.error("Errore nel caricamento dei dati.")
        st.stop()
else:
    squadre = sorted(list(DATI_NAZIONALI.keys()))
    st.sidebar.header("🌍 Selezione Nazionali")
    s_casa = st.sidebar.selectbox("Nazionale Casa", squadre, index=0)
    s_ospite = st.sidebar.selectbox("Nazionale Trasferta", squadre, index=1)
    
    mc_casa, mt_casa = DATI_NAZIONALI.get(s_casa, (1.5, 1.2))
    mc_ospite, mt_ospite = DATI_NAZIONALI.get(s_ospite, (1.5, 1.2))
    
    lambda_casa = max(0.2, (mc_casa + mt_casa) / 2.0 * 1.1)
    lambda_ospite = max(0.2, (mc_ospite + mt_ospite) / 2.0 * 0.9)

st.sidebar.divider()
st.sidebar.subheader("📈 Medie Gol Stimate")
media_casa = st.sidebar.number_input(f"Media Gol {s_casa}", value=float(round(lambda_casa, 2)), step=0.05)
media_ospite = st.sidebar.number_input(f"Media Gol {s_ospite}", value=float(round(lambda_ospite, 2)), step=0.05)

def poisson_pmf(k, mu):
    return (mu**k * math.exp(-mu)) / math.factorial(k)

matrice = np.zeros((6, 6))
for i in range(6):
    for j in range(6):
        matrice[i, j] = poisson_pmf(i, media_casa) * poisson_pmf(j, media_ospite)

prob_1 = float(np.sum(np.tril(matrice, -1)))
prob_x = float(np.sum(np.diag(matrice)))
prob_2 = float(np.sum(np.triu(matrice, 1)))

st.header(f"⚔️ {s_casa} vs {s_ospite}")

c1, c2, c3 = st.columns(3)
c1.metric(f"Vittoria {s_casa} (1)", f"{prob_1*100:.1f}%", f"Fair Quota: {1/prob_1:.2f}")
c2.metric("Pareggio (X)", f"{prob_x*100:.1f}%", f"Fair Quota: {1/prob_x:.2f}")
c3.metric(f"Vittoria {s_ospite} (2)", f"{prob_2*100:.1f}%", f"Fair Quota: {1/prob_2:.2f}")

st.divider()

st.subheader("📌 Top 5 Risultati Esatti Più Probabili")
risultati = []
for i in range(6):
    for j in range(6):
        risultati.append({"Risultato": f"{i} - {j}", "Probabilità": f"{matrice[i, j]*100:.2f}%"})

df_res = pd.DataFrame(risultati).sort_values(by="Probabilità", ascending=False).head(5)
st.dataframe(df_res, use_container_width=True, hide_index=True)
    

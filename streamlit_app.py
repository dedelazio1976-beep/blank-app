import math
import streamlit as st
import numpy as np
import pandas as pd

st.set_page_config(page_title="Analytics Calcio & Betting", page_icon="⚽", layout="wide")

st.title("⚽ Calcolatore Probabilità & Betting (Club & Nazionali)")
st.markdown("Analisi completa delle probabilità e Fair Quote per i principali mercati di scommessa.")

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

# Matrice Gol (da 0-0 a 7-7)
matrice = np.zeros((8, 8))
for i in range(8):
    for j in range(8):
        matrice[i, j] = poisson_pmf(i, media_casa) * poisson_pmf(j, media_ospite)

prob_1 = float(np.sum(np.tril(matrice, -1)))
prob_x = float(np.sum(np.diag(matrice)))
prob_2 = float(np.sum(np.triu(matrice, 1)))

st.header(f"⚔️ {s_casa} vs {s_ospite}")

# --- ESITO FINALE (1X2) ---
st.subheader("1️⃣ Esito Finale (1X2)")
c1, c2, c3 = st.columns(3)
c1.metric(f"1 ({s_casa})", f"{prob_1*100:.1f}%", f"Fair Quota: {1/prob_1:.2f}")
c2.metric("X (Pareggio)", f"{prob_x*100:.1f}%", f"Fair Quota: {1/prob_x:.2f}")
c3.metric(f"2 ({s_ospite})", f"{prob_2*100:.1f}%", f"Fair Quota: {1/prob_2:.2f}")

st.divider()

# --- DOPPIA CHANCE ---
st.subheader("🛡️ Doppia Chance")
prob_1x = prob_1 + prob_x
prob_x2 = prob_x + prob_2
prob_12 = prob_1 + prob_2

d1, d2, d3 = st.columns(3)
d1.metric("1X", f"{prob_1x*100:.1f}%", f"Fair Quota: {1/prob_1x:.2f}")
d2.metric("12", f"{prob_12*100:.1f}%", f"Fair Quota: {1/prob_12:.2f}")
d3.metric("X2", f"{prob_x2*100:.1f}%", f"Fair Quota: {1/prob_x2:.2f}")

st.divider()

# --- GOAL / NO GOAL & OVER/UNDER ---
col_gn, col_uo = st.columns(2)

with col_gn:
    st.subheader("⚽ Goal / No Goal")
    prob_gg = float(np.sum(matrice[1:, 1:]))
    prob_ng = 1.0 - prob_gg
    
    st.write(f"**GOAL (Entrambe segnano):** {prob_gg*100:.1f}% | *Fair Quota:* **{1/prob_gg:.2f}**")
    st.write(f"**NO GOAL:** {prob_ng*100:.1f}% | *Fair Quota:* **{1/prob_ng:.2f}**")

with col_uo:
    st.subheader("📊 Under / Over Totali")
    medie_uo = [0.5, 1.5, 2.5, 3.5, 4.5]
    dati_uo = []
    
    for uo in medie_uo:
        prob_under = 0.0
        for i in range(8):
            for j in range(8):
                if i + j < uo:
                    prob_under += matrice[i, j]
        prob_over = 1.0 - prob_under
        
        dati_uo.append({
            "Soglia": f"{uo}",
            "Under %": f"{prob_under*100:.1f}%",
            "Quota Under": f"{1/prob_under:.2f}" if prob_under > 0 else "-",
            "Over %": f"{prob_over*100:.1f}%",
            "Quota Over": f"{1/prob_over:.2f}" if prob_over > 0 else "-"
        })
    st.dataframe(pd.DataFrame(dati_uo), use_container_width=True, hide_index=True)

st.divider()

# --- MULTIGOL ---
st.subheader("🎯 Multigol")
multigol_ranges = [
    ("1-2 Gol", 1, 2),
    ("1-3 Gol", 1, 3),
    ("2-3 Gol", 2, 3),
    ("2-4 Gol", 2, 4),
    ("2-5 Gol", 2, 5),
    ("3-5 Gol", 3, 5),
    ("4+ Gol", 4, 15)
]

dati_mg = []
for nome, min_g, max_g in multigol_ranges:
    p_mg = 0.0
    for i in range(8):
        for j in range(8):
            if min_g <= (i + j) <= max_g:
                p_mg += matrice[i, j]
    dati_mg.append({
        "Multigol": nome,
        "Probabilità": f"{p_mg*100:.1f}%",
        "Fair Quota": f"{1/p_mg:.2f}" if p_mg > 0 else "-"
    })

m1, m2 = st.columns(2)
with m1:
    st.dataframe(pd.DataFrame(dati_mg[:4]), use_container_width=True, hide_index=True)
with m2:
    st.dataframe(pd.DataFrame(dati_mg[4:]), use_container_width=True, hide_index=True)

st.divider()

# --- RISULTATI ESATTI ---
st.subheader("📌 Top 5 Risultati Esatti Più Probabili")
risultati = []
for i in range(6):
    for j in range(6):
        p_res = matrice[i, j]
        risultati.append({
            "Risultato": f"{i} - {j}",
            "Probabilità": f"{p_res*100:.2f}%",
            "Fair Quota": f"{1/p_res:.2f}" if p_res > 0 else "-"
        })

df_res = pd.DataFrame(risultati).sort_values(by="Probabilità", ascending=False).head(5)
st.dataframe(df_res, use_container_width=True, hide_index=True)

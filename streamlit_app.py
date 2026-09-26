import math
import streamlit as st
import numpy as np
import pandas as pd

st.set_page_config(page_title="Analytics Calcio & Betting Pro", page_icon="⚽", layout="wide")

st.title("⚽ Calcolatore Probabilità & Betting Pro")
st.markdown("Analisi completa delle probabilità e Fair Quote per Campionati, Coppe Europee e Nazionali.")

CAMPIONATI = {
    "🌍 Coppa d'Africa (AFCON)": ("afcon", "AFCON"),
    "🏆 UEFA Champions League": ("coppe", "CL"),
    "🇪🇺 UEFA Europa League": ("coppe", "EL"),
    "🇮🇹 Serie A (Italia)": ("club", "I1"),
    "🇮🇹 Serie B (Italia)": ("club", "I2"),
    "🌍 UEFA Nations League": ("nations", "NL"),
    "🇬🇧 Premier League (Inghilterra)": ("club", "E0"),
    "🇪🇸 La Liga (Spagna)": ("club", "SP1"),
    "🇩🇪 Bundesliga (Germania)": ("club", "D1"),
    "🇫🇷 Ligue 1 (Francia)": ("club", "F1"),
    "🇳🇱 Eredivisie (Olanda)": ("club", "N1")
}

st.sidebar.header("⚙️ Selezione Categoria")
campionato_scelto = st.sidebar.selectbox("Scegli Competizione", list(CAMPIONATI.keys()))
tipo_comp, codice_league = CAMPIONATI[campionato_scelto]

# Database Coppa d'Africa (AFCON)
DATI_AFCON = {
    "Costa d'Avorio": {"rating": 84, "att": 1.6, "def": 0.9},
    "Nigeria": {"rating": 85, "att": 1.8, "def": 1.0},
    "Marocco": {"rating": 87, "att": 1.9, "def": 0.7},
    "Senegal": {"rating": 86, "att": 1.8, "def": 0.8},
    "Egitto": {"rating": 83, "att": 1.5, "def": 0.9},
    "Algeria": {"rating": 82, "att": 1.6, "def": 1.0},
    "Camerun": {"rating": 81, "att": 1.4, "def": 1.0},
    "Ghana": {"rating": 78, "att": 1.3, "def": 1.2},
    "Mali": {"rating": 79, "att": 1.3, "def": 0.9},
    "Sudafrica": {"rating": 77, "att": 1.2, "def": 1.0},
    "Tunisia": {"rating": 79, "att": 1.2, "def": 0.9},
    "RD del Congo": {"rating": 77, "att": 1.2, "def": 1.1},
    "Burkina Faso": {"rating": 76, "att": 1.2, "def": 1.1},
    "Guinea": {"rating": 76, "att": 1.2, "def": 1.1},
    "Capo Verde": {"rating": 75, "att": 1.1, "def": 1.0},
    "Angola": {"rating": 74, "att": 1.1, "def": 1.1},
    "Zambia": {"rating": 73, "att": 1.0, "def": 1.3},
    "Mauritania": {"rating": 70, "att": 0.8, "def": 1.3},
    "Gambia": {"rating": 72, "att": 0.9, "def": 1.3},
    "Mozambico": {"rating": 69, "att": 0.8, "def": 1.5},
    "Namibia": {"rating": 68, "att": 0.7, "def": 1.4},
    "Tanzania": {"rating": 67, "att": 0.7, "def": 1.5},
    "Guinea-Bissau": {"rating": 70, "att": 0.8, "def": 1.4},
    "Equatoriale Guinea": {"rating": 74, "att": 1.1, "def": 1.2}
}

# Database Coppe Europee (Champions & Europa League)
DATI_COPPE = {
    "Real Madrid": {"rating": 94, "att": 2.3, "def": 0.8},
    "Manchester City": {"rating": 94, "att": 2.4, "def": 0.8},
    "Bayern Monaco": {"rating": 91, "att": 2.2, "def": 0.9},
    "PSG": {"rating": 90, "att": 2.1, "def": 0.9},
    "Arsenal": {"rating": 89, "att": 2.0, "def": 0.8},
    "Inter": {"rating": 89, "att": 1.9, "def": 0.8},
    "Barcelona": {"rating": 88, "att": 2.1, "def": 1.0},
    "Liverpool": {"rating": 90, "att": 2.2, "def": 0.9},
    "Atletico Madrid": {"rating": 86, "att": 1.6, "def": 0.9},
    "Juventus": {"rating": 85, "att": 1.6, "def": 0.9},
    "Bayer Leverkusen": {"rating": 88, "att": 2.1, "def": 0.9},
    "Borussia Dortmund": {"rating": 86, "att": 1.8, "def": 1.1},
    "Atalanta": {"rating": 85, "att": 1.9, "def": 1.1},
    "AC Milan": {"rating": 84, "att": 1.6, "def": 1.1},
    "Benfica": {"rating": 83, "att": 1.7, "def": 1.0},
    "Sporting CP": {"rating": 84, "att": 1.9, "def": 1.0},
    "PSV Eindhoven": {"rating": 82, "att": 1.8, "def": 1.1},
    "RB Leipzig": {"rating": 84, "att": 1.8, "def": 1.1},
    "Aston Villa": {"rating": 83, "att": 1.7, "def": 1.1},
    "Lille": {"rating": 80, "att": 1.4, "def": 1.0},
    "Monaco": {"rating": 81, "att": 1.6, "def": 1.1},
    "Manchester United": {"rating": 85, "att": 1.7, "def": 1.1},
    "Tottenham": {"rating": 86, "att": 1.9, "def": 1.1},
    "AS Roma": {"rating": 83, "att": 1.5, "def": 1.0},
    "Lazio": {"rating": 82, "att": 1.5, "def": 1.0},
    "Athletic Bilbao": {"rating": 83, "att": 1.5, "def": 0.9},
    "Real Sociedad": {"rating": 82, "att": 1.4, "def": 0.9},
    "Eintracht Francoforte": {"rating": 82, "att": 1.6, "def": 1.2},
    "Ajax": {"rating": 80, "att": 1.5, "def": 1.2},
    "Porto": {"rating": 83, "att": 1.6, "def": 0.9},
    "Galatasaray": {"rating": 81, "att": 1.7, "def": 1.2},
    "Fenerbahce": {"rating": 81, "att": 1.6, "def": 1.1}
}

# Database Nazionali Europee
DATI_NAZIONALI = {
    "Francia": {"rating": 92, "att": 2.2, "def": 0.8},
    "Spagna": {"rating": 91, "att": 2.1, "def": 0.8},
    "Inghilterra": {"rating": 90, "att": 2.1, "def": 0.8},
    "Germania": {"rating": 88, "att": 2.0, "def": 1.0},
    "Portugal": {"rating": 88, "att": 2.0, "def": 0.9},
    "Olanda": {"rating": 86, "att": 1.9, "def": 1.1},
    "Italia": {"rating": 85, "att": 1.6, "def": 0.9},
    "Belgio": {"rating": 84, "att": 1.7, "def": 1.1},
    "Croazia": {"rating": 83, "att": 1.4, "def": 1.0},
    "Svizzera": {"rating": 81, "att": 1.4, "def": 1.1},
    "Danimarca": {"rating": 81, "att": 1.5, "def": 1.0},
    "Serbia": {"rating": 78, "att": 1.3, "def": 1.3},
    "Ungheria": {"rating": 77, "att": 1.2, "def": 1.2},
    "Polonia": {"rating": 77, "att": 1.3, "def": 1.4},
    "Scozia": {"rating": 76, "att": 1.1, "def": 1.3},
    "Ucraina": {"rating": 78, "att": 1.4, "def": 1.2},
    "Austria": {"rating": 80, "att": 1.6, "def": 1.1},
    "Turchia": {"rating": 79, "att": 1.6, "def": 1.2},
    "Norvegia": {"rating": 79, "att": 1.7, "def": 1.3},
    "Svezia": {"rating": 77, "att": 1.6, "def": 1.2}
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
        st.error("Errore nel caricamento dei dati del campionato.")
        st.stop()

elif tipo_comp == "afcon":
    squadre = sorted(list(DATI_AFCON.keys()))
    st.sidebar.header("🌍 Coppa d'Africa - Partita")
    s_casa = st.sidebar.selectbox("Nazionale Casa / Designata", squadre, index=squadre.index("Marocco") if "Marocco" in squadre else 0)
    s_ospite = st.sidebar.selectbox("Nazionale Trasferta", squadre, index=squadre.index("Nigeria") if "Nigeria" in squadre else 1)
    
    campo_neutro = st.sidebar.checkbox("Campo Neutro (Torneo Finale)", value=True)
    
    d_casa = DATI_AFCON[s_casa]
    d_ospite = DATI_AFCON[s_ospite]
    
    diff_rating = d_casa["rating"] - d_ospite["rating"]
    bonus_campo = 0.20 if not campo_neutro else 0.0
    
    # La Coppa d'Africa ha medie gol storicamente un po' più basse
    lambda_casa = max(0.2, ((d_casa["att"] + d_ospite["def"]) / 2.0 + (diff_rating * 0.02) + bonus_campo) * 0.9)
    lambda_ospite = max(0.2, ((d_ospite["att"] + d_casa["def"]) / 2.0 - (diff_rating * 0.02)) * 0.9)

elif tipo_comp == "coppe":
    squadre = sorted(list(DATI_COPPE.keys()))
    st.sidebar.header("🏆 Coppe Europee - Partita")
    s_casa = st.sidebar.selectbox("Squadra in Casa", squadre, index=squadre.index("Real Madrid") if "Real Madrid" in squadre else 0)
    s_ospite = st.sidebar.selectbox("Squadra in Trasferta", squadre, index=squadre.index("Inter") if "Inter" in squadre else 1)
    
    campo_neutro = st.sidebar.checkbox("Campo Neutro (es. Finale)", value=False)
    
    d_casa = DATI_COPPE[s_casa]
    d_ospite = DATI_COPPE[s_ospite]
    
    diff_rating = d_casa["rating"] - d_ospite["rating"]
    bonus_campo = 0.25 if not campo_neutro else 0.0
    
    lambda_casa = max(0.2, (d_casa["att"] + d_ospite["def"]) / 2.0 + (diff_rating * 0.025) + bonus_campo)
    lambda_ospite = max(0.2, (d_ospite["att"] + d_casa["def"]) / 2.0 - (diff_rating * 0.025))

else:
    squadre = sorted(list(DATI_NAZIONALI.keys()))
    st.sidebar.header("🌍 Nations League - Partita")
    s_casa = st.sidebar.selectbox("Nazionale in Casa", squadre, index=squadre.index("Italia") if "Italia" in squadre else 0)
    s_ospite = st.sidebar.selectbox("Nazionale in Trasferta", squadre, index=squadre.index("Francia") if "Francia" in squadre else 1)
    
    campo_neutro = st.sidebar.checkbox("Campo Neutro / Fase Finale", value=False)
    
    d_casa = DATI_NAZIONALI[s_casa]
    d_ospite = DATI_NAZIONALI[s_ospite]
    
    diff_rating = d_casa["rating"] - d_ospite["rating"]
    bonus_campo = 0.22 if not campo_neutro else 0.0
    
    lambda_casa = max(0.2, (d_casa["att"] + d_ospite["def"]) / 2.0 + (diff_rating * 0.025) + bonus_campo)
    lambda_ospite = max(0.2, (d_ospite["att"] + d_casa["def"]) / 2.0 - (diff_rating * 0.025))

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
    

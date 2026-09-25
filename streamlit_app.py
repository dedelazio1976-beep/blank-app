import math
import streamlit as st
import numpy as np
import pandas as pd

st.set_page_config(page_title="Analytics Calcio", page_icon="⚽", layout="wide")

st.title("⚽ Calcolatore Probabilità Calcio")
st.markdown("Inserisci le medie gol per calcolare percentuali e **quote reali**.")

st.sidebar.header("⚙️ Dati Partita")
squadra_casa = st.sidebar.text_input("Squadra Casa", "Inter")
squadra_ospite = st.sidebar.text_input("Squadra Ospite", "Milan")

media_casa = st.sidebar.number_input(f"Media Gol {squadra_casa}", min_value=0.1, value=1.85, step=0.05)
media_ospite = st.sidebar.number_input(f"Media Gol {squadra_ospite}", min_value=0.1, value=1.15, step=0.05)

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

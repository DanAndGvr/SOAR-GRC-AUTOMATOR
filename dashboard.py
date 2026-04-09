import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="SOC Command Center", layout="wide")

st.title("SOC & SOAR Command Center (Executive View)")
st.markdown("Monitorizare in timp real a incidentelor de securitate, Threat Intelligence si conformitate GRC.")

DB_FILE = "atacuri.csv"

def incarca_date():
    if os.path.exists(DB_FILE):
        try:
            return pd.read_csv(DB_FILE)
        except Exception:
            return pd.DataFrame()
    return pd.DataFrame()

df = incarca_date()

if not df.empty:
    st.subheader("Statistici Amenintari")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Atacuri Blocate", len(df))
    col2.metric("Sursa Principala (Tara)", df["Tara"].mode()[0])
    col3.metric("Ultimul Incident", df["Data"].iloc[-1])

    st.markdown("---")

    st.subheader("Harta Amenintarilor Globale (Threat Map)")
    st.map(df, zoom=1, color="#ff0000", size=3000)

    st.markdown("---")

    st.subheader("Registru de Audit si Conformitate (NIS2 & ISO 27001)")
    
    tabel_display = df[["Data", "IP", "Tara", "Oras", "Politica_Incalcata", "Hash_Dovada"]]
    st.dataframe(tabel_display, use_container_width=True)
    
    st.button("Actualizare Date Live")
else:
    st.info("[INFO] Baza de date este curata. Sistemul monitorizeaza activ reteaua.")

import streamlit as st
import json
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent

CONFIG_DIR = BASE_DIR / "config"
HISTORICO_DIR = BASE_DIR / "historico"

SISTEMAS_FILE = CONFIG_DIR / "sistemas.json"
JUSTIFICATIVAS_FILE = CONFIG_DIR / "justificativas.json"

with open(SISTEMAS_FILE, encoding="utf-8") as f:
    sistemas = json.load(f)

with open(JUSTIFICATIVAS_FILE, encoding="utf-8") as f:
    justificativas = json.load(f)

st.title("📊 Dashboard")

# =====================
# Indicadores
# =====================

total_sistemas = len(sistemas)

total_perfis = sum(
    len(perfis)
    for perfis in sistemas.values()
)

total_justificativas = len(
    justificativas["justificativas"]
)

# Cada solicitação gera um CSV e um Excel no histórico.
# Contamos só os CSV para não contar a mesma solicitação duas vezes.
# O nome começa com o timestamp, então ordenar pelo nome deixa os mais novos primeiro.
if HISTORICO_DIR.exists():

    arquivos_historico = sorted(
        HISTORICO_DIR.glob("*.csv"),
        key=lambda arquivo: arquivo.name,
        reverse=True
    )

else:

    arquivos_historico = []

total_arquivos = len(
    arquivos_historico
)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Sistemas",
        total_sistemas
    )

with col2:
    st.metric(
        "Perfis",
        total_perfis
    )

with col3:
    st.metric(
        "Justificativas",
        total_justificativas
    )

with col4:
    st.metric(
        "Solicitações geradas",
        total_arquivos
    )

# =====================
# Histórico
# =====================

st.divider()

st.subheader(
    "Últimas Solicitações Geradas"
)

if arquivos_historico:

    for arquivo in arquivos_historico[:20]:

        st.write(
            arquivo.name
        )

else:

    st.info(
        "Nenhuma solicitação gerada ainda."
    )
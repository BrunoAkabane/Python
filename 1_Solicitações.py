import streamlit as st
import pandas as pd
import json

from pathlib import Path
from datetime import datetime
from io import BytesIO

# ============================
# CONFIGURAÇÕES
# ============================

BASE_DIR = Path(__file__).parent.parent

CONFIG_DIR = BASE_DIR / "config"

EXPORTADOS_DIR = BASE_DIR / "exportados"
HISTORICO_DIR = BASE_DIR / "historico"

SISTEMAS_FILE = CONFIG_DIR / "sistemas.json"
JUSTIFICATIVAS_FILE = CONFIG_DIR / "justificativas.json"

# ============================
# JSON
# ============================

with open(SISTEMAS_FILE, encoding="utf-8") as f:
    sistemas = json.load(f)

with open(JUSTIFICATIVAS_FILE, encoding="utf-8") as f:
    justificativas = json.load(f)

# ============================
# TELA
# ============================

st.title("📄 Solicitações")

if not sistemas:
    st.warning("Nenhum sistema cadastrado. Cadastre um na página Administração.")
    st.stop()

sistema = st.selectbox(
    "Sistema",
    list(sistemas.keys())
)

if not sistemas[sistema]:
    st.warning("Este sistema não possui perfis. Cadastre um na página Administração.")
    st.stop()

perfil = st.selectbox(
    "Perfil",
    sistemas[sistema]
)

acao = st.selectbox(
    "Ação",
    [
        "ADICIONAR",
        "REMOVER"
    ]
)

if not justificativas["justificativas"]:
    st.warning("Nenhuma justificativa cadastrada. Cadastre uma na página Administração.")
    st.stop()

justificativa = st.selectbox(
    "Justificativa",
    justificativas["justificativas"]
)

st.divider()

origem = st.radio(
    "Origem",
    [
        "Colar Logins",
        "Importar Excel"
    ]
)

logins = []

if origem == "Colar Logins":

    texto = st.text_area(
        "Digite um login por linha",
        height=200
    )

    if texto:

        logins = [
            linha.strip().upper()
            for linha in texto.splitlines()
            if linha.strip()
        ]

else:

    arquivo_excel = st.file_uploader(
        "Selecione o Excel",
        type=["xlsx"]
    )

    if arquivo_excel:

        # dtype=str evita que logins numéricos virem "1234.0"
        df_excel = pd.read_excel(
            arquivo_excel,
            dtype=str
        )

        coluna = st.selectbox(
            "Coluna Login",
            df_excel.columns
        )

        logins = (
            df_excel[coluna]
            .dropna()
            .astype(str)
            .str.strip()
            .str.upper()
            .tolist()
        )

        logins = [login for login in logins if login]

if logins:

    logins_unicos = list(dict.fromkeys(logins))

    df_final = pd.DataFrame(
        {
            "Login no IDM": logins_unicos,
            "Acao": acao,
            "Perfil": perfil,
            "Justificativa": justificativa
        }
    )

    st.dataframe(df_final)

    # CSV com separador ";" e BOM (utf-8-sig) para o Excel abrir os acentos certo.
    # O .encode é necessário: to_csv sem caminho devolve texto e ignora o encoding.
    csv = df_final.to_csv(
        sep=";",
        index=False
    ).encode("utf-8-sig")

    excel_buffer = BytesIO()

    with pd.ExcelWriter(
        excel_buffer,
        engine="openpyxl"
    ) as writer:

        df_final.to_excel(
            writer,
            index=False
        )

    excel_data = excel_buffer.getvalue()

    nome_sistema = sistema.replace(" ", "_")

    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    arquivo_csv = EXPORTADOS_DIR / f"{nome_sistema}.csv"
    arquivo_xlsx = EXPORTADOS_DIR / f"{nome_sistema}.xlsx"

    historico_csv = HISTORICO_DIR / f"{timestamp}_{nome_sistema}.csv"
    historico_xlsx = HISTORICO_DIR / f"{timestamp}_{nome_sistema}.xlsx"

    # Os arquivos só são gravados quando o usuário clica no botão.
    # Sem isso, qualquer interação na tela gravaria tudo de novo.
    if st.button("Gerar arquivos"):

        EXPORTADOS_DIR.mkdir(parents=True, exist_ok=True)
        HISTORICO_DIR.mkdir(parents=True, exist_ok=True)

        arquivo_csv.write_bytes(csv)
        arquivo_xlsx.write_bytes(excel_data)

        historico_csv.write_bytes(csv)
        historico_xlsx.write_bytes(excel_data)

        st.success("Arquivos gerados em exportados/ e historico/")

    col1, col2 = st.columns(2)

    with col1:

        st.download_button(
            "📄 Baixar CSV",
            csv,
            f"{nome_sistema}.csv",
            mime="text/csv"
        )

    with col2:

        st.download_button(
            "📊 Baixar Excel",
            excel_data,
            f"{nome_sistema}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
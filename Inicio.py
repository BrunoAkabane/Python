import streamlit as st
from pathlib import Path


st.set_page_config(
    page_title="Gerador de Acessos",
    page_icon="🔐",
    layout="wide"
)

st.page_link("pages/1_Solicitações.py", label="Solicitações", icon="📄")
st.page_link("pages/2_Administração.py", label="Administração", icon="⚙️")
st.page_link("pages/3_Dashboard.py", label="Dashboard", icon="📊")

st.title("🔐 Gerador de Acessos")

st.markdown("""
Bem-vindo ao sistema.

Utilize o menu lateral para acessar:

- 📄 Solicitações
- ⚙️ Administração
- 📊 Dashboard
""")

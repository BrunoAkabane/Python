import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

db_grafico = pd.read_csv(r'C:/Users/bruno/OneDrive/Área de Trabalho/Microsoft VS Code/Projetos/UNIP/BD_Entradas.csv')


fig = px.bar(db_grafico["DIRECIONAMENTO"].value_counts())
fig2 = px.histogram(db_grafico["FINALIZACAO_URA"])


col95, col100 = st.columns(2)
col95.plotly_chart(fig)
col100 .plotly_chart(fig2)

streamlit run c:/Users/bruno/OneDrive/Área de Trabalho/Microsoft VS Code/Projetos/UNIP/Grafico.py [GeneratorExit]
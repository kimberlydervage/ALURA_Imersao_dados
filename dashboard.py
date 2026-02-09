import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")
st.title("Teste Final - Funcionou!")
st.write("Se você vê isso, o problema era o arquivo app.py antigo.")

# Tenta carregar os dados com proteção de erro
try:
    url = "https://raw.githubusercontent.com/vqrca/dashboard_salarios_dados/main/dados-imersao-final.csv"
    df = pd.read_csv(url)
    st.success(f"Dados carregados com sucesso! {df.shape[0]} linhas.")
    st.dataframe(df.head())
except Exception as e:
    st.error(f"Erro ao ler CSV: {e}")
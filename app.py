import streamlit as st
import pandas as pd
import plotly.express as px

# --- Configuração da Página ---
st.set_page_config(
    page_title="Salários na Área de Dados",
    page_icon="📊",
    layout="wide"
)

# --- Carregamento dos dados ---
@st.cache_data
def carregar_dados():
    url = "https://raw.githubusercontent.com/vqrca/dashboard_salarios_dados/main/dados-imersao-final.csv"
    return pd.read_csv(url)

df = carregar_dados()

# --- Título e Descrição ---
st.title("📊 Dashboard de Salários na Área de Dados")
st.markdown("Explore os dados salariais na área de dados nos últimos anos.")

# --- Barra Lateral (Filtros) ---
st.sidebar.header("🔍 Filtros")

# Dentro do 'with st.sidebar', usamos apenas 'st.multiselect'
with st.sidebar.expander("📅 Ano", expanded=True):
    anos_disponiveis = sorted(df['ano'].unique())
    # Removido o '.sidebar' daqui de dentro
    anos_selecionados = st.multiselect("Selecione o(s) ano(s):", anos_disponiveis, default=anos_disponiveis)

with st.sidebar.expander("👥 Senioridade"):
    senioridades_disponiveis = sorted(df['senioridade'].unique())
    senioridades_selecionadas = st.multiselect("Senioridade:", senioridades_disponiveis, default=senioridades_disponiveis)

with st.sidebar.expander("📄 Tipo de Contrato"):
    contratos_disponiveis = sorted(df['contrato'].unique())
    contratos_selecionados = st.multiselect("Contrato:", contratos_disponiveis, default=contratos_disponiveis)

with st.sidebar.expander("🏢 Tamanho da Empresa"):
    tamanhos_disponiveis = sorted(df['tamanho_empresa'].unique())
    tamanhos_selecionados = st.multiselect("Tamanho:", tamanhos_disponiveis, default=tamanhos_disponiveis)

# --- Filtragem ---
df_filtrado = df[
    (df['ano'].isin(anos_selecionados)) &
    (df['senioridade'].isin(senioridades_selecionadas)) &
    (df['contrato'].isin(contratos_selecionados)) &
    (df['tamanho_empresa'].isin(tamanhos_selecionados))
]

# --- Métricas ---
st.subheader("Métricas gerais (Salário anual em USD)")

if not df_filtrado.empty:
    salario_medio = df_filtrado['usd'].mean()
    salario_maximo = df_filtrado['usd'].max()
    total_registros = len(df_filtrado)
    cargo_mais_frequente = df_filtrado["cargo"].mode().get(0, "N/A")
else:
    salario_medio, salario_maximo, total_registros, cargo_mais_frequente = 0.0, 0.0, 0, "N/A"

col1, col2, col3, col4 = st.columns(4)
col1.metric("Salário médio", f"${salario_medio:,.0f}")
col2.metric("Salário máximo", f"${salario_maximo:,.0f}")
col3.metric("Total de registros", f"{total_registros:,}")
col4.metric("Cargo mais frequente", cargo_mais_frequente)

st.markdown("---")

# --- Gráficos ---
st.subheader("Gráficos")
col_graf1, col_graf2 = st.columns(2)

with col_graf1:
    if not df_filtrado.empty:
        top_cargos = df_filtrado.groupby('cargo')['usd'].mean().nlargest(10).sort_values(ascending=True).reset_index()
        fig_cargos = px.bar(
            top_cargos, x='usd', y='cargo', orientation='h',
            title="Top 10 cargos por salário médio",
            labels={'usd': 'USD', 'cargo': ''},
            color_discrete_sequence=["#082157"]
        )
        st.plotly_chart(fig_cargos, use_container_width=True)

with col_graf2:
    if not df_filtrado.empty:
        fig_hist = px.histogram(
            df_filtrado, x='usd', nbins=30,
            title="Distribuição de salários",
            color_discrete_sequence=["#082157"]
        )
        st.plotly_chart(fig_hist, use_container_width=True)

# --- Dados Detalhados ---
st.subheader("Dados Detalhados")
st.dataframe(df_filtrado)
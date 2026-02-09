import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Configuração da página (DEVE ser a primeira linha do Streamlit)
st.set_page_config(page_title="Salários na Área de Dados", page_icon="📊", layout="wide")

# 2. Carregamento dos dados com Cache
@st.cache_data
def carregar_dados():
    return pd.read_csv("https://raw.githubusercontent.com/vqrca/dashboard_salarios_dados/main/dados-imersao-final.csv")

df = carregar_dados()

# 3. Título
st.title("📊 Dashboard de Salários na Área de Dados")
st.markdown("Explore os dados salariais na área de dados nos últimos anos.")

# 4. Filtros (Correção: st.multiselect direto, sem .sidebar extra)
st.sidebar.header("🔍 Filtros")

# Ano
with st.sidebar.expander("📅 Ano", expanded=True):
    opcoes_anos = sorted(df['ano'].unique())
    sel_anos = st.multiselect("Selecione o(s) ano(s):", opcoes_anos, default=opcoes_anos)

# Senioridade
with st.sidebar.expander("👥 Senioridade"):
    opcoes_senior = sorted(df['senioridade'].unique())
    sel_senior = st.multiselect("Senioridade:", opcoes_senior, default=opcoes_senior)

# Contrato
with st.sidebar.expander("📄 Tipo de Contrato"):
    opcoes_contrato = sorted(df['contrato'].unique())
    sel_contrato = st.multiselect("Contrato:", opcoes_contrato, default=opcoes_contrato)

# Tamanho
with st.sidebar.expander("🏢 Tamanho da Empresa"):
    opcoes_tamanho = sorted(df['tamanho_empresa'].unique())
    sel_tamanho = st.multiselect("Tamanho:", opcoes_tamanho, default=opcoes_tamanho)

# 5. Aplicando Filtros
df_filtrado = df[
    (df['ano'].isin(sel_anos)) &
    (df['senioridade'].isin(sel_senior)) &
    (df['contrato'].isin(sel_contrato)) &
    (df['tamanho_empresa'].isin(sel_tamanho))
]

# 6. Métricas (KPIs)
st.subheader("Métricas gerais (Salário anual em USD)")
col1, col2, col3, col4 = st.columns(4)

if not df_filtrado.empty:
    media = df_filtrado['usd'].mean()
    maximo = df_filtrado['usd'].max()
    registros = df_filtrado.shape[0]
    # .mode() pode retornar vazio, usamos .get para evitar crash
    frequente = df_filtrado["cargo"].mode().get(0, "N/A")
    
    col1.metric("Média", f"${media:,.0f}")
    col2.metric("Máximo", f"${maximo:,.0f}")
    col3.metric("Registros", f"{registros:,}")
    col4.metric("Mais Frequente", frequente)
else:
    col1.metric("Média", "$0")
    col2.metric("Máximo", "$0")
    col3.metric("Registros", "0")
    col4.metric("Mais Frequente", "-")

st.markdown("---")

# 7. Gráficos
st.subheader("Gráficos")

# Se não houver dados, mostramos aviso e paramos a execução dos gráficos
if df_filtrado.empty:
    st.warning("⚠️ Nenhum dado encontrado com os filtros selecionados.")
else:
    col_graf1, col_graf2 = st.columns(2)
    
    with col_graf1:
        # Top 10 Cargos
        df_cargos = df_filtrado.groupby('cargo')['usd'].mean().nlargest(10).sort_values(ascending=True).reset_index()
        fig_cargos = px.bar(
            df_cargos, x='usd', y='cargo', orientation='h',
            title="Top 10 Cargos (Média Salarial)",
            color_discrete_sequence=["#082157"]
        )
        st.plotly_chart(fig_cargos, use_container_width=True)
        
    with col_graf2:
        # Histograma
        fig_hist = px.histogram(
            df_filtrado, x='usd', nbins=30,
            title="Distribuição de Salários",
            color_discrete_sequence=["#082157"]
        )
        st.plotly_chart(fig_hist, use_container_width=True)

    col_graf3, col_graf4 = st.columns(2)
    
    with col_graf3:
        # Pizza (Pie Chart)
        df_remoto = df_filtrado['remoto'].value_counts().reset_index()
        df_remoto.columns = ['tipo', 'qtd']
        fig_pizza = px.pie(
            df_remoto, names='tipo', values='qtd',
            title="Modelo de Trabalho", hole=0.5,
            color='tipo',
            color_discrete_map={"presencial": "#082157", "remoto": "#1E3A8A", "hibrido": "#9CA3AF"}
        )
        st.plotly_chart(fig_pizza, use_container_width=True)
        
    with col_graf4:
        # Mapa (Choropleth) - Filtramos apenas Data Scientist para não poluir
        df_mapa = df_filtrado[df_filtrado['cargo'] == 'Data Scientist']
        if not df_mapa.empty:
            df_paises = df_mapa.groupby('residencia_iso3')['usd'].mean().reset_index()
            fig_mapa = px.choropleth(
                df_paises, locations='residencia_iso3', color='usd',
                title="Média Salarial (Data Scientist) por País",
                color_continuous_scale=['#E5ECF6', '#C7D2FE', '#93C5FD', '#1E3A8A', '#082157']
            )
            st.plotly_chart(fig_mapa, use_container_width=True)
        else:
            st.info("O mapa exibe apenas dados de 'Data Scientist'. Selecione este cargo ou limpe os filtros.")

st.subheader("Base de Dados")
st.dataframe(df_filtrado)
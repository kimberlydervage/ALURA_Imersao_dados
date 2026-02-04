# 📊 Dashboard de Salários na Área de Dados

Este projeto consiste em um **dashboard interativo** desenvolvido em **Python** com **Streamlit**, com o objetivo de explorar e analisar dados salariais na área de Dados entre os anos de 2020 a 2025.

## 🔗 Demo
🔗 Em breve (deploy no Streamlit Cloud)

## 🔍 Funcionalidades
- Filtros dinâmicos por:
  - Ano
  - Senioridade
  - Tipo de contrato
  - Tamanho da empresa
- KPIs de salário médio, salário máximo e total de registros
- Gráficos interativos:
  - Top 10 cargos por salário médio
  - Distribuição de salários anuais
  - Proporção dos tipos de trabalho
  - Mapa de salário médio por país
- Tabela detalhada dos dados filtrados

## 🛠️ Tecnologias Utilizadas
- Python
- Pandas
- Streamlit
- Plotly

## ▶️ Como executar o projeto localmente

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py

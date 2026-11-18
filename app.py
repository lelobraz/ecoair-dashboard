import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(page_title="EcoAir - Regional", layout="wide")

df = pd.read_csv("data/processed/dados_tratados.csv")

st.title("🌱 EcoAir: Qualidade do Ar e Impacto na Saúde Pública")
st.markdown("Análise exploratória sobre os índices de poluição em **Jundiaí, Várzea Paulista, Campo Limpo Paulista, Caieiras, Franco da Rocha e Francisco Morato**.")

st.sidebar.header("Filtros do Painel")
regioes_disponiveis = ["Todas"] + list(df["Regiao"].unique())
regiao_selecionada = st.sidebar.selectbox("Selecione a Sub-região:", regioes_disponiveis)

max_pm25 = float(df["Poluente_PM25"].max())
min_pm25 = float(df["Poluente_PM25"].min())
if min_pm25 == max_pm25:
    min_pm25 = 0.0
limite_poluicao = st.sidebar.slider("Filtrar por nível máximo de PM2.5 (µg/m³):", min_pm25, max_pm25, max_pm25)

df_filtrado = df.copy()
if regiao_selecionada != "Todas":
    df_filtrado = df_filtrado[df_filtrado["Regiao"] == regiao_selecionada]
df_filtrado = df_filtrado[df_filtrado["Poluente_PM25"] <= limite_poluicao]

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Média de PM2.5 Geral", f"{df_filtrado['Poluente_PM25'].mean():.2f} µg/m³")
with col2:
    st.metric("Total de Casos Estimados", int(df_filtrado["Casos_Respiratorios_Est"].sum()))
with col3:
    st.metric("Cidades Analisadas", len(df_filtrado["Cidade"].unique()))

st.subheader("Análise Visual dos Dados")
aba1, aba2 = st.tabs(["Poluição por Cidade", "Correlação: Poluente vs Saúde"])

with aba1:
    fig_barra = px.bar(
        df_filtrado.groupby("Cidade").mean(numeric_only=True).reset_index(),
        x="Cidade", y="Poluente_NO2", title="Concentração Média de NO2 por Município (µg/m³)", color="Cidade"
    )
    st.plotly_chart(fig_barra, width="stretch")

with aba2:
    fig_dispersao = px.scatter(
        df_filtrado, x="Poluente_PM25", y="Casos_Respiratorios_Est", color="Cidade", size="Casos_Respiratorios_Est",
        title="Relação entre PM2.5 e Casos Respiratórios Estimados na Região"
    )
    st.plotly_chart(fig_dispersao, width="stretch")

st.subheader("📋 Visualização da Base de Dados Local (Processada)")
st.dataframe(df_filtrado, width="stretch")

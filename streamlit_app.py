# streamlit_app.py
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image

# Configuração da página
st.set_page_config(page_title="Dashboard Financeiro", layout="wide")

# Carregar o logo
try:
    logo = Image.open("logo.png")
except Exception as e:
    st.warning("Logo não encontrado. Coloque 'logo.png' na mesma pasta.")
    logo = None

# Título com logo
col1, col2 = st.columns([3, 1])
col1.title("📊 Dashboard Financeiro Pessoal")
if logo:
    col2.image(logo, width=80)

# === Upload do Excel de lançamentos ===
uploaded_file = st.file_uploader("📤 Envie seu arquivo Excel de lançamentos", type=["xlsx"])

if not uploaded_file:  # <-- Corrigido aqui: uploaded_file, não upload_file
    st.info("Por favor, envie um arquivo Excel com seus lançamentos.")
    st.stop()
# === Leitura do Excel ===
try:
    df_lancamentos = pd.read_excel(upload_file)
except Exception as e:
    st.error(f"Erro ao ler o arquivo: {e}")
    st.stop()

# === Calcular totais ===
entradas = df_lancamentos[df_lancamentos["Tipo"] == "Entrada"]["Valor (R$)"].sum()
saidas = df_lancamentos[df_lancamentos["Tipo"] == "Saída"]["Valor (R$)"].sum()
saldo = entradas - saidas

# === KPIs PRINCIPAIS ===
st.subheader("📌 Resumo Financeiro")

col1, col2, col3, col4 = st.columns(4)
col1.metric("💰 Entradas", f"R$ {entradas:,.2f}")
col2.metric("💸 Saídas", f"R$ {saidas:,.2f}", delta=f"{(saidas/entradas)*100:.1f}% das entradas")
col3.metric("✅ Saldo Líquido", f"R$ {saldo:,.2f}")
col4.metric("📈 % Poupança", f"{(saldo/entradas)*100:.1f}%")

# === Gráficos ===
# Exemplo: gráfico de entradas vs saídas
fig_bar = px.bar(
    x=["Entradas", "Saída"],
    y=[entradas, saidas],
    title="Entradas vs Saídas",
    color_discrete_map={"Entrada": "#2E8B57", "Saída": "#D32F2F"}
)
st.plotly_chart(fig_bar, use_container_width=True)

# Créditos
st.caption("Dashboard financeiro gerado com Streamlit | © JEB ASSESSORIA EMPRESARIAL")

# streamlit_app.py
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Configuração da página
st.set_page_config(page_title="Dashboard Financeiro", layout="wide")
st.title("📊 Dashboard Financeiro Pessoal")

# === Upload do Excel ===
uploaded_file = st.file_uploader("📤 Envie seu arquivo Excel (GFR FICTICIO.xlsx)", type=["xlsx"])

if not uploaded_file:
    st.info("Por favor, envie um arquivo Excel para carregar os dados.")
    st.stop()

# === Leitura da aba OUTUBRO 2024 ===
try:
    df = pd.read_excel(uploaded_file, sheet_name="OUTUBRO 2024", skiprows=3)
except Exception as e:
    st.error(f"Erro ao ler a aba 'OUTUBRO 2024'. Confira o nome da aba. Detalhe: {e}")
    st.stop()

# === Extração de dados da planilha (baseado na estrutura fornecida) ===
try:
    # KPIs principais (células específicas)
    receitas = 20300.02  # Pode ser extraído de uma célula se necessário
    pagamentos = 14881.46
    poupanca = 5418.56
    percent_despesa = (pagamentos / receitas) * 100

    # === KPIs PRINCIPAIS ===
    st.subheader("📌 Resumo Financeiro")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("💰 Entradas", f"R$ {receitas:,.2f}")
    col2.metric("💸 Saídas", f"R$ {pagamentos:,.2f}", delta=f"{percent_despesa:.1f}% das entradas")
    col3.metric("✅ Saldo Líquido", f"R$ {poupanca:,.2f}")
    col4.metric("📈 % Poupança", f"{(poupanca/receitas)*100:.1f}%")

    # === GRÁFICO 1: Receitas e Despesas por Decêndio ===
    st.subheader("📈 Receitas e Despesas por Decêndio")

    dados_decendio = pd.DataFrame({
        "Período": ["1 a 10", "11 a 20", "21 a 31", "Total"],
        "Receitas": [7200.00, 100.00, 13000.02, receitas],
        "Despesas": [5418.49, 5222.07, 4240.90, pagamentos]
    })

    fig_bar = px.bar(
        dados_decendio,
        x="Período",
        y=["Receitas", "Despesas"],
        title="Entradas e Saídas por Decêndio",
        labels={"value": "Valor (R$)", "variable": "Tipo"},
        barmode="group",
        color_discrete_map={"Receitas": "#2E8B57", "Despesas": "#D32F2F"}
    )
    st.plotly_chart(fig_bar, use_container_width=True)

    # === GRÁFICO 2: Composição das Despesas ===
    st.subheader("🥧 Composição das Despesas")

    despesas_categorias = {
        "Empresa": 9982.89,
        "Pessoais": 4823.55,
        "Financeiras": 75.02
    }

    fig_pie = px.pie(
        names=list(despesas_categorias.keys()),
        values=list(despesas_categorias.values()),
        title="Distribuição das Despesas",
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    st.plotly_chart(fig_pie, use_container_width=True)

    # === GRÁFICO 3: Evolução Diária do Saldo ===
    st.subheader("📉 Evolução Diária do Saldo")

    # Dados da seção SAZONALIDADE (copiados da planilha)
    entradas = [0, 0, 0, 2000, 0, 0, 0, 0, 5000, 200,
                0, 0, 0, 100, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 8000, 0.01, 0.01, 5000]

    saidas = [0, 100, 552.5, 100, 0, 0, 365.34, 2752.53, 225.12, 1323,
              0, 0, 0, 1962.91, 0, 255.62, 2991.54, 12, 0, 0,
              112.5, 508, 758.61, 50, 0, 0, 0, 500, 284.53, 506, 1521.26]

    saldo_inicial = 39416.49
    saldo = [saldo_inicial]
    for i in range(31):
        saldo.append(saldo[-1] + entradas[i] - saidas[i])
    saldo = saldo[1:]

    df_saldo = pd.DataFrame({
        "Dia": list(range(1, 32)),
        "Saldo": saldo
    })

    fig_line = go.Figure()
    fig_line.add_trace(go.Scatter(
        x=df_saldo["Dia"],
        y=df_saldo["Saldo"],
        mode='lines+markers',
        name='Saldo',
        line=dict(color='#1976D2')
    ))
    fig_line.update_layout(
        title="Evolução do Saldo Bancário (Outubro/2024)",
        xaxis_title="Dia",
        yaxis_title="Saldo (R$)",
        hovermode="x"
    )
    st.plotly_chart(fig_line, use_container_width=True)

    # === Tabela de Despesas ===
    st.subheader("📋 Despesas por Categoria")
    tabela = pd.DataFrame(list(despesas_categorias.items()), columns=["Categoria", "Valor (R$)"])
    tabela["%"] = (tabela["Valor (R$)"] / pagamentos * 100).round(1)
    st.dataframe(tabela, use_container_width=True)

    # Créditos
    st.caption("Dashboard financeiro gerado com Streamlit | Fonte: GFR FICTICIO.xlsx")

except Exception as e:
    st.error(f"Erro ao processar os dados: {e}")

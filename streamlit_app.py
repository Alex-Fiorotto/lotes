import streamlit as st
import pandas as pd

# Função para classificar os lotes
def classificar_lote(dias):
    if dias <= 3:
        return "Lote 0 a 3 dias"
    elif dias <= 7:
        return "Lote 4 a 7 dias"
    elif dias <= 14:
        return "Lote 8 a 14 dias"
    elif dias <= 29:
        return "Lote 15 a 29 dias"
    elif dias <= 44:
        return "Lote 30 a 44 dias"
    elif dias <= 60:
        return "Lote 45 a 60 dias"
    else:
        return "Lote 60+"

st.title("Análise de Ingressos por Lote de Dias de Antecedência")

uploaded_file = st.file_uploader("Envie o relatório de vendas (Excel)", type=["xlsx"])

if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)

    # Conversão de datas
    df["Data/Hora"] = pd.to_datetime(df["Data/Hora"], errors="coerce")
    df["Data/Hora - leitura"] = pd.to_datetime(df["Data/Hora - leitura"], errors="coerce")

    # Remover entradas inválidas
    df = df.dropna(subset=["Data/Hora", "Data/Hora - leitura", "Valor Pago"])

    # Cálculo dos dias de antecedência
    df["dias_antecedencia"] = (df["Data/Hora - leitura"] - df["Data/Hora"]).dt.days

    # Classificação dos lotes
    df["LOTE"] = df["dias_antecedencia"].apply(classificar_lote)

    # Agrupamento por lote
    resumo = df.groupby("LOTE").agg(
        QUANTIDADE=("Valor Pago", "count"),
        RECEITA=("Valor Pago", "sum")
    ).reset_index()

    # Ordenação dos lotes
    ordem_lotes = [
        "Lote 0 a 3 dias", "Lote 4 a 7 dias", "Lote 8 a 14 dias",
        "Lote 15 a 29 dias", "Lote 30 a 44 dias",
        "Lote 45 a 60 dias", "Lote 60+"
    ]
    resumo["ordem"] = resumo["LOTE"].apply(lambda x: ordem_lotes.index(x))
    resumo = resumo.sort_values("ordem").drop(columns="ordem")

    # Formatação contábil da receita
    resumo["RECEITA"] = resumo["RECEITA"].apply(lambda x: f"R$ {x:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))

    st.subheader("Resumo por Lote de Dias de Antecedência")
    st.dataframe(resumo)

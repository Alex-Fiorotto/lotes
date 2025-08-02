import streamlit as st
import pandas as pd
from datetime import datetime

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

st.title("Análise de Ingressos por Lote de Dias")

# Upload do arquivo
uploaded_file = st.file_uploader("Envie o relatório de vendas (Excel)", type=["xlsx"])

if uploaded_file is not None:
    # Leitura do Excel
    df = pd.read_excel(uploaded_file)

    # Verificação de colunas obrigatórias
    colunas_necessarias = {"DATA DA COMPRA", "DATA DO USO", "VALOR"}
    if not colunas_necessarias.issubset(df.columns):
        st.error("O arquivo precisa conter as colunas: DATA DA COMPRA, DATA DO USO e VALOR")
    else:
        # Conversão de datas
        df["DATA DA COMPRA"] = pd.to_datetime(df["DATA DA COMPRA"])
        df["DATA DO USO"] = pd.to_datetime(df["DATA DO USO"])

        # Cálculo dos dias de antecedência
        df["dias_antecedencia"] = (df["DATA DO USO"] - df["DATA DA COMPRA"]).dt.days

        # Classificação por lote
        df["LOTE"] = df["dias_antecedencia"].apply(classificar_lote)

        # Agrupamento por lote
        resumo = df.groupby("LOTE").agg(
            QUANTIDADE=("VALOR", "count"),
            VALOR_TOTAL=("VALOR", "sum")
        ).reset_index()

        resumo = resumo.sort_values(by="LOTE")  # Ordenação

        st.subheader("Resumo por Lote de Dias de Antecedência")
        st.dataframe(resumo)

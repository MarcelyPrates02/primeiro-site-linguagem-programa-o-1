# -*- coding: utf-8 -*-
# App: Planilha Financeira Completa com Streamlit

import streamlit as st
import pandas as pd
import plotly.express as px
import datetime as dt

# --------------------------
# Configurações da página
# --------------------------
st.set_page_config(page_title="Planilha Financeira", page_icon="💰", layout="wide")
st.title("💰 Planilha Financeira Simples")
st.write("Exemplo didático de site para controlar receitas e despesas com categorias e formas de pagamento.")

# --------------------------
# Constantes
# --------------------------
CATEGORIAS_PADRAO = ["Alimentação", "Transporte", "Saúde", "Lazer", "Educação", "Outros"]
FORMAS_PAGAMENTO = ["Cartão de Crédito", "Débito", "Dinheiro", "PIX"]

# --------------------------
# Inputs do usuário
# --------------------------
tipo_add = st.selectbox("Tipo", ["Entrada", "Saída"])
descricao_add = st.text_input("Descrição")
valor_add = st.number_input("Valor", min_value=0.0, step=1.0, format="%.2f")
categoria_add = st.selectbox("Categoria", options=CATEGORIAS_PADRAO)
forma_pagamento_add = st.selectbox("Forma de Pagamento", options=FORMAS_PAGAMENTO)

# --------------------------
# Botão para adicionar lançamento
# --------------------------
if st.button("Adicionar lançamento"):
    if "df" not in st.session_state:
        st.session_state.df = pd.DataFrame(columns=["Data","Tipo","Descrição","Categoria","Forma de Pagamento","Valor"])
    novo_lancamento = pd.DataFrame([{
        "Data": dt.date.today(),
        "Tipo": tipo_add,
        "Descrição": descricao_add,
        "Categoria": categoria_add,
        "Forma de Pagamento": forma_pagamento_add,
        "Valor": valor_add
    }])
    st.session_state.df = pd.concat([st.session_state.df, novo_lancamento], ignore_index=True)
    st.success("Lançamento adicionado!")

# --------------------------
# Mostrar tabela e gráficos
# --------------------------
if "df" in st.session_state and not st.session_state.df.empty:
    st.subheader("📄 Lançamentos")
    st.dataframe(st.session_state.df)

    # Gráfico Entradas x Saídas
    st.subheader("📊 Entradas vs Saídas")
    fig = px.pie(
        st.session_state.df,
        names="Tipo",
        values="Valor",
        hole=0.4,
        title="Proporção de Entradas e Saídas"
    )
    st.plotly_chart(fig)

    # Gráfico por Categoria
    st.subheader("📊 Gastos por Categoria")
    fig2 = px.pie(
        st.session_state.df,
        names="Categoria",
        values="Valor",
        hole=0.4,
        title="Distribuição por Categoria"
    )
    st.plotly_chart(fig2)

    # Gráfico por Forma de Pagamento
    st.subheader("📊 Distribuição por Forma de Pagamento")
    fig3 = px.pie(
        st.session_state.df,
        names="Forma de Pagamento",
        values="Valor",
        hole=0.4,
        title="Distribuição por Forma de Pagamento"
    )
    st.plotly_chart(fig3)

    # Saldo total
    saldo = st.session_state.df.apply(lambda row: row["Valor"] if row["Tipo"]=="Entrada" else -row["Valor"], axis=1).sum()
    st.metric("💵 Saldo Total", f"R$ {saldo:,.2f}")

    # --------------------------
    # --------------------------
    # Excluir lançamentos (versão melhorada)
    # --------------------------
    if "df" in st.session_state and not st.session_state.df.empty:
        st.subheader("❌ Excluir Lançamentos")
        st.write("Selecione os lançamentos que deseja excluir:")

        # Criar opções com índice e resumo do lançamento
        opcoes = [
            f'{i} | {row["Data"]} | {row["Tipo"]} | {row["Descrição"]} | {row["Categoria"]} | {row["Forma de Pagamento"]} | R$ {row["Valor"]:.2f}'
            for i, row in st.session_state.df.iterrows()
        ]

        # Selecionar um ou mais lançamentos para excluir
        selecionar_para_excluir = st.multiselect("Escolha os lançamentos", options=opcoes)

        if st.button("Excluir selecionados"):
            if selecionar_para_excluir:
                indices_excluir = [int(op.split(" | ")[0]) for op in selecionar_para_excluir]
                st.session_state.df.drop(indices_excluir, inplace=True)
                st.session_state.df.reset_index(drop=True, inplace=True)
                st.success(f"{len(indices_excluir)} lançamento(s) excluído(s) com sucesso!")



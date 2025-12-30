import pandas as pd
import streamlit as st
from streamlit_gsheets import GSheetsConnection
import plotly.express as px


# conexão planilha
conn = st.connection("gsheets", type=GSheetsConnection)

df = conn.read(worksheet="Página1", ttl=0)

acao = st.sidebar.selectbox('Analisar:', ('Venda', 'Compra'))

col1, col2, col3 = st.columns([0.5, 0.25, 0.25])

if acao == 'Venda':
    
    df = df[df['tipo_mov'] == 'Venda']

    col1.markdown('# Vendas Realizadas 💸')

    valor_venda_total = f'R$ {df['total'].sum():.2f}'
    col2.metric('Valor Total de vendas realizadas', valor_venda_total)

    produto_mais_vendido = df['produto'].value_counts().index[0]
    col3.metric('Produto mais vendido', produto_mais_vendido)


elif acao == 'Compra':

    df = df[df['tipo_mov'] == 'Compra']

    col1.markdown('# Compras Realizadas 🛒')

    valor_compras_total = f'R$ {df['total'].sum():.2f}'
    col2.metric('Valor Total de compras realizadas', valor_compras_total)

    produto_mais_comprado = df['produto'].value_counts().index[0]
    col3.metric('Produto mais comprado', produto_mais_comprado)

st.divider()

col21, col22, col23 = st.columns([0.5, 0.25, 0.25])

col21.text('Gráfico Geral')
metrica_21 = st.sidebar.selectbox('Gráfico Geral:', ['produto', 'pagamento'])
fig_pizza = px.pie(df, names= metrica_21, values='total')
col21.plotly_chart(fig_pizza)

col22.text('Gráfico dos Meis')
metrica_22 = st.sidebar.selectbox('Gráfico dos Meis:', ['subproduto', 'modelo'])
df_22 = df[(df[df['produto'] == 'Mel']) & (df[metrica_22].notna())]
fig_pizza = px.pie(df_22, names= metrica_22, values='total')
col22.plotly_chart(fig_pizza)

col23.text('Gráfico dos Sabonetes')
df_23 = df[(df[df['produto'] == 'Sabonete']) & (df['subproduto'].notna())]
fig_pizza = px.pie(df_23, names='subproduto', values='total')
col23.plotly_chart(fig_pizza)

st.divider()

# Ideias

'''

alterar o produto mais vendido/comprado para quantos % a compra/venda representa das operações
seria bom ter um gráfico que mostra compra e venda (em pizza)

grafico 1: produto, pagamento
grafico 2 - Mel: subprouto 
grafico 3 - Sabonete: modelo


total_vendas = df[df['tipo_mov'] == 'Venda']['total'].sum()
total_compras = df[df['tipo_mov'] == 'Compra']['total'].sum()

if total_vendas < total_compras:
    print(f'Situação do mês: PREZUÍZO de R$ {total_vendas - total_compras:.2f}')

elif total_vendas > total_compras:
    print(f'Situação do mês: LUCRO de R$ {total_vendas - total_compras:.2f}')

else:
    print('Ponto de Equilíbrio! Vendas iguais as Compras')
    
produtos_pizza = (df['produto'].value_counts(1) * 100).round(2).to_dict()

'''
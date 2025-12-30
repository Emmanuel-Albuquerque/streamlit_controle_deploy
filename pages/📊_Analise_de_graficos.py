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


    perc_venda = f'{(df[df['tipo_mov'] == 'Venda']['total'].sum() / df['total'].sum()) * 100:.2f}%'
    col3.metric(r'As vendas representam % de todas as operaçãoes', perc_venda)


elif acao == 'Compra':

    df = df[df['tipo_mov'] == 'Compra']

    col1.markdown('# Compras Realizadas 🛒')

    valor_compras_total = f'R$ {df['total'].sum():.2f}'
    col2.metric('Valor Total de compras realizadas', valor_compras_total)

    produto_mais_comprado = df['produto'].value_counts().index[0]
    col3.metric('Produto mais comprado', produto_mais_comprado)

st.divider()

paleta_mel = [
    "#FFD966",  # amarelo mel claro
    "#F4B183",  # dourado
    "#C55A11",  # âmbar
    "#8B5A2B",  # marrom mel
    "#FFF2CC",  # quase branco
]

col21, col22, col23 = st.columns([0.33, 0.33, 0.33])

col21.subheader('Gráfico Geral')
metrica_21 = st.sidebar.selectbox('Gráfico Geral:', ['produto', 'pagamento'])
fig_pizza = px.pie(df, names= metrica_21, values='total', color_discrete_sequence=paleta_mel)
col21.plotly_chart(fig_pizza, use_container_width=True)

col22.subheader('Gráfico dos Meis')
metrica_22 = st.sidebar.selectbox('Gráfico dos Meis:', ['subproduto', 'modelo'])
df_22 = df[(df['produto'] == 'Mel') & (df[metrica_22].notna())]
fig_pizza = px.pie(df_22, names= metrica_22, values='total', color_discrete_sequence=paleta_mel)
col22.plotly_chart(fig_pizza, use_container_width=True)

col23.subheader('Gráfico dos Sabonetes')
df_23 = df[(df['produto'] == 'Sabonete') & (df['subproduto'].notna())]
fig_pizza = px.pie(df_23, names='subproduto', values='total', color_discrete_sequence=paleta_mel)
col23.plotly_chart(fig_pizza, use_container_width=True)

st.divider()

# Ideias

'''

alterar o produto mais vendido/comprado para quantos % a compra/venda representa das operações
seria bom ter um gráfico que mostra compra e venda (em pizza)


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
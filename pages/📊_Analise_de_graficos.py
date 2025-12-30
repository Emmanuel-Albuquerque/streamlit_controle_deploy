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
    
    col1.markdown('# Vendas Realizadas 🛒')

    valor_venda_total = f'R$ {df[df['tipo_mov'] == 'Venda']['total'].sum():.2f}'
    col2.metric('Valor Total de vendas realizadas', valor_venda_total)

    produto_mais_vendido = df[(df['tipo_mov'] == 'Venda')]['produto'].value_counts().index[0]
    col3.metric('Produto mais vendido', produto_mais_vendido)


elif acao == 'Compra':

    col1.markdown('# Compras Realizadas 💸')

    valor_compras_total = f'R$ {df[df['tipo_mov'] == 'Compra']['total'].sum():.2f}'
    col2.metric('Valor Total de compras realizadas', valor_compras_total)

    produto_mais_comprado = df[df['tipo_mov'] == 'Compra']['produto'].value_counts().index[0]
    col3.metric('Produto mais comprado', produto_mais_comprado)

st.divider()

col21, col22 = st.columns([0.5, 0.5])

metrica = st.sidebar.selectbox('Métrica do gráfico de pizza', ['Produto', 'Subproduto', 'Modelo', 'Pagamento'])

fig_pizza = px.pie(df, names=metrica, values='total')
col21.plotly_chart(fig_pizza)

st.divider()

# Ideias

'''

separar se é compra ou venda
no gráfico pegar apenas os que tem subprodutos, sem o 'Null'


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
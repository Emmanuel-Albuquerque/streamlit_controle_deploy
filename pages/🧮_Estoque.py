import pandas as pd
import streamlit as st
from streamlit_gsheets import GSheetsConnection
import plotly.express as px

#cores
paleta_mel = [
    "#FFD966",  # amarelo mel claro
    "#F4B183",  # dourado
    "#C55A11",  # âmbar
    "#8B5A2B",  # marrom mel
    "#FFF2CC",  # quase branco
]



# conexão planilha
conn = st.connection("gsheets", type=GSheetsConnection)

df = conn.read(worksheet="Página1", ttl=0)

st.title('Segue o seu estoque atual por produto 🧮')

st.divider()



produto = st.sidebar.selectbox('Selecione o Produto:',
                             (
                               'Mel', 
                               'Sabonete', 
                               'Própolis', 
                               'Spray Bucal', 
                               'Pomada', 
                               'Pomada Apitoxina', 
                               'Protetor Labial', 
                               'Xarope', 
                               'Favo de Mel', 
                               'Shampoo', 
                               'Vela', 
                               'Pólen', 
                               'Gengibre Cristalizado', 
                               'Sache'
                             ))

if produto == 'Mel':

    col1, col2 = st.columns([0.25, 0.75])

    subproduto = st.sidebar.selectbox('Selecione o Tipo:',
                                      (
                                        'Aroeira', 
                                        'Assa-peixe', 
                                        'Cipó-uva', 
                                        'Eucalipto', 
                                        'Silvestre', 
                                        'Cristalizado',
                                        'Misto'  
                                      ))
    
    df = df[df['subproduto'] == subproduto]

    # o gráfico mostra quais os modelo do mel selecionado ainda estão em estoque
    col2.subheader(f'Gráfico Detalhado de {subproduto}')
    fig_pizza = px.pie(df, names='modelo', values='quantidade', color_discrete_sequence=paleta_mel)
    fig_pizza.update_traces(textinfo = 'percent+value', textposition='inside')
    col2.plotly_chart(fig_pizza, use_container_width=True)

else:
    col1, col2 = st.columns([0.5, 0.5])
    df = df[df['produto'] == produto]

    df_venda = df[df['tipo_mov'] == 'Venda']
    fig_pizza = px.pie(df_venda, names='pagamento', values='total', color_discrete_sequence=paleta_mel)
    fig_pizza.update_traces(textinfo = 'percent+value', textposition='inside')
    col2.subheader('Vendas Realizadas no:')
    col2.plotly_chart(fig_pizza, use_container_width=True)

compra = sum(df[df['tipo_mov'] == 'Compra']['quantidade'].values)
venda = sum(df[df['tipo_mov'] == 'Venda']['quantidade'].values)
estoque = compra - venda

col1.metric('Quantidade em estoque', f"{estoque:.0f} unidades")





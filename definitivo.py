import pandas as pd
from datetime import date
import streamlit as st
from streamlit_gsheets import GSheetsConnection


# Conexão oficial
conn = st.connection("gsheets", type=GSheetsConnection)

# Lê dados
df = conn.read()

st.set_page_config(page_title='Controle', layout='wide')

st.title('Bem vindo Guillen!🍯🐝')

acao = st.selectbox('Qual das opções a seguir deseja registrar?', ('Venda', 'Compra'))

produto = st.selectbox('Qual o seu produto?', ('Mel', 'Sabonete', 'Própolis', 'Spray Bucal', 'Pomada Apitoxina', 'Protetor Labial', 'Xarope', 'Favo de Mel', 'Shampoo'))

modelo = None
subproduto = None
if produto == 'Mel':
    subproduto = st.selectbox('Qual o tipo do Mel?', ('Aroeira', 'Assa-peixe', 'Cipó-uva', 'Eucalipto', 'Silvestre'))

    modelo = st.selectbox('Qual o modelo do Mel?', ('1 kg', '500g', '300g', 'Vidro 850g', ' Vidro 500g', 'Vidro 300g', 'Vidro Cristalizado 850g', 'Vidro Cristalizado 500g', 'Vidro Cristalizado 300g'))

elif produto == 'Sabonete':
    subproduto = st.selectbox('Qual o tipo do Sabonete?', ('Açafrão', 'Babosa e Alecrim', 'Barbatimão', 'Mel e Própolis', 'Líquido'))

quantidade = st.number_input('Escreva a seguir a quantidade:', min_value=1)

valor_unit = st.number_input('Qual o valor de cada unidade? (ex: 16.99)')

pagamento = st.selectbox('Qual foi o meio de pagamento?', ('Cartão', 'Pix', 'Dinheiro', 'Outro'))

if st.button('Registrar ação'):

    nova_linha = pd.DataFrame([[
        str(date.today()),
        acao,
        produto,
        subproduto,
        modelo,
        quantidade,
        valor_unit,
        pagamento,
        (quantidade * valor_unit)
    ]], columns= df.columns)
    
    conn.append(worksheet="Sheet1", data=nova_linha)

    st.success(f'Movimentação registrada com sucesso!')


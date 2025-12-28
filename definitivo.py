import pandas as pd
from datetime import date
import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

creds = ServiceAccountCredentials.from_json_keyfile_name("teste-pai-482601-49416dfc2658.json", scope)
client = gspread.authorize(creds)

sheet = client.open_by_key("1crCeP1HmAFvc8SkU3xLyK70wsHRwvtcfd3I0MrBXHnQ").sheet1

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

    sheet.append_row([
        str(date.today()),
        acao,
        produto,
        subproduto,
        modelo,
        quantidade,
        valor_unit,
        pagamento,
        (quantidade * valor_unit)
    ])

    st.success(f'Movimentação registrada com sucesso!')

    

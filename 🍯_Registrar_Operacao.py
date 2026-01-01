import pandas as pd
from datetime import date
import streamlit as st
from streamlit_gsheets import GSheetsConnection


# Conexão oficial
conn = st.connection("gsheets", type=GSheetsConnection)

st.set_page_config(page_title='Controle', page_icon='📝', layout='wide')
st.title('Bem vindo Guillen!🍯🐝')

st.divider()

acao = st.selectbox('Qual das opções a seguir deseja registrar?', ('Venda', 'Compra', 'Outros'))

# atribuindo valores para evitar erro
produto = None
modelo = None
subproduto = None
observacao = None

if acao == 'Outros':
    observacao = st.text_input('Qual foi o gasto?').lower()
    if observacao == '':
        observacao = 'desconhecido'

    valor_unit = st.number_input('Qual o valor do gasto? (ex: 199.99)')
    quantidade = 1

else:
    produto = st.selectbox('Qual o seu produto?', ('Mel', 'Sabonete', 'Própolis', 'Spray Bucal', 'Pomada Apitoxina', 'Protetor Labial', 'Xarope', 'Favo de Mel', 'Shampoo'))

    if produto == 'Mel':
        subproduto = st.selectbox('Qual o tipo do Mel?', ('Aroeira', 'Assa-peixe', 'Cipó-uva', 'Eucalipto', 'Silvestre'))

        modelo = st.selectbox('Qual o modelo do Mel?', ('1 kg', '500g', '300g', 'Vidro 850g', ' Vidro 500g', 'Vidro 300g', 'Vidro Cristalizado 850g', 'Vidro Cristalizado 500g', 'Vidro Cristalizado 300g'))

    elif produto == 'Sabonete':
        subproduto = st.selectbox('Qual o tipo do Sabonete?', ('Açafrão', 'Babosa e Alecrim', 'Barbatimão', 'Mel e Própolis', 'Líquido'))

    quantidade = st.number_input('Escreva a seguir a quantidade:', min_value=1)

    valor_unit = st.number_input('Qual o valor de cada unidade? (ex: 16.99)')

pagamento = st.selectbox('Qual foi o meio de pagamento?', ('Cartão', 'Pix', 'Dinheiro', 'Outro'))

if st.button('Registrar ação'):

    nova_linha = pd.DataFrame([{
        'data': str(date.today()),
        'tipo_mov': acao,
        'produto': produto,
        'subproduto': subproduto,
        'modelo': modelo,
        'observacao': observacao, 
        'quantidade': quantidade,
        'valor_unit': valor_unit,
        'pagamento': pagamento,
        'total': (quantidade * valor_unit)
    }])
    
    # Lê a planilha atual
    df = conn.read(worksheet="Página1", ttl=0)
    
    # Junta com a nova linha
    df = pd.concat([df, nova_linha], ignore_index=True)

    # Atualiza tudo novamente
    conn.update(worksheet="Página1", data=df)

    st.success(f'Movimentação registrada com sucesso!')



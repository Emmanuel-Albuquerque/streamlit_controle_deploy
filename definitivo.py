import streamlit as st
import pandas as pd
from datetime import date
from google.oauth2 import service_account
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

creds = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=SCOPES
)

service = build("sheets", "v4", credentials=creds)

SPREADSHEET_ID = "1crCeP1HmAFvc8SkU3xLyK70wsHRwvtcfd3I0MrBXHnQ"
RANGE = "A:I"

result = service.spreadsheets().values().get(
    spreadsheetId=SPREADSHEET_ID,
    range=RANGE
).execute()

values = result.get("values", [])

df = pd.DataFrame(values[1:], columns=values[0]) if values else pd.DataFrame()

st.set_page_config(page_title='Controle', layout='wide')
st.title("Bem vindo Guillen 🍯🐝")

acao = st.selectbox("Ação", ["Venda","Compra"])
produto = st.selectbox("Produto", ["Mel","Sabonete","Própolis","Spray Bucal"])
quantidade = st.number_input("Quantidade", min_value=1)
valor_unit = st.number_input("Valor Unitário", format="%.2f")
pagamento = st.selectbox("Pagamento", ["Pix","Cartão","Dinheiro"])

if st.button("Registrar"):
    nova_linha = [
        str(date.today()),
        acao,
        produto,
        quantidade,
        valor_unit,
        pagamento,
        quantidade * valor_unit
    ]

    service.spreadsheets().values().append(
        spreadsheetId=SPREADSHEET_ID,
        range=RANGE,
        valueInputOption="USER_ENTERED",
        body={"values":[nova_linha]}
    ).execute()

    st.success("Registro gravado com sucesso!")

st.dataframe(df)

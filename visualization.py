import streamlit as st

registrar_movi = st.Page('main.py', title="Registrar Movimentação", icon=":material/add_circle:")
df_page = st.Page('page2.py', title='Base de dados', icon=':material/dataset:')

pg = st.navigation([registrar_movi, df_page])
st.set_page_config(page_title="Controle", page_icon=":material/edit:")
pg.run()
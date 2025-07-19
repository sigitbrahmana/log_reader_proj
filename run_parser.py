import streamlit as st
from modules import app_optlog, app_log_parser

# Sembunyikan menu dan footer
hide_streamlit_style = """
            <style>
            
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

st.set_page_config(page_title="Log Tools", layout="wide")
st.sidebar.title("🔧 Menu")

# Menu navigasi
app_choice = st.sidebar.radio("Pilih Tools:", ["CR LOG Parser", "OPTLOG Parser"])

# Panggil halaman berdasarkan pilihan
if app_choice == "CR LOG Parser":
    app_log_parser.main()
elif app_choice == "OPTLOG Parser":
    app_optlog.main()

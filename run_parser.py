import streamlit as st
from modules import app_optlog, app_log_parser

st.set_page_config(page_title="Log Tools", layout="wide")
st.sidebar.title("🔧 Menu")

# Menu navigasi
app_choice = st.sidebar.radio("Pilih Aplikasi:", ["CR LOG Parser", "OPTLOG Parser"])

# Panggil halaman berdasarkan pilihan
if app_choice == "CR LOG Parser":
    app_log_parser.main()
elif app_choice == "OPTLOG Parser":
    app_optlog.main()

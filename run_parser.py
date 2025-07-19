import streamlit as st
from modules import app_optlog, app_log_parser

# Sembunyikan menu dan footer
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: visible;}
            footer {visibility: hidden;}
            header {visibility: visible;}
            
            /* Sembunyikan badge GitHub/Fork di pojok kanan atas */
            a[href*="github.com"] {
                        display: none !important;
            }
            .st-emotion-cache-6qob1r.e1vs0wn30 { 
                        display: none !important; 
            }
            [data-testid="stDecoration"] {
                        display: none !important;
            }
            </style>
"""

st.markdown(hide_streamlit_style, unsafe_allow_html=True)

st.set_page_config(page_title="Log Tools", layout="wide")
st.sidebar.title("🔧 Menu")

# Menu navigasi
# app_choice = st.sidebar.radio("Pilih Tools:", ["CR LOG Parser", "OPTLOG Parser"])
app_choice = st.selectbox("Pilih Tools:", ["CR LOG Parser", "OPTLOG Parser"])

# Panggil halaman berdasarkan pilihan
if app_choice == "CR LOG Parser":
    app_log_parser.main()
elif app_choice == "OPTLOG Parser":
    app_optlog.main()

import streamlit as st
from modules import app_optlog, app_log_parser

# Sembunyikan menu dan footer
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            
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

# Gambar QRIS di sidebar
with st.sidebar:
    st.image(
        "https://raw.githubusercontent.com/sigitbrahmana/log_reader_proj/refs/heads/mainan/Capture.JPG",
        use_container_width=True
    )
    
    st.markdown(
        """
        <div style='text-align: center; margin-top: 10px;'>
            <span style='font-size: 20px; font-weight: bold; color: white; background-color: black; padding: 6px 12px; border-radius: 8px; display: inline-block;'>
                Scan QRIS untuk nraktir ngopi ☕
            </span>
        </div>
        """,
        unsafe_allow_html=True
    )
# Menu navigasi
app_choice = st.selectbox("Pilih Tools:", ["CR LOG Parser", "OPTLOG Parser"])

# Panggil halaman berdasarkan pilihan
if app_choice == "CR LOG Parser":
    app_log_parser.main()
elif app_choice == "OPTLOG Parser":
    app_optlog.main()

import streamlit as st
from modules import app_optlog, app_log_parser

# Sembunyikan menu dan footer
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            
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
# st.sidebar.title("🔧 Menu")

# Menu navigasi
 # Sisipkan gambar yang melayang di pojok kanan atas
st.markdown(
    """
    <style>
    .floating-image-container {
        position: fixed;
        top: 10px;
        right: 10px;
        text-align: center;
        z-index: 100;
    }
    .floating-image-container img {
        width: 100px;
        border-radius: 8px;
        box-shadow: 0px 0px 10px rgba(0,0,0,0.3);
    }
    .floating-image-container p {
        margin: 5px 0 0 0;
        font-size: 12px;
        color: black;
        font-weight: bold;
    }
    </style>
    <img src="https://images-loyalty.ovo.id/public/merchant/08/55/3325508.png?ver=1652848671" class="floating-image">
    """,
    unsafe_allow_html=True
)
# app_choice = st.sidebar.radio("Pilih Tools:", ["CR LOG Parser", "OPTLOG Parser"])
app_choice = st.selectbox("Pilih Tools:", ["CR LOG Parser", "OPTLOG Parser"])

# Panggil halaman berdasarkan pilihan
if app_choice == "CR LOG Parser":
    app_log_parser.main()
elif app_choice == "OPTLOG Parser":
    app_optlog.main()

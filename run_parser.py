import streamlit as st
from modules import app_optlog, app_log_parser

# Sembunyikan menu dan footer Streamlit default
hide_streamlit_style = """
    <style>
    #MainMenu, footer, header {
        visibility: hidden;
    }
    a[href*="github.com"], 
    .st-emotion-cache-6qob1r.e1vs0wn30, 
    [data-testid="stDecoration"] {
        display: none !important;
    }
    </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

st.set_page_config(page_title="Log Tools", layout="wide")

# Floating Image QRIS
st.markdown(
    """
    <style>
    .floating-image-container {
        position: fixed;
        bottom: 10px;
        left: 10px;
        text-align: center;
        z-index: 9998;
    }
    .floating-image-container img {
        width: 150px;
        height: auto;
        border-radius: 8px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    .floating-image-container p {
        margin: 4px 0 0 0;
        font-size: 14px;
        font-weight: bold;
        color: #fff;
        background-color: rgba(0, 0, 0, 0.7);
        padding: 4px 8px;
        border-radius: 4px;
    }

    .floating-button {
        position: fixed;
        bottom: 170px;
        left: 20px;
        z-index: 9999;
    }
    </style>

    <div class="floating-image-container">
        <img src="https://raw.githubusercontent.com/sigitbrahmana/log_reader_proj/refs/heads/mainan/Capture.JPG" alt="QRIS Traktir Kopi">
        <p>Scan QRIS untuk traktir ngopi ☕</p>
    </div>
    """,
    unsafe_allow_html=True
)

# Tombol untuk menyembunyikan/memunculkan selectbox
with st.sidebar:
    st.markdown("### ⚙️ Tampilan")
    toggle = st.checkbox("Tampilkan Pilihan Tools", value=True)

# Elemen yang bisa di-hide
if toggle:
    app_choice = st.selectbox("Pilih Tools:", ["CR LOG Parser", "OPTLOG Parser"])
    if app_choice == "CR LOG Parser":
        app_log_parser.main()
    elif app_choice == "OPTLOG Parser":
        app_optlog.main()

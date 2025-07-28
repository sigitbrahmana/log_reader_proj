import streamlit as st
from modules import app_optlog, app_log_parser, bikingcell

# Atur halaman
st.set_page_config(page_title="Log Tools", layout="wide")

# Sembunyikan elemen UI yang tidak diinginkan
hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    a[href*="github.com"] {
        display: none !important;
    }
    /* Hindari sembunyikan elemen penting sidebar */
    /* .st-emotion-cache-6qob1r.e1vs0wn30 {
        display: none !important;
    }
    [data-testid="stDecoration"] {
        display: none !important;
    } */
    </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    # Gambar QRIS
    st.markdown(
        """
        <div style='text-align: center;'>
            <img src='https://raw.githubusercontent.com/sigitbrahmana/log_reader_proj/refs/heads/mainan/my code.png' 
                 style='width: 60%;' />
            <span style='font-size: 18px; font-weight: bold; color: white; background-color: black; padding: 6px 12px; border-radius: 8px; display: inline-block;'>
                Scan QRIS traktir creator kopi ☕
            </span>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<br><br>", unsafe_allow_html=True)

    # Info fitur baru
    st.markdown(
        """
        <span style='font-size: 12px; font-weight: bold; color: red; background-color: white; padding: 6px 12px; border-radius: 8px; display: inline-block;'>
            Telah ditambahkan Create Gcell (beta) di menu "Pilih Tools"<br><br>
            Catatan:<br>
            Gunakan untuk membuat Gcell di area kecil agar prosesnya tidak lama, misalkan filter engpar terlebih dahulu untuk area Kecamatan Tebet.<br><br>
            Informasikan jika menemukan bugs. Thx!
        </span>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<br>", unsafe_allow_html=True)

    # Menu navigasi di sidebar
    app_choice = st.selectbox("Pilih Tools:", ["CR LOG Parser", "OPTLOG Parser", "Create Gcell"])

# Panggil halaman berdasarkan pilihan
if app_choice == "CR LOG Parser":
    app_log_parser.main()
elif app_choice == "OPTLOG Parser":
    app_optlog.main()
elif app_choice == "Create Gcell":
    bikingcell.main()

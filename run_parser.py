import streamlit as st
from modules import app_optlog, app_log_parser, bikingcell

# Konfigurasi halaman
st.set_page_config(page_title="Log Tools", layout="wide")

# Sembunyikan elemen-elemen Streamlit standar
hide_streamlit_style = """
    <style>
        #MainMenu, footer, header {visibility: hidden;}
        a[href*="github.com"] {display: none !important;}
        .st-emotion-cache-6qob1r.e1vs0wn30 {display: none !important;}
        [data-testid="stDecoration"] {display: none !important;}
    </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    # QRIS image dan teks
    st.markdown(
        """
        <div style='text-align: center;'>
            <img src='https://raw.githubusercontent.com/sigitbrahmana/log_reader_proj/refs/heads/mainan/my%20code.png' 
                 style='width: 60%; margin-bottom: 10px;' />
            <div style='font-size: 16px; font-weight: bold; color: white; background-color: black; padding: 6px 12px; border-radius: 8px; display: inline-block;'>
                Scan QRIS traktir creator kopi ☕
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Spacer agar teks berada di bawah
    st.markdown("<br><br>", unsafe_allow_html=True)

    # Info tambahan (perubahan fitur)
    st.markdown(
        """
        <div style='font-size: 12px; font-weight: bold; color: red; background-color: white; padding: 6px 12px; border-radius: 8px;'>
            Telah ditambahkan fitur <b>Create Gcell (beta)</b> di menu "Pilih Tools"<br><br>
            <u>Catatan:</u><br>
            Gunakan untuk membuat Gcell di area kecil agar proses cepat.<br>
            Contoh: filter <i>engpar</i> terlebih dahulu untuk area Kecamatan Tebet.<br><br>
            Silakan informasikan jika menemukan bugs. Terima kasih!
        </div>
        """,
        unsafe_allow_html=True
    )

# Menu pilihan tools
app_choice = st.selectbox("Pilih Tools:", ["CR LOG Parser", "OPTLOG Parser", "Create Gcell"])

# Panggil modul sesuai pilihan
if app_choice == "CR LOG Parser":
    app_log_parser.main()
elif app_choice == "OPTLOG Parser":
    app_optlog.main()
elif app_choice == "Create Gcell":
    bikingcell.main()

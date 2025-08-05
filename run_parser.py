import streamlit as st
from modules import app_optlog, app_log_parser, bikingcell

# Konfigurasi halaman
# Menambahkan initial_sidebar_state="expanded" untuk memastikan sidebar selalu terbuka
st.set_page_config(page_title="Log Tools", layout="wide", initial_sidebar_state="expanded")

# Sembunyikan elemen-elemen Streamlit standar yang tidak diinginkan
# Aturan CSS ini telah disederhanakan agar tidak menyembunyikan sidebar
hide_streamlit_style = """
    <style>
        #MainMenu {visibility: hidden;} /* Menyembunyikan menu utama Streamlit */
        footer {visibility: hidden;} /* Menyembunyikan footer "Made with Streamlit" */
        /* Menyembunyikan tautan atau tombol yang mengarah ke GitHub, termasuk tombol Deploy */
        a[href*="github.com"] {display: none !important;}
        [data-testid="stDeployButton"] {
            display: none !important;
        }
        /* Menyembunyikan tombol collapse sidebar */
        [data-testid="stSidebarCollapseButton"] {
            display: none !important;
        }
        /* Menyembunyikan header utama Streamlit */
        [data-testid="stHeader"] {
            display: none !important;
        }
    </style>
"""

st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    # Gambar QRIS dan teks untuk traktir creator
    st.markdown(
        """
        <div style='text-align: center;'>
            <img src='https://raw.githubusercontent.com/sigitbrahmana/log_reader_proj/refs/heads/mainan/Capture.jpeg'
                 style='width: 60%; margin-bottom: 10px;' />
            <div style='font-size: 16px; font-weight: bold; color: white; background-color: black; padding: 6px 12px; border-radius: 8px; display: inline-block;'>
                QRIS Ngopi ☕
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Spacer untuk penataan
    st.markdown("<br><br>", unsafe_allow_html=True)

    # Informasi tambahan atau pengumuman fitur baru
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

# Menu pilihan tools utama
app_choice = st.selectbox("Pilih Tools:", ["CR LOG Parser", "OPTLOG Parser", "Create Gcell"])

# Memanggil modul yang sesuai berdasarkan pilihan pengguna
if app_choice == "CR LOG Parser":
    app_log_parser.main()
elif app_choice == "OPTLOG Parser":
    app_optlog.main()
elif app_choice == "Create Gcell":
    bikingcell.main()

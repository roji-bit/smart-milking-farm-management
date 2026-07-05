import streamlit as st
from datetime import datetime
import pytz

# =========================================================
# 1. PENGATURAN HALAMAN & CSS REVISI (JUDUL NAIK & HAPUS LOGO)
# =========================================================
st.set_page_config(
    page_title="Milking Time Report",
    page_icon="🥛",
    layout="centered"
)

# Injeksi CSS untuk merapikan tampilan sesuai request Bapak
st.markdown("""
    <style>
        /* Memicu container utama agar mepet ke atas (Judul Naik) */
        .block-container {
            padding-top: 1rem !important;
            padding-bottom: 0rem !important;
            max-width: 500px !important; /* Pas untuk layar HP */
        }
        
        /* Menghilangkan footer 'Hosted with Streamlit' */
        footer {
            visibility: hidden !important;
            height: 0px !important;
            padding: 0px !important;
        }
        
        /* Menghilangkan tombol menu bulat ungu & header atas bawaan */
        header, #MainMenu, footer {
            display: none !important;
        }
        
        /* Merapikan kartu judul hijau agar terlihat modern di HP */
        .header-box {
            background: linear-gradient(135deg, #11998e, #38ef7d);
            color: white;
            padding: 30px 20px;
            border-radius: 20px;
            text-align: center;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }
        .header-box h1 {
            margin: 0;
            font-size: 26px;
            font-weight: 800;
            letter-spacing: 0.5px;
        }
        .header-box p {
            margin: 10px 0 0 0;
            font-size: 13px;
            opacity: 0.9;
            font-weight: 600;
        }
    </style>
""", unsafe_allow_html=True)

# =========================================================
# 2. LOGIKA JAM & SHIFT KERJA (SINKRON WAKTU WIB)
# =========================================================
# Mengunci zona waktu ke Asia/Jakarta (WIB) agar tidak ikut waktu Amerika
tz_jkt = pytz.timezone('Asia/Jakarta')
waktu_sekarang = datetime.now(tz_jkt)

jam_menit_str = waktu_sekarang.strftime("%H:%M")
tanggal_str = waktu_sekarang.strftime("%d/%m/%Y")
jam_int = waktu_sekarang.hour

# Penentuan Shift Kerja Otomatis berdasarkan Jam WIB
if 6 <= jam_int < 14:
    shift_aktif = "Shift 1 (06:00 - 13:59)"
elif 14 <= jam_int < 22:
    shift_aktif = "Shift 2 (14:00 - 21:59)"
else:
    shift_aktif = "Shift 3 (22:00 - 05:59)"

# =========================================================
# 3. TAMPILAN INTERFACE APLIKASI DI HP
# =========================================================

# Kartu Judul Utama (Sudah naik ke atas)
st.markdown(f"""
    <div class="header-box">
        <h1>MILKING TIME REPORT</h1>
        <p>BUMI ROJO KOYO • MILKING DEPARTMENT</p>
    </div>
""", unsafe_allow_html=True)

# Informasi Shift & Waktu Real-Time Bapak
with st.container(border=True):
    st.markdown(f"🟢 **SHIFT KERJA SAAT INI:**")
    st.markdown(f"### {shift_aktif}")
    st.markdown(f"📆 **Tanggal:** {tanggal_str} | ⏰ **Jam WIB:** {jam_menit_str}")

# Input Simulasi Data Perahan
st.markdown("### 📋 PENCATATAN GRUP PERAH")
grup_opsi = [f"Grup {i}" for i in range(1, 10)]
grup_terpilih = st.selectbox("Pilih Group Sapi yang Siap Di-record:", grup_opsi)

# Progress bar
st.markdown("---")
st.markdown("**PROGRESS PEMERAHAN**")
st.progress(33)
st.caption("3 dari 9 group selesai")

if st.button("🚀 Simpan Data Perahan", use_container_width=True):
    st.success(f"Berhasil mencatat data untuk {grup_terpilih} pada jam {jam_menit_str} WIB!")
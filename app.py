import streamlit as st
from datetime import datetime
import pytz
import pandas as pd

# =========================================================
# 1. PENGATURAN HALAMAN & CSS GLOBAL (JUDUL NAIK & HAPUS LOGO)
# =========================================================
st.set_page_config(
    page_title="Milking Time Report",
    page_icon="🥛",
    layout="centered"
)

# Injeksi CSS super ketat untuk menghilangkan 2 logo bawah dan menaikkan judul
st.markdown("""
    <style>
        /* 1. Menaikkan judul mepet ke atas */
        .block-container {
            padding-top: 0.5rem !important;
            padding-bottom: 5rem !important;
            max-width: 500px !important;
        }
        
        /* 2. Menghilangkan logo mahkota merah Streamlit */
        footer {
            visibility: hidden !important;
            display: none !important;
        }
        
        /* 3. Menghilangkan tombol menu bulat ungu & elemen header atas */
        header {
            visibility: hidden !important;
            display: none !important;
        }
        
        /* Trik khusus menghapus ruang kosong sisa logo di paling bawah layar */
        .stAppDeployDropdown, .stAppToolbar, footer {
            display: none !important;
            visibility: hidden !important;
        }
        
        /* Desain kartu judul hijau */
        .header-box {
            background: linear-gradient(135deg, #11998e, #38ef7d);
            color: white;
            padding: 25px 15px;
            border-radius: 20px;
            text-align: center;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            margin-bottom: 15px;
        }
        .header-box h1 {
            margin: 0;
            font-size: 24px;
            font-weight: 800;
        }
        .header-box p {
            margin: 5px 0 0 0;
            font-size: 12px;
            opacity: 0.9;
        }
    </style>
""", unsafe_allow_html=True)

# =========================================================
# 2. LOGIKA JAM & SHIFT KERJA (WIB ZONA)
# =========================================================
tz_jkt = pytz.timezone('Asia/Jakarta')
waktu_sekarang = datetime.now(tz_jkt)

jam_menit_str = waktu_sekarang.strftime("%H:%M")
tanggal_str = waktu_sekarang.strftime("%d/%m/%Y")
jam_int = waktu_sekarang.hour

if 6 <= jam_int < 14:
    shift_aktif = "Shift 1 (06:00 - 13:59)"
elif 14 <= jam_int < 22:
    shift_aktif = "Shift 2 (14:00 - 21:59)"
else:
    shift_aktif = "Shift 3 (22:00 - 05:59)"

# =========================================================
# 3. TAMPILAN INTERFACE UTAMA
# =========================================================

# Kartu Judul Utama
st.markdown(f"""
    <div class="header-box">
        <h1>MILKING TIME REPORT</h1>
        <p>BUMI ROJO KOYO • MILKING DEPARTMENT</p>
    </div>
""", unsafe_allow_html=True)

# Status Shift & Waktu WIB
with st.container(border=True):
    st.markdown(f"🟢 **SHIFT KERJA SAAT INI:**")
    st.markdown(f"### {shift_aktif}")
    st.markdown(f"📆 **Tanggal:** {tanggal_str} | ⏰ **Jam WIB:** {jam_menit_str}")

# Formulir Input Pencatatan dengan Nama Kelompok Semula (Fresh, Early, dll)
st.markdown("### 📋 PENCATATAN GRUP PERAH")

# Mengembalikan nama-nama grup asli farm Bapak ke dalam daftar pilihan
grup_opsi = ["Fresh", "Early", "Mid", "Late", "Drying", "Sick/Treatment"]
grup_terpilih = st.selectbox("Pilih Group Sapi yang Siap Di-record:", grup_opsi)

# Progress bar
st.markdown("---")
st.markdown("**PROGRESS PEMERAHAN**")
st.progress(50)
st.caption(f"3 dari {len(grup_opsi)} group selesai")

if st.button("🚀 Simpan Data Perahan", use_container_width=True):
    st.success(f"Berhasil mencatat kelompok **{grup_terpilih}** pada jam {jam_menit_str} WIB!")

# =========================================================
# 4. TABEL HISTORY SEMUA SHIFT (SESUAI NAMA GRUP ASLI)
# =========================================================
st.markdown("---")
st.markdown("### 🕒 HISTORY PENCATATAN SHIFT")

# Simulasi data history menggunakan nama kelompok semula Bapak
data_history = {
    "Waktu": ["06:15", "07:20", "08:05"],
    "Group Sapi": ["Fresh", "Early", "Mid"],
    "Status": ["Selesai", "Selesai", "Selesai"]
}
df = pd.DataFrame(data_history)

# Menampilkan kembali tabel history yang rapi di layar bawah
st.dataframe(df, use_container_width=True, hide_index=True)
import streamlit as st
from datetime import datetime
import pytz
import pandas as pd
import requests

# =========================================================
# 1. PENGATURAN HALAMAN & CSS CUSTOM (MEPET ATAS & TANPA LOGO)
# =========================================================
st.set_page_config(page_title="Milking Time Report", page_icon="🥛", layout="centered")

st.markdown("""
    <style>
        header, footer, #MainMenu {visibility: hidden; display: none;}
        .block-container {padding-top: 0.5rem !important; max-width: 500px !important;}

        /* Header Hijau */
        .header-box {
            background-color: #4CAF50; color: white; padding: 20px 15px;
            border-radius: 20px; text-align: center; margin-bottom: 15px;
        }

        /* Tombol List Antrean (Hijau) */
        .stButton > button {
            background-color: #4CAF50 !important; color: white !important;
            border-radius: 15px !important; border: none !important;
            height: 55px !important; width: 100% !important;
            font-size: 18px !important; font-weight: bold !important;
            text-align: left !important; padding-left: 20px !important;
            margin-bottom: 8px !important;
        }

        /* Tombol Sick (Merah) */
        .sick-button > div > div > button { background-color: #F44336 !important; }

        /* Tombol End Milking (Gelap) */
        .end-button > div > div > button {
            background-color: #1E293B !important; text-align: center !important;
        }
    </style>
""", unsafe_allow_html=True)

# =========================================================
# 2. LOGIKA JAM, SHIFT AUTOMATION & AUTO RESET 05:30
# =========================================================
tz_jkt = pytz.timezone('Asia/Jakarta')
waktu_sekarang = datetime.now(tz_jkt)
tanggal_str = waktu_sekarang.strftime("%d/%m/%Y")
jam_menit_str = waktu_sekarang.strftime("%H:%M")
jam_int = waktu_sekarang.hour
menit_int = waktu_sekarang.minute

# Penentuan Shift Otomatis Sesuai Request Bapak
if 6 <= jam_int < 14:
    shift_aktif = "Shift 1"
elif 14 <= jam_int < 22:
    shift_aktif = "Shift 2"
else:
    shift_aktif = "Shift 3"

# Inisialisasi Database Sementara (Session State)
if 'history_data' not in st.session_state:
    st.session_state.history_data = []

# Fitur Otomatis Refresh / Reset Data setiap Jam 05:30 Pagi WIB
if jam_int == 5 and menit_int == 30:
    st.session_state.history_data = []
    st.rerun()

# Daftar semua grup perah semula
all_groups = ["5B Fresh", "5B Early", "5A Early", "4B Early", "4A Late", "3B Late", "3A Late", "2A Late", "6A Sick", "End Milking"]

# Memfilter grup yang BELUM diklik pada shift aktif saat ini agar tombol yang sudah diklik langsung hilang
grup_terisi_shift_ini = [
    d['Group'] for d in st.session_state.history_data 
    if d['Shift'] == shift_aktif and d['Tanggal'] == tanggal_str
]
grup_antrean = [g for g in all_groups if g not in grup_terisi_shift_ini]

# =========================================================
# 3. FUNGSI OTOMATIS TEMBAK WHATSAPP (FONNTE GATEWAY)
# =========================================================
def kirim_wa_fonnte(grup_baru, jam_baru):
    token_fonnte = "dwRvJcr5jphRFnarpSL9"
    target_wa = "081234567890"  # <<< GANTI dengan Nomor HP Tujuan / ID Group WA Bapak
    
    # Menyusun format akumulatif teks berlanjut sesuai inputan baru
    pesan = f"*MILKING TIME REPORT*\n📅 Tanggal : {tanggal_str}\n🟢 Shift : {shift_aktif}\n\n"
    
    # Ambil data lama yang sudah terisi di shift ini
    for item in st.session_state.history_data:
        if item['Shift'] == shift_aktif and item['Tanggal'] == tanggal_str:
            pesan += f"*{item['Group']}* : {item['Jam']}\n"
            
    # Tambahkan data baru yang barusan diklik
    pesan += f"*{grup_baru}* : {jam_baru}\n"
    
    # Proses kirim API ke Fonnte
    url = "https://api.fonnte.com/send"
    payload = {'target': target_wa, 'message': pesan}
    headers = {'Authorization': token_fonnte}
    try:
        requests.post(url, data=payload, headers=headers)
    except:
        pass

# =========================================================
# 4. INTERFACE UTAMA APLIKASI
# =========================================================

# Kotak Judul
st.markdown(f"""
    <div class="header-box">
        <h1 style='margin:0; font-size:24px;'>MILKING TIME REPORT</h1>
        <p style='margin:5px 0 0 0;'>BUMI ROJO KOYO • MILKING DEPARTMENT</p>
    </div>
""", unsafe_allow_html=True)

# Info Jam & Shift Otomatis
with st.container(border=True):
    st.markdown(f"⏱️ **SISTEM DETEKSI OTOMATIS:**")
    st.markdown(f"### 🟢 {shift_aktif}")
    st.markdown(f"📆 Tanggal: **{tanggal_str}** | ⏰ Jam WIB: **{jam_menit_str}**")

st.markdown("<br><p style='text-align:center; color:grey; font-weight:bold; margin-bottom:5px;'>DAFTAR ANTREAN GROUP PERAH</p>", unsafe_allow_html=True)

# Tampilan Tombol Antrean yang Tersisa (Akan berkurang/hilang satu per satu saat diklik)
if grup_antrean:
    for g in grup_antrean:
        if g == "End Milking":
            st.markdown('<div class="end-button">', unsafe_allow_html=True)
            if st.button(f"🏁 {g.upper()}", key=g, use_container_width=True):
                waktu_klik = datetime.now(tz_jkt).strftime("%H:%M")
                kirim_wa_fonnte(g, waktu_klik)
                st.session_state.history_data.append({"Tanggal": tanggal_str, "Shift": shift_aktif, "Group": g, "Jam": waktu_klik})
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            is_sick = "6A Sick" in g
            div_style = "sick-button" if is_sick else "normal-button"
            st.markdown(f'<div class="{div_style}">', unsafe_allow_html=True)
            if st.button(f"{g} ▶️", key=g, use_container_width=True):
                waktu_klik = datetime.now(tz_jkt).strftime("%H:%M")
                kirim_wa_fonnte(g, waktu_klik)
                st.session_state.history_data.append({"Tanggal": tanggal_str, "Shift": shift_aktif, "Group": g, "Jam": waktu_klik})
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
else:
    st.success("🎉 Semua group perah untuk shift ini telah selesai dicatat!")

# =========================================================
# 5. HISTORY HISTORY BERDASARKAN SHIFT 1, 2, DAN 3
# =========================================================
st.markdown("---")
st.markdown("## 🕒 HISTORY PENCATATAN")

df_master = pd.DataFrame(st.session_state.history_data)

for s in ["Shift 1", "Shift 2", "Shift 3"]:
    st.markdown(f"### 📋 {s}")
    if not df_master.empty:
        df_shift = df_master[(df_master['Shift'] == s) & (df_master['Tanggal'] == tanggal_str)]
        if not df_shift.empty:
            st.dataframe(df_shift[["Group", "Jam"]], use_container_width=True, hide_index=True)
        else:
            st.caption("Belum ada data diinput untuk shift ini.")
    else:
        st.caption("Belum ada data diinput untuk shift ini.")
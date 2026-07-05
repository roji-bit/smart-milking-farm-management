import streamlit as st
from datetime import datetime
import pytz
import pandas as pd

# =========================================================
# 1. PENGATURAN HALAMAN & CSS CUSTOM (DESAIN BARU)
# =========================================================
st.set_page_config(page_title="Milking Time Report", page_icon="🥛", layout="centered")

st.markdown("""
    <style>
        /* Sembunyikan elemen bawaan Streamlit */
        header, footer, #MainMenu {visibility: hidden; display: none;}
        .block-container {padding-top: 1rem !important; max-width: 500px !important;}

        /* Header Hijau */
        .header-box {
            background-color: #4CAF50; color: white; padding: 25px 15px;
            border-radius: 20px; text-align: center; margin-bottom: 20px;
        }

        /* Tombol Grup (Hijau) */
        .stButton > button {
            background-color: #4CAF50 !important; color: white !important;
            border-radius: 15px !important; border: none !important;
            height: 60px !important; width: 100% !important;
            font-size: 20px !important; font-weight: bold !important;
            text-align: left !important; padding-left: 20px !important;
            margin-bottom: 10px !important; display: flex !important;
            justify-content: space-between !important; align-items: center !important;
        }

        /* Tombol Sick (Merah) */
        .sick-button > div > div > button {
            background-color: #F44336 !important;
        }

        /* Tombol End Milking (Gelap) */
        .end-button > div > div > button {
            background-color: #1E293B !important;
            text-align: center !important; justify-content: center !important;
        }
        
        .group-label { font-size: 18px; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# =========================================================
# 2. LOGIKA DATA & WAKTU
# =========================================================
tz_jkt = pytz.timezone('Asia/Jakarta')
waktu_sekarang = datetime.now(tz_jkt)
tanggal_laporan = waktu_sekarang.strftime("%d/%m/%Y")

# Inisialisasi State (Penyimpanan Sementara)
if 'history' not in st.session_state:
    st.session_state.history = {}

groups = [
    "5B Fresh", "5B Early", "5A Early", "4B Early", 
    "4A Late", "3B Late", "3A Late", "2A Late", "6A Sick"
]

# =========================================================
# 3. TAMPILAN APLIKASI
# =========================================================

# Header
st.markdown(f"""
    <div class="header-box">
        <h1 style='margin:0; font-size:26px;'>MILKING TIME REPORT</h1>
        <p style='margin:5px 0 0 0;'>BUMI ROJO KOYO • MILKING DEPARTMENT</p>
    </div>
""", unsafe_allow_html=True)

# Shift Info
with st.container(border=True):
    st.markdown("🟢 **SHIFT KERJA SAAT INI:**")
    st.selectbox("Pilih Shift:", ["Shift 1 (06:00 - 13:00)", "Shift 2 (14:00 - 21:00)", "Shift 3 (22:00 - 05:00)"], label_visibility="collapsed")

# Progress Bar
st.markdown("<br>", unsafe_allow_html=True)
count_done = len(st.session_state.history)
progress = count_done / (len(groups) + 1)
col_a, col_b = st.columns([2,1])
col_a.markdown(f"**PROGRESS PEMERAHAN**")
col_b.markdown(f"<p style='text-align:right; color:green; font-weight:bold;'>{int(progress*100)}%</p>", unsafe_allow_html=True)
st.progress(progress)
st.caption(f"{count_done} dari {len(groups)+1} group selesai")

# Daftar Antrean
st.markdown("<p style='text-align:center; color:grey; font-weight:bold;'>DAFTAR ANTREAN GROUP PERAH</p>", unsafe_allow_html=True)

for g in groups:
    # Styling khusus untuk grup Sick
    is_sick = "6A Sick" in g
    button_type = "sick-button" if is_sick else "normal-button"
    
    col_btn = st.container()
    with col_btn:
        st.markdown(f'<div class="{button_type}">', unsafe_allow_html=True)
        # Menampilkan jam jika sudah di-klik
        label = f"{g} 🕒 {st.session_state.history.get(g, '')}" if g in st.session_state.history else f"{g} ▶️"
        if st.button(label, key=g):
            st.session_state.history[g] = waktu_sekarang.strftime("%H:%M")
        st.markdown('</div>', unsafe_allow_html=True)

# End Milking Button
st.markdown("<br>", unsafe_allow_html=True)
st.markdown('<div class="end-button">', unsafe_allow_html=True)
label_end = f"🏁 🏁 END MILKING 🕒 {st.session_state.history.get('End', '')}" if 'End' in st.session_state.history else "🏁 🏁 END MILKING"
if st.button(label_end, key="end_btn"):
    st.session_state.history['End'] = waktu_sekarang.strftime("%H:%M")
st.markdown('</div>', unsafe_allow_html=True)

# =========================================================
# 4. HISTORY & TEMPLATE WHATSAPP
# =========================================================
st.markdown("---")
st.markdown("### 🕒 HISTORY PENCATATAN")
if st.session_state.history:
    df = pd.DataFrame([{"Group": k, "Jam": v} for k, v in st.session_state.history.items()])
    st.table(df)

    # Template WA
    st.markdown("### 📱 TEMPLATE LAPORAN WA")
    wa_text = f"*MILKING TIME REPORT*\n📅 Tanggal : {tanggal_laporan}\n\n"
    for g in groups:
        jam = st.session_state.history.get(g, "--:--")
        wa_text += f"*{g}* : {jam}\n"
    
    jam_end = st.session_state.history.get('End', "--:--")
    wa_text += f"\n*End Milking* : {jam_end}"
    
    st.code(wa_text, language="text")
    st.info("Salin teks di atas untuk dikirim ke Grup WhatsApp.")
else:
    st.write("Belum ada data tercatat.")
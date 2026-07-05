import streamlit as st
import requests
from datetime import datetime, timedelta

# Pengaturan dasar halaman agar pas di layar HP
st.set_page_config(page_title="Milking Time Report", layout="centered")

# --- URL WEB APP GOOGLE APPS SCRIPT KAMU ---
URL_WEB_APP_SHEETS = "https://script.google.com/a/macros/bumirojokoyo.com/s/AKfycbyUn3VZlml4I1RkrAJAb_zCMz-w_mzJRbClEhkvsI_xm0yIYKOJz2wA4f-QzGWYsoIk/exec"

# --- INJEKSI CSS CUSTOM UTK TAMPILAN PREMIUM HP ---
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    .header-box {
        background: linear-gradient(135deg, #38b000 0%, #007200 100%);
        color: white;
        padding: 25px 10px;
        border-radius: 18px;
        text-align: center;
        box-shadow: 0 6px 12px rgba(0,0,0,0.15);
        margin-bottom: 20px;
    }
    .header-box h1 {
        font-size: 24px !important;
        font-weight: 800 !important;
        margin: 0 !important;
        letter-spacing: 1px;
    }
    .header-box p {
        font-size: 13px;
        margin: 5px 0 0 0;
        opacity: 0.9;
        letter-spacing: 0.5px;
    }
    
    .custom-card {
        background-color: white;
        padding: 20px;
        border-radius: 14px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.06);
        border: 1px solid #eef2f3;
        margin-bottom: 15px;
    }
    
    .card-label {
        font-size: 12px;
        font-weight: 700;
        color: #6c757d;
        text-transform: uppercase;
        margin-bottom: 8px;
        display: flex;
        align-items: center;
        gap: 5px;
    }
    </style>
""", unsafe_allow_html=True)

# --- HEADER UTAMA ---
st.markdown("""
    <div class="header-box">
        <h1>MILKING TIME REPORT</h1>
        <p>BUMI ROJO KOYO • MILKING DEPARTMENT</p>
    </div>
""", unsafe_allow_html=True)

GRUP_SAPI = ["5B Fresh", "5B Early", "5A Early", "4B Early", "4A Late", "3B Late", "3A Late", "2A Late", "6A Sick"]
GRUP_MASTER = GRUP_SAPI + ["End Milking"]

# --- LOGIKA PENENTUAN SHIFT ---
waktu_sekarang = datetime.now()
jam_angka = waktu_sekarang.hour

if 6 <= jam_angka <= 13:
    indeks_shift = 0  
    id_shift_aktif = "Shift 1 (06:00 - 13:59)"
    id_kunci = "S1"
    tanggal_laporan = waktu_sekarang.strftime("%d/%m/%Y")
elif 14 <= jam_angka <= 21:
    indeks_shift = 1  
    id_shift_aktif = "Shift 2 (14:00 - 21:59)"
    id_kunci = "S2"
    tanggal_laporan = waktu_sekarang.strftime("%d/%m/%Y")
else:
    indeks_shift = 2  
    id_shift_aktif = "Shift 3 (22:00 - 05:59)"
    id_kunci = "S3"
    if jam_angka < 6:
        tanggal_laporan = (waktu_sekarang - timedelta(days=1)).strftime("%d/%m/%Y")
    else:
        tanggal_laporan = waktu_sekarang.strftime("%d/%m/%Y")

# --- LOGIKA AUTO RESET STATE HARI & SHIFT ---
if "tanggal_terakhir" not in st.session_state or st.session_state.tanggal_terakhir != tanggal_laporan:
    st.session_state.tanggal_terakhir = tanggal_laporan
    st.session_state.data_laporan = {grup: ["-", "-", "-"] for grup in GRUP_MASTER}

id_kunci_shift_ini = f"{tanggal_laporan}-{id_kunci}"
if "kunci_shift_terakhir" not in st.session_state or st.session_state.kunci_shift_terakhir != id_kunci_shift_ini:
    st.session_state.kunci_shift_terakhir = id_kunci_shift_ini
    st.session_state.grup_sudah_diisi_shift_ini = []

grup_tersedia = [grup for grup in GRUP_MASTER if grup not in st.session_state.grup_sudah_diisi_shift_ini]

# --- KARTU 1: SHIFT KERJA SAAT INI ---
st.markdown(f"""
    <div class="custom-card">
        <div class="card-label">🟢 Shift Kerja Saat Ini:</div>
        <h3 style='margin:0; color:#1e293b; font-size:18px;'>{id_shift_aktif}</h3>
        <p style='margin:5px 0 0 0; color:#64748b; font-size:13px;'>📅 Tanggal: {tanggal_laporan}</p>
    </div>
""", unsafe_allow_html=True)

# --- KARTU 2: PROGRESS PEMERAHAN BAR ---
grup_selesai_hitung = [g for g in GRUP_SAPI if g in st.session_state.grup_sudah_diisi_shift_ini]
jumlah_selesai = len(grup_selesai_hitung)
persentase_progress = int((jumlah_selesai / 9) * 100)

st.markdown(f"""
    <div class="custom-card" style="border-left: 5px solid #38b000;">
        <div style="display:flex; justify-content:space-between; align-items:center;">
            <div class="card-label" style="margin:0;">PROGRESS PEMERAHAN</div>
            <div style="color:#38b000; font-weight:800; font-size:20px;">{persentase_progress}%</div>
        </div>
""", unsafe_allow_html=True)
st.progress(persentase_progress / 100)
st.markdown(f"""<p style='margin:5px 0 0 0; text-align:right; color:#64748b; font-size:12px;'>{jumlah_selesai} dari 9 group selesai</p></div>""", unsafe_allow_html=True)

# --- KARTU 3: DAFTAR ANTREAN ---
st.markdown("""
    <div class="custom-card">
        <div class="card-label" style="text-align:center; display:block;">DAFTAR ANTREAN GROUP PERAH</div>
        <hr style="margin:10px 0; border:0; border-top:1px solid #e2e8f0;">
""", unsafe_allow_html=True)

if not grup_tersedia:
    st.markdown("""
        <div style="text-align:center; padding: 15px 0;">
            <h2 style="color:#38b000; margin:0; font-size:35px;">✅</h2>
            <p style="color:#38b000; font-weight:700; margin:5px 0 0 0; font-size:15px;">Semua Group Sapi Selesai Diperah!</p>
        </div>
    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    if st.checkbox("🔄 Mode Koreksi Data Shift Ini"):
        st.session_state.grup_sudah_diisi_shift_ini = []
        st.rerun()
else:
    grup_terpilih = st.selectbox("Pilih Group Sapi yang Siap Di-record:", grup_tersedia, label_visibility="collapsed")
    st.write("")
    
    if st.button("💾 RECORD JAM, GOOGLE SHEETS & WA", use_container_width=True, type="primary"):
        jam_menit_str = waktu_sekarang.strftime("%H:%M")
        waktu_log = waktu_sekarang.strftime("%Y-%m-%d %H:%M:%S")
        
        st.session_state.data_laporan[grup_terpilih][indeks_shift] = jam_menit_str
        st.session_state.grup_sudah_diisi_shift_ini.append(grup_terpilih)
        
        # A. PROSES SIMPAN OTOMATIS KE GOOGLE SHEETS VIA WEB APP
        try:
            payload_sheets = {
                "Tanggal": tanggal_laporan,
                "GroupSapi": grup_terpilih,
                "Shift": f"Shift {indeks_shift + 1}",
                "JamPerah": jam_menit_str,
                "Operator": "Milking Supervisor",
                "WaktuInput": waktu_log
            }
            requests.post(URL_WEB_APP_SHEETS, json=payload_sheets)
            st.toast("💾 Tersimpan ke Google Sheets!", icon="☁️")
        except Exception as e:
            st.error(f"Gagal simpan ke Sheets: {e}")
        
        # B. PROSES SUSUN TEKS & KIRIM WA (FONNTE)
        teks_grup_grup = ""
        for grup in GRUP_MASTER:
            s1 = st.session_state.data_laporan[grup][0]
            s2 = st.session_state.data_laporan[grup][1]
            s3 = st.session_state.data_laporan[grup][2]
            if grup == "End Milking":
                teks_grup_grup += f"\n*{grup}* : {s1} / {s2} / {s3}\n"
            else:
                teks_grup_grup += f"*{grup}* : {s1} / {s2} / {s3}\n"

        pesan_wa = f"*MILKING TIME REPORT*\n📅 Tanggal : {tanggal_laporan}\n\n{teks_grup_grup}"
        
        url_fonnte = "https://api.fonnte.com/send"
        payload_wa = {'target': '6281332276546', 'message': pesan_wa}
        headers_wa = {'Authorization': 'dwRvJcr5jphRFnarpSL9'}
        
        response = requests.post(url_fonnte, data=payload_wa, headers=headers_wa)
        if response.status_code == 200:
            st.success(f"✅ Data {grup_terpilih} ({jam_menit_str}) Sukses Terkirim!")
            st.rerun()
        else:
            st.error("❌ Kiriman WA Fonnte gagal, cek jaringan.")
            
    st.markdown("</div>", unsafe_allow_html=True)

# --- KARTU 4: LIVE MONITORING TABEL ---
st.markdown("""
    <div class="custom-card">
        <div class="card-label">📊 LIVE DATA MONITORING HARI INI:</div>
""", unsafe_allow_html=True)

data_tabel = []
for grup in GRUP_MASTER:
    data_tabel.append({
        "Group Sapi": grup,
        "Shift 1": st.session_state.data_laporan[grup][0],
        "Shift 2": st.session_state.data_laporan[grup][1],
        "Shift 3": st.session_state.data_laporan[grup][2]
    })
st.table(data_tabel)
st.markdown("</div>", unsafe_allow_html=True)
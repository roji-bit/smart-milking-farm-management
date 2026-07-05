<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Milking Time Report</title>
    <script src="https://www.gstatic.com/firebasejs/8.10.1/firebase-app.js"></script>
    <script src="https://www.gstatic.com/firebasejs/8.10.1/firebase-database.js"></script>
    
    <style>
        * { box-sizing: border-box; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0; padding: 0; }
        body { background-color: #f5f5f5; padding: 15px; display: flex; justify-content: center; }
        .container { width: 100%; max-width: 500px; background: white; padding: 20px; border-radius: 20px; box-shadow: 0 4px 10px rgba(0,0,0,0.05); }
        
        /* Header Box */
        .header-box { background: linear-gradient(135deg, #11998e, #38ef7d); color: white; padding: 20px; border-radius: 15px; text-align: center; margin-bottom: 15px; }
        .header-box h1 { font-size: 24px; font-weight: 800; }
        .header-box p { font-size: 12px; opacity: 0.9; margin-top: 5px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; }
        
        /* Info Box */
        .info-box { border: 1px solid #e0e0e0; padding: 15px; border-radius: 15px; margin-bottom: 15px; background-color: #fafafa; }
        .info-title { color: #666; font-size: 14px; font-weight: bold; }
        .info-shift { color: #4CAF50; font-size: 22px; font-weight: bold; margin-top: 2px; }
        .info-time { font-size: 13px; color: #333; margin-top: 5px; }
        
        /* List Antrean */
        .section-title { text-align: center; color: #888; font-weight: bold; font-size: 14px; margin: 20px 0 10px 0; letter-spacing: 0.5px; }
        .btn-list { display: flex; flex-direction: column; gap: 8px; }
        
        /* Tombol Utama */
        .btn-group { width: 100%; height: 55px; background-color: #4CAF50; color: white; border: none; border-radius: 12px; font-size: 18px; font-weight: bold; text-align: left; padding-left: 20px; cursor: pointer; display: flex; align-items: center; justify-content: space-between; box-shadow: 0 2px 5px rgba(0,0,0,0.05); }
        .btn-group.sick { background-color: #F44336; }
        .btn-group.end { background-color: #1E293B; justify-content: center; padding: 0; }
        .btn-group:active { opacity: 0.9; }
        
        /* Tabel History */
        table { width: 100%; border-collapse: collapse; margin-top: 10px; font-size: 14px; }
        th, td { border: 1px solid #e0e0e0; padding: 10px; text-align: left; }
        th { background-color: #fafafa; font-weight: bold; }
        .success-msg { background-color: #e8f5e9; color: #2e7d32; padding: 15px; border-radius: 12px; text-align: center; font-weight: bold; font-size: 15px; }
    </style>
</head>
<body>

<div class="container">
    <div class="header-box">
        <h1>MILKING TIME REPORT</h1>
        <p>MILKING DEPARTMENT • INDEPENDENT SYSTEM</p>
    </div>

    <div class="info-box">
        <div class="info-title">⏱️ SISTEM DETEKSI OTOMATIS:</div>
        <div class="info-shift" id="txt-shift">Memuat...</div>
        <div class="info-time" id="txt-waktu">Memuat tanggal dan jam...</div>
    </div>

    <div class="section-title">DAFTAR ANTREAN GROUP PERAH</div>
    <div class="btn-list" id="area-tombol">
        </div>
    <div id="area-sukses" class="success-msg" style="display: none;">
        🎉 Semua group perah untuk shift ini telah selesai dicatat!
    </div>

    <div class="section-title" style="margin-top: 30px;">🕒 HISTORY PENCATATAN</div>
    <table>
        <thead>
            <tr>
                <th>Group Sapi</th>
                <th>Shift 1</th>
                <th>Shift 2</th>
                <th>Shift 3</th>
            </tr>
        </thead>
        <tbody id="tabel-history">
            </tbody>
    </table>
</div>

<script>
    // =========================================================
    // DATA PROYEK FIREBASE (TERKUNCI)
    // =========================================================
    const firebaseConfig = {
        apiKey: "AIzaSyC2NlZ" + "q5Cst8vW_m26SHeA9pMvV_rO6iFs", 
        databaseURL: "https://bumirojokoyo-milking-default-rtdb.asia-southeast1.firebasedatabase.app"
    };
    
    // Initialize Firebase
    firebase.initializeApp(firebaseConfig);
    const database = firebase.database();

    // Data Konfigurasi Tetap Aplikasi
    const allGroups = ["5B Fresh", "5B Early", "5A Early", "4B Early", "4A Late", "3B Late", "3A Late", "2A Late", "6A Sick", "End Milking"];
    const tokenFonnte = "dwRvJcr5jphRFnarpSL9";
    const targetWa = "6281332276546";

    // Variabel Penentu Waktu & Shift
    let tanggalStr = "";
    let shiftAktif = "";
    let shiftIdx = 0;

    function updateWaktuDanShift() {
        const sekarang = new Date(new Date().toLocaleString("en-US", {timeZone: "Asia/Jakarta"}));
        
        let dd = String(sekarang.getDate()).padStart(2, '0');
        let mm = String(sekarang.getMonth() + 1).padStart(2, '0');
        let yyyy = sekarang.getFullYear();
        tanggalStr = `${dd}-${mm}-${yyyy}`; // Format tanggal id Firebase

        let jam = sekarang.getHours();
        let menit = String(sekarang.getMinutes()).padStart(2, '0');
        let jamMenit = `${String(jam).padStart(2, '0')}:${menit}`;

        // Reset Otomatis Jam 05:30 Pagi
        if (jam === 5 && menit === "30") {
            database.ref('milking/' + tanggalStr).remove();
            location.reload();
        }

        // Pembagian Shift Otomatis sesuai jam kerja
        if (jam >= 6 && jam < 14) {
            shiftAktif = "Shift 1"; shiftIdx = 0;
        } else if (jam >= 14 && jam < 22) {
            shiftAktif = "Shift 2"; shiftIdx = 1;
        } else {
            shiftAktif = "Shift 3"; shiftIdx = 2;
        }

        document.getElementById("txt-shift").innerText = `🟢 ${shiftAktif}`;
        document.getElementById("txt-waktu").innerText = `📆 Tanggal: ${dd}/${mm}/${yyyy} | ⏰ Jam WIB: ${jamMenit}`;
    }

    // Jalankan waktu pertama kali
    updateWaktuDanShift();
    setInterval(updateWaktuDanShift, 10000); // Sinkronisasi berkala tiap 10 detik

    // Mendengarkan Perubahan Data secara Real-time dari Firebase Server
    database.ref('milking/' + tanggalStr).on('value', (snapshot) => {
        let data = snapshot.val() || {};
        
        // Pastikan struktur dasar grup siap
        allGroups.forEach(g => {
            if (!data[g]) data[g] = ["--:--", "--:--", "--:--"];
        });

        // 1. Render Ulang Tombol Antrean (Tombol terisi otomatis HILANG dari antrean)
        const areaTombol = document.getElementById("area-tombol");
        areaTombol.innerHTML = "";
        let adaTombol = false;

        allGroups.forEach(g => {
            if (data[g][shiftIdx] === "--:--") {
                adaTombol = true;
                const btn = document.createElement("button");
                btn.className = "btn-group";
                
                if (g === "6A Sick") btn.classList.add("sick");
                if (g === "End Milking") {
                    btn.classList.add("end");
                    btn.innerHTML = `🏁 ${g.toUpperCase()}`;
                } else {
                    btn.innerHTML = `<span>${g}</span> <span>▶️</span>`;
                }

                btn.onclick = () => simpanDanKirim(g, data);
                areaTombol.appendChild(btn);
            }
        });

        if (adaTombol) {
            document.getElementById("area-sukses").style.display = "none";
        } else {
            document.getElementById("area-sukses").style.display = "block";
        }

        // 2. Render Ulang Tabel History Bawah
        const tabelHistory = document.getElementById("tabel-history");
        tabelHistory.innerHTML = "";
        allGroups.forEach(g => {
            const tr = document.createElement("tr");
            tr.innerHTML = `
                <td><b>${g}</b></td>
                <td>${data[g][0]}</td>
                <td>${data[g][1]}</td>
                <td>${data[g][2]}</td>
            `;
            tabelHistory.appendChild(tr);
        });
    });

    // Fungsi klik tombol: Simpan ke Firebase Database + Kirim Tembakan Otomatis WA Fonnte
    function simpanDanKirim(group, dataSekarang) {
        const sekarang = new Date(new Date().toLocaleString("en-US", {timeZone: "Asia/Jakarta"}));
        let jamKlik = `${String(sekarang.getHours()).padStart(2, '0')}:${String(sekarang.getMinutes()).padStart(2, '0')}`;
        
        // Update data lokal sebelum kirim WA
        dataSekarang[group][shiftIdx] = jamKlik;

        // 1. Simpan permanen ke Firebase Database Cloud Server
        database.ref('milking/' + tanggalStr + '/' + group + '/' + shiftIdx).set(jamKlik);

        // 2. Susun template pesan berlanjut untuk dikirim ke Fonnte
        let formatTanggalWA = tanggalStr.replace(/-/g, '/');
        let pesan = `*MILKING TIME REPORT*\n📅 Tanggal : ${formatTanggalWA}\n\n`;
        
        allGroups.forEach(g => {
            if (g === "End Milking") pesan += "\n";
            pesan += `*${g}* : ${dataSekarang[g][0]} / ${dataSekarang[g][1]} / ${dataSekarang[g][2]}\n`;
        });

        // Kirim HTTP POST Request otomatis langsung ke API Fonnte Gateway
        var formData = new FormData();
        formData.append('target', targetWa);
        formData.append('message', pesan);

        fetch('https://api.fonnte.com/send', {
            method: 'POST',
            headers: { 'Authorization': tokenFonnte },
            body: formData
        }).catch(err => console.log("Gagal kirim WA:", err));
    }
</script>

</body>
</html>
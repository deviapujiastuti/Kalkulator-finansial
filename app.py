import streamlit as st

st.set_page_config(
    page_title="Kalkulator Finansial",
    page_icon="💰",
    layout="wide"
)

def rupiah(x):
    return f"Rp {x:,.0f}".replace(",", ".")

# ============ KODE AKSES (disimpan di Streamlit Secrets, bukan di file ini) ============
# Cara setting: buat file .streamlit/secrets.toml (lokal) atau isi lewat menu
# "Settings > Secrets" di Streamlit Community Cloud, dengan format:
#
# kode_akses_valid = ["DEVIA-7X9K", "DEVIA-4M2P", "DEVIA-8L5Q"]
#
# Kalau belum ada secrets sama sekali, aplikasi tetap bisa dibuka tanpa kode
# (mode ini otomatis aktif kalau kamu belum setting apapun) — cocok buat testing.

KODE_AKSES_VALID = st.secrets.get("kode_akses_valid", None)

if "akses_diberikan" not in st.session_state:
    st.session_state["akses_diberikan"] = False

if KODE_AKSES_VALID and not st.session_state["akses_diberikan"]:
    st.title("💰 Kalkulator Keuangan Sehari-hari")
    st.write("Aplikasi ini khusus untuk pembeli. Masukkan kode akses yang kamu terima setelah pembelian.")
    kode_input = st.text_input("Kode Akses", placeholder="Masukkan Kode Akses Disini...")
    cek_kode = st.button("Masuk", type="primary")

    if cek_kode:
        if kode_input.strip().upper() in [k.upper() for k in KODE_AKSES_VALID]:
            st.session_state["akses_diberikan"] = True
            st.rerun()
        else:
            st.error("Kode akses salah atau tidak ditemukan. Cek kembali kode yang kamu terima, atau hubungi penjual.")

    st.stop()

st.title("💰 Kalkulator Keuangan Sehari-hari")
st.caption("Alat bantu hitung keuangan simpel, tanpa istilah ribet — gratis, ngga perlu login/API apapun")

tab1, tab2, tab3 = st.tabs(["🛟 Dana Darurat", "🏠 Simulasi Cicilan", "💵 Gaji yang Diterima"])

# ================= TAB 1: DANA DARURAT =================
with tab1:
    st.subheader("Berapa Tabungan Jaga-Jaga yang Aku Perlu Punya?")
    st.write("Dana darurat itu tabungan buat jaga-jaga kalau tiba-tiba butuh uang mendesak — misal kena PHK, sakit, atau kendaraan rusak. Isi angkanya di bawah, nanti kelihatan berapa yang idealnya kamu siapkan.")

    col1, col2 = st.columns(2)
    with col1:
        status = st.selectbox("Status kamu sekarang", ["Belum menikah", "Menikah, belum punya anak", "Menikah, sudah punya anak"])
        pengeluaran_bulanan = st.number_input("Pengeluaran rutin kamu tiap bulan (Rp)", min_value=0, value=5000000, step=100000,
                                                help="Total pengeluaran wajib sebulan: makan, kos/kontrakan, transport, dll")
    with col2:
        tabungan_sekarang = st.number_input("Tabungan dana darurat yang sudah kamu punya sekarang (Rp)", min_value=0, value=0, step=100000)
        tabungan_bulanan = st.number_input("Kira-kira bisa nabung berapa per bulan buat dana darurat? (Rp)", min_value=0, value=500000, step=50000)

    if status == "Belum menikah":
        bulan_target = 6
    elif status == "Menikah, belum punya anak":
        bulan_target = 9
    else:
        bulan_target = 12

    target_dana_darurat = pengeluaran_bulanan * bulan_target
    kekurangan = max(target_dana_darurat - tabungan_sekarang, 0)

    st.markdown("---")
    c1, c2, c3 = st.columns(3)
    c1.metric("Dana Darurat yang Sebaiknya Kamu Punya", rupiah(target_dana_darurat))
    c2.metric("Masih Kurang", rupiah(kekurangan))

    if kekurangan > 0 and tabungan_bulanan > 0:
        bulan_dibutuhkan = kekurangan / tabungan_bulanan
        c3.metric("Kira-Kira Tercapai Dalam", f"{bulan_dibutuhkan:.1f} bulan")
    elif kekurangan == 0:
        c3.metric("Status", "Sudah tercapai! 🎉")
    else:
        c3.metric("Kira-Kira Tercapai Dalam", "-")

    st.info(f"Patokan umum: kalau kamu **{status.lower()}**, sebaiknya punya tabungan dana darurat setara **{bulan_target}x pengeluaran bulanan kamu**, buat jaga-jaga kalau ada kejadian mendadak (kena PHK, sakit, dll).")

# ================= TAB 2: SIMULASI CICILAN =================
with tab2:
    st.subheader("Simulasi Cicilan Utang")
    st.write("Mau beli rumah, motor/mobil, atau pinjam uang buat kebutuhan lain? Isi angkanya di bawah, nanti langsung kelihatan cicilan per bulannya.")

    jenis_pilihan = st.selectbox("Ini cicilan buat apa?", ["Rumah", "Motor / Mobil", "Lainnya (isi sendiri)"])
    if jenis_pilihan == "Lainnya (isi sendiri)":
        nama_pinjaman = st.text_input("Tulis nama pinjamannya", value="Pinjaman saya")
    else:
        nama_pinjaman = jenis_pilihan

    col1, col2 = st.columns(2)
    with col1:
        harga_barang = st.number_input("Harga barang / jumlah yang mau dipinjam (Rp)", min_value=0, value=300000000, step=1000000,
                                        help="Contoh: harga rumah, harga motor, atau jumlah uang yang mau dipinjam")
        uang_muka = st.number_input("Uang muka / DP yang sudah dibayar duluan (Rp)", min_value=0, value=60000000, step=1000000,
                                     help="Kalau bayar langsung lunas tanpa DP, isi 0 saja")
    with col2:
        lama_tahun = st.number_input("Mau dicicil berapa lama? (dalam tahun)", min_value=1, max_value=30, value=15)
        bunga_pertahun = st.number_input("Bunga per tahun (%)", min_value=0.0, value=8.5, step=0.1,
                                          help="Biasanya tertulis di brosur/perjanjian dari bank atau leasing, misal '8.5% per tahun'")
        metode_pilihan = st.selectbox("Tipe cicilan", [
            "Cicilan makin lama makin kecil (biasanya buat rumah)",
            "Cicilan sama terus tiap bulan (biasanya buat motor/mobil)"
        ])

    sisa_pinjaman = max(harga_barang - uang_muka, 0)
    lama_bulan = lama_tahun * 12
    bunga_bulanan = bunga_pertahun / 100 / 12

    if sisa_pinjaman > 0 and lama_bulan > 0:
        if metode_pilihan.startswith("Cicilan makin lama"):
            if bunga_bulanan > 0:
                cicilan_bulanan = sisa_pinjaman * (bunga_bulanan * (1 + bunga_bulanan) ** lama_bulan) / ((1 + bunga_bulanan) ** lama_bulan - 1)
            else:
                cicilan_bulanan = sisa_pinjaman / lama_bulan
            total_bayar = cicilan_bulanan * lama_bulan
            label_cicilan = "Cicilan Bulan Pertama"
        else:  # flat
            total_bunga = sisa_pinjaman * (bunga_pertahun / 100) * lama_tahun
            total_bayar = sisa_pinjaman + total_bunga
            cicilan_bulanan = total_bayar / lama_bulan
            label_cicilan = "Cicilan per Bulan"

        total_bunga_dibayar = total_bayar - sisa_pinjaman

        st.markdown("---")
        st.write(f"**Hasil untuk: {nama_pinjaman}**")
        c1, c2, c3 = st.columns(3)
        c1.metric(label_cicilan, rupiah(cicilan_bulanan))
        c2.metric("Total Bunga yang Dibayar", rupiah(total_bunga_dibayar))
        c3.metric("Total Semua Pembayaran", rupiah(total_bayar))

        st.caption(f"Sisa yang perlu dicicil (setelah DP): {rupiah(sisa_pinjaman)} • Lama cicilan: {lama_bulan} bulan ({lama_tahun} tahun)")

        with st.expander("💡 Tips biar ngga kebebanan cicilan"):
            st.write("""
            - Usahakan **semua cicilan digabung** (rumah + motor + lainnya) tidak lebih dari **30-35% dari gaji bulanan**.
            - **"Cicilan makin lama makin kecil"** artinya di awal kamu bayar bunga lebih banyak, tapi lama-lama porsi bunganya berkurang. Ini biasanya dipakai bank untuk cicilan rumah.
            - **"Cicilan sama terus"** artinya jumlah cicilan tiap bulan sama dari awal sampai akhir. Ini biasanya dipakai untuk cicilan motor/mobil atau pinjaman biasa.
            """)
    else:
        st.warning("Isi dulu harga barang dan lama cicilannya ya.")

# ================= TAB 3: GAJI BERSIH =================
with tab3:
    st.subheader("Berapa Gaji yang Benar-Benar Kamu Terima?")
    st.write("Gaji yang ditawarkan di kontrak biasanya masih dipotong pajak dan BPJS dulu. Isi angka di bawah buat lihat kira-kira berapa yang masuk ke rekening kamu tiap bulan.")

    col1, col2 = st.columns(2)
    with col1:
        gaji_bruto = st.number_input("Gaji sebelum dipotong apapun (Rp)", min_value=0, value=8000000, step=500000,
                                      help="Ini angka gaji yang biasa disebutkan di kontrak/lowongan kerja, sebelum dipotong pajak & BPJS")
        status_ptkp = st.selectbox("Status kamu", [
            "Belum menikah, tidak menanggung siapa-siapa",
            "Belum menikah, menanggung 1 orang (misal orang tua/adik)",
            "Menikah, belum ada tanggungan lain",
            "Menikah, menanggung 1 anak",
            "Menikah, menanggung 2 anak",
            "Menikah, menanggung 3 anak"
        ], help="Status ini mempengaruhi jumlah pajak yang dipotong dari gaji")
    with col2:
        ikut_bpjs_kesehatan = st.checkbox("Potong iuran BPJS Kesehatan", value=True,
                                           help="Biasanya 1% dari gaji, maksimal sekitar Rp120.000/bulan")
        ikut_bpjs_tk = st.checkbox("Potong iuran BPJS Ketenagakerjaan (jaminan hari tua & pensiun)", value=True,
                                    help="Biasanya sekitar 3% dari gaji")

    # PTKP tahunan (berdasarkan aturan umum yang berlaku)
    ptkp_map = {
        "Belum menikah, tidak menanggung siapa-siapa": 54_000_000,
        "Belum menikah, menanggung 1 orang (misal orang tua/adik)": 58_500_000,
        "Menikah, belum ada tanggungan lain": 58_500_000,
        "Menikah, menanggung 1 anak": 63_000_000,
        "Menikah, menanggung 2 anak": 67_500_000,
        "Menikah, menanggung 3 anak": 72_000_000,
    }
    ptkp_tahunan = ptkp_map[status_ptkp]

    gaji_bruto_tahunan = gaji_bruto * 12

    # Biaya jabatan: 5% dari bruto, maks Rp 500.000/bulan (Rp 6.000.000/tahun)
    biaya_jabatan_bulanan = min(gaji_bruto * 0.05, 500_000)
    biaya_jabatan_tahunan = biaya_jabatan_bulanan * 12

    bpjs_kesehatan_bulanan = min(gaji_bruto * 0.01, 120_000) if ikut_bpjs_kesehatan else 0
    bpjs_tk_bulanan = (gaji_bruto * 0.02 + gaji_bruto * 0.01) if ikut_bpjs_tk else 0

    total_potongan_bpjs_tahunan = (bpjs_kesehatan_bulanan + bpjs_tk_bulanan) * 12

    pkp_tahunan = max(gaji_bruto_tahunan - biaya_jabatan_tahunan - total_potongan_bpjs_tahunan - ptkp_tahunan, 0)

    # Tarif PPh 21 progresif (UU HPP)
    def hitung_pph21(pkp):
        brackets = [
            (60_000_000, 0.05),
            (250_000_000, 0.15),
            (500_000_000, 0.25),
            (5_000_000_000, 0.30),
            (float("inf"), 0.35),
        ]
        pajak = 0
        sisa = pkp
        batas_bawah = 0
        for batas_atas, tarif in brackets:
            lebar = batas_atas - batas_bawah
            kena = min(sisa, lebar)
            if kena > 0:
                pajak += kena * tarif
                sisa -= kena
            batas_bawah = batas_atas
            if sisa <= 0:
                break
        return pajak

    pph21_tahunan = hitung_pph21(pkp_tahunan)
    pph21_bulanan = pph21_tahunan / 12

    total_potongan_bulanan = bpjs_kesehatan_bulanan + bpjs_tk_bulanan + pph21_bulanan
    gaji_bersih = gaji_bruto - total_potongan_bulanan

    st.markdown("---")
    c1, c2 = st.columns(2)
    c1.metric("Uang yang Kamu Terima per Bulan", rupiah(gaji_bersih))
    c2.metric("Total yang Dipotong per Bulan", rupiah(total_potongan_bulanan))

    with st.expander("📊 Rincian potongannya apa aja"):
        st.write(f"- Iuran BPJS Kesehatan: {rupiah(bpjs_kesehatan_bulanan)}")
        st.write(f"- Iuran BPJS Ketenagakerjaan: {rupiah(bpjs_tk_bulanan)}")
        st.write(f"- Pajak penghasilan: {rupiah(pph21_bulanan)}")

    st.caption("⚠️ Ini perkiraan kasar untuk gambaran umum, bukan angka pasti dari perusahaan/kantor pajak. Setiap perusahaan bisa punya aturan tunjangan/potongan yang sedikit berbeda.")

st.markdown("---")
st.caption("Dibuat dengan ❤️ menggunakan Streamlit — 100% gratis, tanpa API berbayar")

# SIMUTEH – Sistem Pemeriksaan Mutu Daun Teh Berbasis Citra
Evaluasi Hasil Belajar Praktikum Computer Vision (Pertemuan 1 – 4)  
Program Studi Teknik Informatika, Fakultas Sains dan Teknologi  
Universitas Muhammadiyah Sukabumi (UMMI)

---

## Identitas Mahasiswa
- **Nama**: Mochamad Rizki Ramdani
- **NIM**: 2330511070
- **SEED**: 1070 (4 digit terakhir NIM)
- **Tag Rilis**: `v0.1-praproses`

---

## Deskripsi Singkat Kasus
SIMUTEH dirancang untuk membantu kelompok tani teh rakyat di Kabupaten Sukabumi dalam menyortir mutu daun teh berdasarkan tingkat keparahan penyakit cacar daun (*blister blight* yang disebabkan jamur *Exobasidium vexans*). Sistem memproses foto daun di atas nampan sortir dari kamera telepon genggam untuk menghasilkan rekomendasi kelas mutu (**Sehat**, **Bercak Ringan**, atau **Bercak Berat**) secara objektif di bawah variasi pencahayaan lapangan (normal, gelap, terang, kontras rendah, bayangan).

---

## Struktur Repositori
```text
simuteh-2330511070/
├── data/
│   └── sintetis/              # Dataset citra sintetis (60 citra x 4 varian + label.csv)
│       ├── citra/             # Citra masukan lapangan (gangguan cahaya + derau)
│       ├── bersih/            # Citra acuan tanpa gangguan
│       ├── mask_daun/         # Mask biner area daun
│       └── mask_bercak/       # Mask biner area bercak
├── notebook/
│   ├── B1_lingkungan.ipynb    # Bagian 1: Verifikasi lingkungan & formulasi masalah
│   ├── B2_citra_warna.ipynb   # Bagian 2: Lembar hitung optik, ruang warna & KB kanal
│   ├── B3_histogram.ipynb     # Bagian 3: Diagnosis histogram & perbaikan titik
│   ├── B4_penapisan.ipynb     # Bagian 4: Konvolusi spasial, penapisan derau & PSNR
│   └── B5_praproses.ipynb     # Bagian 5: Integrasi rangkaian praproses & justifikasi
├── src/
│   ├── buat_dataset_sintetis.py # Pembangkit dataset sintetis (SEED=1070)
│   ├── utils_cv.py              # Fungsi bantu (baca, tampil, kontras_bercak, statistik)
│   └── praproses.py             # Modul rangkaian praproses SIMUTEH
├── hasil/                     # Seluruh berkas keluaran (.csv, .png, .json)
├── laporan/                   # Laporan PDF dan slide presentasi PPTX
├── requirements.txt           # Daftar pustaka Python yang dibutuhkan
└── README.md                  # Dokumentasi reprodusibilitas proyek
```

---

## Cara Menjalankan Proyek

### 1. Persiapan Lingkungan & Pustaka
Pastikan Python versi 3.10 atau yang lebih baru telah terpasang. Buat dan aktifkan virtual environment:
```bash
python -m venv .venv
# Windows (PowerShell):
.\.venv\Scripts\Activate.ps1
# Linux/macOS:
source .venv/bin/activate
```
Pasang seluruh dependensi:
```bash
pip install -r requirements.txt
```

### 2. Pembangkitan Dataset Sintetis
Jalankan generator dataset dengan SEED 1070:
```bash
python src/buat_dataset_sintetis.py
```
Perintah ini membangkitkan 60 citra sintetis berukuran 640×480 piksel beserta mask daun, mask bercak, dan `label.csv`.

### 3. Eksekusi Notebook
Jalankan Jupyter Notebook dan eksekusi secara berurutan (*Restart & Run All*):
1. `notebook/B1_lingkungan.ipynb`
2. `notebook/B2_citra_warna.ipynb`
3. `notebook/B3_histogram.ipynb`
4. `notebook/B4_penapisan.ipynb`
5. `notebook/B5_praproses.ipynb`

---

## Ringkasan Hasil Evaluasi (B1 s.d. B5)

### Bagian 1: Lingkungan Kerja & Formulasi Masalah
- **Problem Statement**: Bagi kelompok tani teh di Sukabumi yang menghadapi ketidakseragaman sortir manual daun akibat pencahayaan lapangan, kami membangun SIMUTEH yang menerima foto daun teh dari telepon genggam dan menghasilkan estimasi persentase luas bercak serta kelas mutu, sehingga proses sortir menjadi lebih konsisten, cepat, dan adil.
- **Responsible AI**: Menghapus metadata EXIF koordinat GPS kebun dan melarang foto yang memuat wajah petani.

### Bagian 2: Pembentukan Citra & Ruang Warna
- **Lembar Hitung Optik**: Pada resolusi kerja 640×480, jarak pemotretan maksimum agar bercak 5 mm tetap berukuran $\ge 10$ piksel adalah **±23 cm**.
- **Kanal Terpilih**: **Kanal R (Red)** dan **Kanal H (Hue)** terbukti secara konsisten menghasilkan Kontras Bercak (KB) tertinggi di semua kondisi pencahayaan (rata-rata KB R > 7.0), karena bercak cokelat-kekuningan memiliki perbedaan nilai komponen merah yang sangat kontras terhadap daun hijau pekat.

### Bagian 3: Histogram & Perbaikan Citra
- **Diagnosis Histogram**: Mengidentifikasi karakteristik 5 kondisi (normal, gelap, terang, kontras rendah, bayangan).
- **CLAHE Kanal V**: Mengaplikasikan CLAHE pada kanal V (Value) di ruang HSV berhasil memperbaiki pencahayaan area bayangan tanpa merusak rona warna alami daun (*zero color shift*).

### Bagian 4: Konvolusi & Penapisan Spasial
- **Penapis Terpilih**: Penapis **Median 3×3** terbukti paling efektif meredam derau sensor bawaan (menaikkan PSNR rata-rata **+6.9 dB**) dan unggul telak pada derau impulsif (PSNR **48.25 dB**), dengan tetap mempertahankan integritas bercak kecil kelas ringan ($dI = 28.73$).

### Bagian 5: Integrasi Rangkaian Praproses
- **Parameter Baku Final (`hasil/param_praproses.json`)**:
  ```json
  {
    "lebar": 640,
    "gamma": 1.0,
    "clahe_clip": 2.0,
    "clahe_tile": 8,
    "penapis": "median",
    "kernel": 3,
    "sigma": 1.0,
    "tajam_k": 0.0
  }
  ```
- **Kinerja Praproses pada 40 Citra Berbercak**:
  - Rata-rata KB sebelum praproses: **7.06**
  - Rata-rata KB sesudah praproses: **9.21** (Peningkatan rata-rata: **+30.75%**)
  - Peningkatan tertinggi dicapai pada kondisi **bayangan (+56.18%)** dan **gelap (+53.27%)**.
- **Uji Bercak Palsu pada Daun Sehat**:
  - Simpangan baku ($\sigma$) area daun pada kondisi bayangan, gelap, normal, dan kontras rendah mengalami penurunan (permukaan daun lebih homogen bersih). Tidak memunculkan bercak semu (*false positive*).

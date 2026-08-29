# RPS Generator (DOCX from JSON)

Proyek ini adalah *tool* otomatisasi berbasis Python yang digunakan untuk menghasilkan (generate) dokumen Rencana Pembelajaran Semester (RPS) dalam format Microsoft Word (`.docx`). *Tool* ini mengambil data dari file `.json` dan mengisikannya ke dalam template dokumen `.docx`.

Saat ini repo memuat RPS lengkap untuk **54 mata kuliah Program Studi S1 Sistem Informasi ITEKES Bintang Persada**, semester 1 sampai 8.

> **Aturan paling penting:** CPL yang dibebankan pada sebuah mata kuliah **tidak boleh dipilih sendiri**. Penentunya adalah Tabel 3.2 Buku Kurikulum. Lihat [Menyusun RPS baru](#menyusun-rps-baru).

## Fitur Utama

1. **Auto-Fill Template**: Secara otomatis mengganti teks *placeholder* di dokumen (seperti `{kode_mk}`, `{cpmk[0].deskripsi}`) dengan data dari struktur JSON.
2. **Support Nested & List Data**: Mendukung data bertingkat di dalam JSON (misalnya mengambil data dari struktur `meta`) dan menggabungkan data list menjadi multi-baris (seperti daftar bahan kajian).
3. **Slot cadangan dibuang otomatis**: Template menyediakan lebih banyak baris daripada yang umumnya dibutuhkan (mis. 20 baris CPL). Baris, kolom, dan paragraf yang seluruh placeholder-nya tidak terisi dibuang saat pengisian, sehingga tidak tercetak sebagai `{cpl_prodi[19].kode}`.
4. **Pengaman bagian kosong**: `tools/edit_rps.py` keluar dengan status 1 dan mencetak peringatan bila bagian wajib (`detail`, `cpl_prodi`, `cpmk`, `sub_cpmk`, `pustaka_utama`) kosong sama sekali di dokumen hasil — pertanda nama field JSON tidak cocok dengan template.
5. **Tiga matriks penjaminan mutu**: Korelasi CPMK×Sub-CPMK, Korelasi CPMK×penilaian, dan Korelasi CPL×Sub-CPMK (format Panduan KPT 2024) dibangun otomatis dari data dan diverifikasi agar berjumlah tepat 100%.
6. **Otomatisasi Tanda Tangan (Image Injection)**:
   - Memasukkan gambar tanda tangan langsung ke dokumen jika terdapat placeholder `{dosen_sign}` (ukuran normal 1.0 inch) atau `{dosen_sign_small}` (ukuran kecil 0.5 inch).
   - Mengubah properti gambar di Word secara otomatis agar berada pada posisi **"In Front of Text"**.
   - Mendukung transparansi gambar PNG (dikonversi dengan benar menggunakan *Pillow*).
7. **Batch Processing**: Bisa memproses banyak file `.json` sekaligus dari sebuah folder menggunakan `tools/run_batch.py`.
8. **Image Normalization**: Menggunakan *Computer Vision* (`OpenCV`) untuk menyeragamkan resolusi, ketebalan goresan pena, dan warna semua tanda tangan dosen.
9. **Data Correction Tool**: Menyediakan *script* `tools/fix_nuptk.py` untuk memeriksa dan mengoreksi data NUPTK dosen secara otomatis di seluruh file JSON berdasarkan *mapping* terpusat.

## Persyaratan Sistem

- **Python 3.x**
- **[uv](https://github.com/astral-sh/uv)** (Direkomendasikan untuk manajemen environment yang sangat cepat)
- **Microsoft Word** — hanya dibutuhkan untuk konversi DOCX ke PDF (`tools/docx_to_pdf_folder.py` memakai automation Word lewat `comtypes`).

## Instalasi

```powershell
# Buat virtual environment
uv venv

# Aktifkan virtual environment (opsional jika selalu pakai 'uv run')
.venv\Scripts\activate

# Instal dependensi
uv pip install -r requirements.txt
```

*Library* utama: `python-docx` (baca/tulis DOCX), `Pillow` + `opencv-python` (tanda tangan), `comtypes` (Word automation), `pymupdf` (baca PDF acuan dan verifikasi hasil), `pdf2docx` (konversi PDF ke DOCX).

## Panduan Penggunaan

### 1. Menghasilkan Satu File RPS

```powershell
uv run python tools/edit_rps.py -i "input/rps_json/sem1.1/TSI1107_Agama.json" -o "outputs/rps/sem1.1/TSI1107_Agama.docx"
```

**Opsi:**
- `-o "folder/hasil.docx"`: lokasi output. Bila tidak diisi, hasil disimpan ke `output/<nama_file>.docx`.
- `--template "template/RPS_Template.docx"`: template lain (default `template/RPS_MK_TSI0000.docx`).

### 2. Menghasilkan RPS Secara Massal

```powershell
# Memproses seluruh input/rps_json/** ke outputs/rps/** dengan struktur folder yang sama
uv run python tools/run_batch.py rps

# Dari folder tertentu
uv run python tools/run_batch.py rps -f input/rps_json/sem2

# Konversi seluruh hasil RPS ke PDF
uv run python tools/run_batch.py pdf-rps
```

Argumen `mode` wajib diisi: `rps`, `sap`, `kontrak`, `pdf-rps`, `pdf-sap`,
`pdf-kontrak`, atau `all`. Jalur input/output diatur di `generate.conf`.

### 3. Konversi ke PDF

```powershell
uv run python tools/docx_to_pdf_folder.py -i outputs/rps/sem2
```

### 4. Memeriksa Hasil

```powershell
# Periksa konsistensi JSON sebelum digenerate
uv run python tools/validasi_rps.py "input/rps_json/sem*/*.json" --ringkas

# Periksa placeholder yang tersisa pada dokumen hasil
uv run python tools/check_placeholders.py "outputs/rps/sem2/*.docx"
```

`tools/validasi_rps.py` memeriksa rantai CPL→CPMK→Sub-CPMK, kesesuaian rumusan CPL dengan Buku Kurikulum, total bobot 100%, konsistensi ketiga matriks, kapasitas template, dan format kolom tabel mingguan. Status keluar 1 bila ada temuan.

### 5. Menyeragamkan Gambar Tanda Tangan

```powershell
uv run python tools/normalize_signs.py
```

### 6. Memperbaiki Data NUPTK

```powershell
uv run python tools/fix_nuptk.py
```

## Menyusun RPS baru

1. Buka `prompt/rps.md` — memuat skema JSON lengkap, aturan penulisan, batas kapasitas, dan checklist.
2. **Tentukan CPL dari Tabel 3.2 Buku Kurikulum**, bukan dari penilaian sendiri. Rumusan tiap CPL tersedia siap pakai di `cpl_resmi.json` (dihasilkan `tools/cpl_resmi.py`).
3. Setelah JSON jadi, periksa dengan `tools/validasi_rps.py`, lalu generate.

Untuk memeriksa apakah CPL sebuah RPS sudah sesuai kurikulum:

```powershell
uv run python tools/selaraskan_cpl_kurikulum.py "input/rps_json/sem2/*.json" --periksa
```

Alur lengkap membangun template dan meningkatkan JSON ada di **[`tools/README.md`](tools/README.md)**.

## Struktur File / Folder

| Jalur | Isi |
|---|---|
| `tools/edit_rps.py` | Generator utama RPS: mengisi template dari JSON |
| `tools/edit_sap.py`, `tools/edit_konkul.py` | Generator SAP dan Kontrak Kuliah |
| `tools/run_batch.py` | Pemroses massal seluruh folder input |
| `tools/docx_to_pdf_folder.py` | Konversi DOCX ke PDF lewat Word |
| `tools/check_placeholders.py` | Deteksi placeholder tersisa pada dokumen hasil |
| `tools/normalize_signs.py`, `tools/fix_nuptk.py` | Utilitas tanda tangan dan koreksi NUPTK |
| `template/` | Template Word: `RPS_MK_TSI0000.docx`, `SAP_MK_TSI0000.docx`, `Kontrak_Kuliah_MK_TSI0000.docx` |
| `generate.conf` | Pemetaan folder input dan output |
| `cpl_resmi.json` | 33 CPL resmi hasil ekstraksi Buku Kurikulum |
| `input/rps_json/semN/` | Sumber data RPS per semester |
| `input/sap_json/`, `input/kontrak_json/` | Sumber data SAP dan Kontrak Kuliah |
| `outputs/rps/semN/` | Hasil generate (DOCX dan PDF); tidak dilacak git |
| `prompt/rps.md`, `prompt/sap.md` | Prompt penyusunan JSON RPS dan SAP |
| `tools/` | Seluruh skrip Python: generator, pembangun template, peningkatan JSON, validator — lihat `tools/README.md` |
| `isian/` | Lembar isian untuk diisi dosen (mis. Bab pustaka per minggu) |
| `materi-rps/` | Dokumen acuan: Buku Kurikulum, contoh RPS, panduan BPM dan KPT |
| `sign/` | Gambar tanda tangan dosen (tidak dilacak git) |
| `requirements.txt` | Daftar dependensi paket Python |

## Dokumen acuan

Keempat dokumen ini menjadi dasar seluruh format dan isi RPS, dan **dilacak git** karena skrip membacanya langsung:

| Dokumen | Dipakai untuk |
|---|---|
| `materi-rps/Buku Kurikulum S1 Sistem Informasi - 20260508.docx` | rumusan CPL resmi (§3.2), pemetaan CPL×MK (Tabel 3.2), daftar MK (Tabel 3.1), bahan kajian (Bab IV) |
| `materi-rps/KFR 4560 Cosmeceutical.docx` | acuan format tabel RPS |
| `materi-rps/1. Panduan terkait Pembelajaran/PANDUAN PENYUSUNAN RPS ITEKES BP 2023 (1).pdf` | komponen wajib RPS, kode metode pembelajaran, singkatan TM/PT/BM |
| `materi-rps/1. Panduan terkait Pembelajaran/Buku-Panduan-KPT-2024...pdf` | format band Korelasi CPL terhadap Sub-CPMK (hal. 118) |

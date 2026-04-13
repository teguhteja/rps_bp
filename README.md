# RPS Generator (DOCX from JSON)

Proyek ini adalah *tool* otomatisasi berbasis Python yang digunakan untuk menghasilkan (generate) dokumen Rencana Pembelajaran Semester (RPS) dalam format Microsoft Word (`.docx`). *Tool* ini mengambil data dari file `.json` dan mengisikannya ke dalam template dokumen `.docx`.

## Fitur Utama

1. **Auto-Fill Template**: Secara otomatis mengganti teks *placeholder* di dokumen (seperti `{kode_mk}`, `{cpmk[0].deskripsi}`) dengan data dari struktur JSON.
2. **Support Nested & List Data**: Mendukung data bertingkat di dalam JSON (misalnya mengambil data dari struktur `meta`) dan menggabungkan data list menjadi multi-baris (seperti daftar bahan kajian).
3. **Otomatisasi Tanda Tangan (Image Injection)**: 
   - Memasukkan gambar tanda tangan langsung ke dokumen jika terdapat placeholder `{dosen_sign}` (ukuran normal 1.0 inch) atau `{dosen_sign_smal}` (ukuran kecil 0.5 inch).
   - Mengubah properti gambar di Word secara otomatis agar berada pada posisi **"In Front of Text"**.
   - Mendukung transparansi gambar PNG (dikonversi dengan benar menggunakan *Pillow*).
4. **Batch Processing**: Bisa memproses banyak file `.json` sekaligus dari sebuah folder menggunakan `run_batch.py`.
5. **Image Normalization**: Menggunakan *Computer Vision* (`OpenCV`) untuk menyeragamkan resolusi, ketebalan goresan pena, dan warna semua tanda tangan dosen agar persis sama dengan referensi utama (contoh: `venny.png`).
6. **Data Correction Tool**: Menyediakan *script* `fix_nuptk.py` untuk memeriksa dan mengoreksi data NUPTK dosen secara otomatis di seluruh file JSON berdasarkan *mapping* terpusat.

## Persyaratan Sistem

- **Python 3.x**
- **[uv](https://github.com/astral-sh/uv)** (Direkomendasikan untuk manajemen environment yang sangat cepat)

## Instalasi

1. Pastikan `uv` sudah terinstal di sistem Anda.
2. Clone atau buka folder proyek ini.
3. Buat environment baru dan instal dependensi dari file `requirements.txt`:

```powershell
# Buat virtual environment
uv venv

# Aktifkan virtual environment (opsional jika selalu pakai 'uv run')
.venv\Scripts\activate

# Instal dependensi
uv pip install -r requirements.txt
```

*Library* utama yang digunakan meliputi: `python-docx`, `Pillow`, `opencv-python`, dan `numpy`.

## Panduan Penggunaan

### 1. Menghasilkan Satu File RPS
Gunakan `edit_rps.py` untuk mengonversi satu file JSON ke dalam format DOCX.

```powershell
uv run python edit_rps.py -i "input/nama_file.json"
```
*Catatan:* Hasil secara otomatis akan disimpan di folder `output/` dengan nama yang sama (misal `output/nama_file.docx`).

**Opsi Tambahan:**
- `-o "custom_folder/hasil.docx"`: Tentukan lokasi spesifik output.
- `--template "RPS_Template.docx"`: Gunakan file template `.docx` yang berbeda (default: `RPS_MK_TSI0000.docx`).

### 2. Menghasilkan RPS Secara Massal (Batch)
Gunakan `run_batch.py` untuk memproses seluruh folder JSON.

```powershell
# Memproses semua file .json di folder 'input' dan menyimpan ke 'output'
uv run python run_batch.py

# Memproses dari folder input tertentu ke folder output tertentu
uv run python run_batch.py -f input_3 -o output_3
```

### 3. Menyeragamkan Gambar Tanda Tangan
Jika Anda memiliki gambar tanda tangan baru di folder `sign/` dan ingin menyeragamkan ukuran, warna tinta, dan ketebalan garisnya:

```powershell
uv run python normalize_signs.py
```
Script ini akan membaca file `venny.png` sebagai patokan (target) dan menyesuaikan file `.png` lainnya di dalam folder `sign/`.

### 4. Memperbaiki Data NUPTK
Jika ada ketidaksesuaian data NUPTK dosen di banyak file JSON, Anda bisa memperbaikinya sekaligus:

```powershell
uv run python fix_nuptk.py
```
*Tool* ini akan membaca data dosen dari properti `meta.dosen_pengampu` di setiap file JSON yang ada di folder input (seperti `input_3` s.d. `input_8`) dan menyesuaikan nilai `nuptk` berdasarkan *dictionary mapping* yang sudah disetel.

## Struktur File / Folder
- `edit_rps.py` : Skrip utama generator DOCX.
- `run_batch.py` : Skrip otomatisasi folder/batch.
- `normalize_signs.py` : Skrip OpenCV untuk normalisasi tanda tangan.
- `fix_nuptk.py` : Skrip utilitas koreksi NUPTK JSON.
- `RPS_MK_TSI0000.docx` : Template Word standar.
- `input_*/` : Kumpulan folder yang berisi file input `.json`.
- `output/` : Folder default penyimpanan hasil *generate*.
- `sign/` : Folder yang berisi file gambar `.png` untuk tanda tangan dosen.
- `requirements.txt` : Daftar dependensi paket Python.
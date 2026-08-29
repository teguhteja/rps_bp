# Kerangka Buku Ajar — Business Intelligence

**Mata kuliah:** TSI3752 Business Intelligence · 3 SKS (T3 P0) · Semester 7
**Status:** MK Penciri · Kelompok Keilmuan Data dan Kecerdasan Buatan
**Pengampu:** Ida Bagus Teguh Teja Murti, S.Kom., M.Kom.

---

## Posisi buku ini

Seluruh pustaka utamanya asing dan berat: Kimball & Ross (*The Data Warehouse
Toolkit*), Inmon (*Building the Data Warehouse*), Few (*Show Me the Numbers*),
Kaplan & Norton (*The Balanced Scorecard*). Semuanya rujukan kelas dunia, tetapi
tidak satu pun ditulis sebagai buku ajar semester 7 berbahasa Indonesia.

Materi MK ini sangat praktis — Power BI, DAX, ETL, dashboard. Untuk materi semacam
ini, buku berbahasa Indonesia dengan tangkapan layar, dataset lokal, dan langkah
terbimbing jauh lebih terpakai daripada terjemahan buku teori.

Buku ini juga menopang Profil Lulusan **PL-05 Data Analyst** secara langsung.

## Sasaran pembaca

1. Mahasiswa S1 Sistem Informasi semester 7
2. Mahasiswa MK serumpun: Analitik dan Visualisasi Data, Big Data, Sistem Pendukung
   Keputusan
3. Praktisi yang menyiapkan dashboard di organisasi — pasar di luar kampus

## Struktur

10 bab mengikuti 8 bahan kajian RPS, dengan bab praktikum dipisah agar terbimbing.
Perkiraan 200–240 halaman karena banyak tangkapan layar.

---

## Bab 1 — Konsep dan Arsitektur Business Intelligence
*Minggu 1 · Bahan kajian 1*

- Definisi BI dan evolusinya dari pelaporan statis ke analitik
- Arsitektur BI: sumber data → ETL → data warehouse → OLAP → penyajian
- Peran BI dalam pengambilan keputusan organisasi
- Perbedaan BI, analitik data, dan ilmu data

## Bab 2 — Data Warehouse: Konsep dan Arsitektur
*Minggu 2 · Bahan kajian 2*

- Karakteristik data warehouse: berorientasi subjek, terpadu, rentang waktu, non-volatil
- OLTP versus OLAP — perbandingan sistematis
- Pendekatan Inmon (top-down) versus Kimball (bottom-up)
- Data mart dan kapan memilihnya

## Bab 3 — Pemodelan Dimensional
*Minggu 3 · Bahan kajian 2*

- Tabel fakta: ukuran, kunci asing, granularitas
- Tabel dimensi: atribut, hierarki
- Skema bintang dan skema snowflake — kelebihan dan konsekuensinya
- Degenerate dimension, slowly changing dimension
- **Latihan terbimbing:** merancang skema bintang untuk data penjualan

## Bab 4 — Proses ETL: Ekstraksi dan Transformasi
*Minggu 4 · Bahan kajian 3*

- Sumber data: basis data operasional, berkas datar, API
- Teknik ekstraksi: penuh dan inkremental
- Transformasi: pembersihan, penyeragaman, penggabungan, agregasi
- Penanganan data kotor dan nilai hilang

## Bab 5 — Proses ETL: Pemuatan dan Operasional
*Minggu 5 · Bahan kajian 3*

- Strategi pemuatan: batch dan inkremental
- Penjadwalan: cron, Apache Airflow
- Pemantauan log, penanganan galat, dan pemulihan
- Kualitas data dan pengujian pipeline

## Bab 6 — OLAP dan Analisis Multidimensional
*Minggu 6 · Bahan kajian 4*

- Kubus data dan operasinya: slice, dice, drill-down, roll-up, pivot
- MDX dasar
- SQL analitik: GROUP BY CUBE, ROLLUP, GROUPING SETS
- Perbandingan MOLAP, ROLAP, HOLAP

## Bab 7 — SQL Analitik Lanjutan
*Minggu 7 · Bahan kajian 4*

- Window function: OVER, PARTITION BY, ORDER BY
- Fungsi peringkat: ROW_NUMBER, RANK, DENSE_RANK
- Fungsi geser: LAG, LEAD
- Agregat berjalan dan rata-rata bergerak
- **Latihan:** analisis tren penjualan bulanan

## Bab 8 — Membangun Dashboard dengan Power BI
*Minggu 9–10 · Bahan kajian 8*

- Pemasangan, antarmuka, dan koneksi sumber data
- Visual dasar: batang, garis, lingkaran, peta — dan kapan memakai yang mana
- Penapis, slicer, dan penapisan silang
- **DAX:** SUM, AVERAGE, CALCULATE, FILTER, dan time intelligence
- Bookmark dan navigasi laporan

> Bab dengan tangkapan layar terbanyak. Sertakan **dataset latihan yang bisa diunduh**
> agar pembaca mengikuti langkah demi langkah, bukan sekadar membaca.

## Bab 9 — Desain Dashboard, KPI, dan Balanced Scorecard
*Minggu 11–12 · Bahan kajian 5 dan 6*

- Prinsip desain dashboard yang efektif — saripati Few (2012)
- Kesalahan lazim: grafik lingkaran berlebihan, 3D, warna tanpa makna
- KPI: indikator pendahulu dan pengikut, indikator lampu lalu lintas
- Balanced Scorecard: perspektif keuangan, pelanggan, proses internal, pembelajaran
- Pemetaan strategi dan penurunannya menjadi ukuran

## Bab 10 — Proyek BI Menyeluruh
*Minggu 13–15 · Bahan kajian 7 dan 8*

- Pemilihan studi kasus: penjualan, keuangan, atau logistik
- Identifikasi sumber data dan perancangan skema
- Implementasi ETL dengan SSIS, Pentaho, atau Talend
- Pembuatan dashboard dan penyusunan rekomendasi bisnis
- Presentasi hasil kepada pemangku kepentingan
- **Satu proyek lengkap dari awal sampai akhir** sebagai contoh acuan

> Pengantar data mining (bahan kajian 7) ditempatkan di sini sebagai pembuka arah
> lanjutan, bukan bab tersendiri — sesuai porsinya di RPS.

---

## Elemen pedagogis tiap bab

| Elemen | Isi |
|---|---|
| Capaian pembelajaran | Sub-CPMK dari RPS |
| Langkah terbimbing | Prosedur bernomor dengan tangkapan layar |
| Dataset latihan | Berkas yang dapat diunduh, konteks Indonesia |
| Kesalahan lazim | Kekeliruan yang sering terjadi beserta perbaikannya |
| Latihan mandiri | Selaras dengan indikator penilaian RPS |
| Rangkuman dan evaluasi | Sesuai bobot minggu di RPS |

## Pustaka acuan

- Kimball, R., & Ross, M. (2013). *The Data Warehouse Toolkit* (3rd ed.)
- Ferrari, A., & Russo, M. (2019). *Analyzing Data with Power BI and Power Pivot*
- Few, S. (2012). *Show Me the Numbers*
- Inmon, W. H. (2005). *Building the Data Warehouse* (4th ed.)
- Kaplan, R. S., & Norton, D. P. (1996). *The Balanced Scorecard*

## Catatan penggarapan

**Risiko terbesar buku ini: cepat usang.** Antarmuka Power BI berubah beberapa kali
setahun, sehingga tangkapan layar Bab 8 paling cepat kedaluwarsa. Dua cara meredamnya:

1. Tekankan **konsep** di Bab 1–7 dan 9 — bagian ini tahan lama. Bab 8 dan 10 yang
   bergantung perkakas dibuat sebagai bagian yang mudah diperbarui.
2. Sebutkan **versi perkakas** secara eksplisit di awal Bab 8, dan sediakan berkas
   pendamping daring untuk pembaruan langkah.

Dataset latihan sebaiknya disiapkan sejak awal dan dipakai konsisten dari Bab 3
sampai Bab 10, sehingga pembaca membangun satu solusi utuh sepanjang buku alih-alih
mengerjakan contoh yang terputus-putus.

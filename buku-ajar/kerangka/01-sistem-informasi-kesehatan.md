# Kerangka Buku Ajar — Sistem Informasi Kesehatan

**Mata kuliah:** TSI1433 Sistem Informasi Kesehatan · 2 SKS (T2 P0) · Semester 4
**Status:** MKKP — khusus prodi kesehatan, dapat diambil lintas prodi
**Pengampu:** Ida Bagus Teguh Teja Murti, S.Kom., M.Kom.

---

## Mengapa buku ini lebih dulu

ITEKES Bintang Persada punya fakultas kesehatan dan fakultas teknologi dalam satu
institusi. Buku ini adalah satu-satunya kandidat yang melayani keduanya sekaligus:
mahasiswa SI belajar domain kesehatan, mahasiswa kesehatan belajar sistem informasinya.

Isinya juga paling sulit ditemukan di buku asing. Tan (2020) dan Wager dkk. (2021)
membahas *health informatics* dalam konteks Amerika — tidak memuat BPJS, INA-CBG,
VClaim, e-Puskesmas, SISRUTE, PIS-PK, maupun UU Kesehatan No. 17/2023. Justru itulah
yang diuji di RPS.

## Sasaran pembaca

1. Mahasiswa S1 Sistem Informasi semester 4 (pembaca utama)
2. Mahasiswa prodi kesehatan yang mengambil MK ini sebagai MKKP
3. Praktisi rekam medis dan staf IT rumah sakit/puskesmas — pasar di luar kampus

## Struktur

10 bab, mengikuti 9 bahan kajian RPS dengan bab pembuka tambahan. Perkiraan
160–200 halaman.

---

## Bab 1 — Konsep Dasar Sistem Informasi Kesehatan
*Minggu 1 · Bahan kajian 1*

- Definisi sistem informasi kesehatan dan posisinya dalam sistem kesehatan nasional
- Lima komponen: data, informasi, teknologi, manusia, proses
- Peran SI dalam mutu layanan, efisiensi, dan pengambilan keputusan klinis
- Perbedaan data klinis, administratif, dan epidemiologis

> **Kotak konteks:** mengapa rumah sakit di Indonesia wajib punya SIMRS
> (Permenkes No. 82 Tahun 2013).

## Bab 2 — Ekosistem Layanan Kesehatan Indonesia
*Minggu 2 · Bahan kajian 1*

- Jenjang layanan: FKTP, FKRTL, sistem rujukan berjenjang
- JKN dan BPJS Kesehatan: kepesertaan, klaim, verifikasi
- Peran Kementerian Kesehatan dan Dinas Kesehatan daerah
- Aliran data dari fasilitas ke tingkat nasional

> **Bab yang paling menentukan.** Tanpa memahami ekosistem ini, seluruh pembahasan
> teknis di bab berikutnya kehilangan konteks. Berikan porsi halaman yang cukup.

## Bab 3 — Standar Klasifikasi: ICD-10 dan ICD-9-CM
*Minggu 3 · Bahan kajian 2*

- Mengapa klasifikasi diperlukan: keseragaman, statistik, pembiayaan
- Struktur kode ICD-10 (bab, blok, kategori, subkategori)
- ICD-9-CM untuk tindakan medis
- Latihan pengodean dari ringkasan rekam medis
- Kaitan kode dengan INA-CBG dan besaran klaim

## Bab 4 — Standar Pertukaran Data dan Rekam Medis Elektronik
*Minggu 4 · Bahan kajian 2*

- HL7 v2 dan v3: struktur pesan, segmen, tipe kejadian
- FHIR: resource, RESTful API, mengapa menjadi arah baru
- Rekam Medis Elektronik: definisi, komponen, manfaat, hambatan penerapan
- Permenkes No. 24 Tahun 2022 tentang Rekam Medis (kewajiban RME)

## Bab 5 — Sistem Informasi Rumah Sakit (SIMRS)
*Minggu 5–6 · Bahan kajian 3*

- Definisi, tujuan, dan dasar hukum SIMRS
- Arsitektur: client-server, berbasis web, cloud — beserta konsekuensinya
- Modul fungsional: pendaftaran, rawat jalan, rawat inap, farmasi, laboratorium,
  radiologi, kasir, akuntansi
- Alur data pasien dari pendaftaran hingga pemulangan
- Integrasi: BPJS (VClaim, INA-CBG), LIS, sistem farmasi, e-Puskesmas
- Mekanisme integrasi: API, HL7, pertukaran berkas

## Bab 6 — Sistem Informasi Puskesmas dan FKTP
*Minggu 7 · Bahan kajian 4*

- e-Puskesmas: modul kunjungan, kohort, obat, surveilans, PIS-PK
- Pelaporan berjenjang ke Dinas Kesehatan
- Perbedaan karakteristik SI puskesmas dan rumah sakit
- Kendala khas FKTP: keterbatasan jaringan, SDM, dan perangkat

## Bab 7 — Privasi, Keamanan, dan Manajemen Data Pasien
*Minggu 9 · Bahan kajian 5*

- Manajemen data pasien: identifikasi tunggal, kualitas data, retensi
- Rahasia medis menurut UU Kesehatan No. 17 Tahun 2023
- UU No. 27 Tahun 2022 tentang Perlindungan Data Pribadi dan implikasinya
- Kontrol akses berbasis peran, jejak audit, enkripsi
- Kasus kebocoran data kesehatan dan pelajarannya

> **Bab dengan nilai jual tertinggi di luar kampus.** Staf IT fasilitas kesehatan
> membutuhkan panduan praktis ini dan hampir tidak tersedia dalam bahasa Indonesia.

## Bab 8 — Telemedicine dan e-Health
*Minggu 10 · Bahan kajian 6*

- Definisi dan jenis telemedicine: konsultasi, tele-radiologi, tele-EKG
- Platform Indonesia: Halodoc, Alodokter, SISRUTE
- Permenkes tentang telemedicine dan batas kewenangannya
- Transformasi digital layanan kesehatan pasca-pandemi

## Bab 9 — Interoperabilitas dan Regulasi
*Minggu 11–12 · Bahan kajian 7 dan 8*

- Tingkat interoperabilitas: teknis, sintaksis, semantis, organisasional
- Standar: HL7, FHIR, DICOM
- SISRUTE dan integrasi antar fasilitas
- Peta regulasi: Permenkes SIMRS, RME, telemedicine; cetak biru transformasi
  digital kesehatan Kemenkes

## Bab 10 — Studi Kasus dan Perancangan Solusi
*Minggu 13–15 · Bahan kajian 9*

- Metode: pemilihan kasus, identifikasi masalah, analisis kesenjangan
- Masalah yang lazim: proses manual, sistem tidak terintegrasi, pelaporan lambat
- Perancangan usulan: arsitektur, modul, standar data, keamanan, interoperabilitas
- Struktur laporan dan teknik presentasi
- **Dua studi kasus lengkap:** satu rumah sakit, satu puskesmas

---

## Elemen pedagogis tiap bab

| Elemen | Isi |
|---|---|
| Capaian pembelajaran | Salin Sub-CPMK yang relevan dari RPS |
| Kotak regulasi | Pasal atau permenkes yang mengikat topik bab |
| Studi kasus singkat | Fasilitas kesehatan di Bali |
| Latihan | Selaras dengan indikator penilaian RPS minggu terkait |
| Rangkuman | 5–8 butir |
| Soal evaluasi | Pilihan ganda dan esai, setara bobot minggu di RPS |

## Pustaka acuan

Sudah tercantum di RPS dan tinggal dipakai:

- Tan, J. (2020). *Healthcare information systems and informatics*
- Wager, K. A., Lee, F. W., & Glaser, J. P. (2021). *Health care information systems*
- Kementerian Kesehatan RI. (2023). *Pedoman Sistem Informasi Rumah Sakit*
- UU No. 17 Tahun 2023 tentang Kesehatan
- UU No. 27 Tahun 2022 tentang Perlindungan Data Pribadi

**Perlu ditambahkan sendiri:** Permenkes No. 24/2022 (RME), Permenkes No. 82/2013
(SIMRS), pedoman VClaim dan INA-CBG dari BPJS Kesehatan, serta cetak biru
transformasi digital kesehatan Kemenkes 2024–2029.

## Catatan penggarapan

Bab 2, 5, 7, dan 10 adalah inti nilai buku ini dan sebaiknya digarap lebih dulu —
keempatnya yang paling tidak tergantikan buku asing. Bab 3 dan 4 lebih teknis dan
bisa disusun lebih cepat karena strukturnya sudah baku.

Akses ke satu rumah sakit dan satu puskesmas mitra akan sangat menentukan mutu Bab 10.
Sebaiknya diamankan sejak awal penulisan, bukan di akhir.

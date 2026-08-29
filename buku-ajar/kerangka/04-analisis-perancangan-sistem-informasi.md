# Kerangka Buku Ajar — Analisis dan Perancangan Sistem Informasi

**Mata kuliah:** TSI3321 Analisis dan Perancangan Sistem Informasi · 4 SKS (T3 P1) · Semester 3
**Status:** MK Utama Prodi (wajib) · Kelompok Keilmuan Sistem Informasi dan Tata Kelola TI
**Pengampu:** I Wayan Septa Malan Vergantana, S.Kom., M.Kom.
**Prasyarat:** TSI3104 Konsep Sistem Informasi (direkomendasikan)

---

## Posisi buku ini

Usulan Dekan ini tepat sasaran, dan alasannya bisa ditunjukkan dari data RPS sendiri:

1. **MK berbobot terbesar di kelompok intinya.** 4 SKS dengan komponen praktik (T3 P1) —
   satu-satunya di semester 3 selain Jaringan Komputer. Jam temu mahasiswa dengan
   materi ini paling banyak, sehingga buku ajarnya paling terpakai.
2. **Penopang langsung Profil Lulusan PL-01 Systems Analyst.** Tidak ada MK lain di
   kurikulum yang menopang profil itu sekuat ini.
3. **Seluruh pustaka utamanya asing.** Kendall & Kendall, Dennis dkk., Pressman —
   ketiganya rujukan baku, tetapi tak satu pun ditulis sebagai buku ajar semester 3
   berbahasa Indonesia dengan studi kasus lokal.
4. **Menopang 11 CPL** — jumlah terbanyak di antara MK semester 3: P-01, P-02, P-03,
   KU-01, KU-02, KU-04, KK-01, KK-03, KK-04, KK-06, KK-08.

Dibanding tiga kandidat sebelumnya, MK ini duduk **di atas Business Intelligence**
dan setara Sistem Informasi Kesehatan dari sisi dampak — bedanya, SI Kesehatan
melayani dua fakultas sekaligus, sedangkan buku ini melayani inti keilmuan prodi.

> **Catatan kepengarangan.** Pengampu TSI3321 adalah I Wayan Septa Malan Vergantana,
> bukan Anda. Jika buku ini digarap, sebaiknya sebagai **karya bersama** dengan beliau
> — pengampu yang memegang studi kasus dan pengalaman kelasnya. Ini perlu disepakati
> di awal, bukan setelah naskah berjalan.

## Sasaran pembaca

1. Mahasiswa S1 Sistem Informasi semester 3 (pembaca utama)
2. Mahasiswa MK serumpun: Arsitektur Enterprise, Pemrograman berbasis Web,
   Fundamental ERP, dan Tugas Akhir berjalur perancangan sistem
3. Mahasiswa prodi lain yang mengambil MK analisis sistem
4. Praktisi pemula — analis sistem dan staf TI yang menyusun dokumen kebutuhan

## Struktur

13 bab mengikuti 10 bahan kajian RPS, ditambah lampiran proyek. Perkiraan
**260–300 halaman** — paling tebal di antara empat kandidat, karena padat diagram.

---

## Bab 1 — Sistem Informasi dan Siklus Hidup Pengembangan
*Minggu 1 · Bahan kajian 1*

- Definisi sistem informasi dan komponennya
- SDLC: tahapan dan mengapa urutannya penting
- **Peran analis sistem**: tanggung jawab, keterampilan, posisinya di antara
  pengguna dan pengembang
- Ragam peran serumpun: business analyst, product owner, system designer

## Bab 2 — Metodologi Pengembangan Sistem
*Minggu 2 · Bahan kajian 1*

- Waterfall: fase, dokumen keluaran, kapan masih relevan
- Prototyping: throwaway dan evolusioner
- Agile: Scrum dan Kanban — peran, artefak, ritme kerja
- **Tabel perbandingan** kelebihan, kekurangan, dan kriteria pemilihan
- Kesalahan lazim: memilih metodologi karena tren, bukan karena karakter proyek

## Bab 3 — Investigasi Awal dan Studi Kelayakan
*Minggu 3 · Bahan kajian 2*

- Identifikasi masalah dan perumusan ruang lingkup
- Empat sisi kelayakan: teknis, ekonomis, operasional, jadwal
- **Perhitungan ROI dan NPV** — dengan contoh angka rupiah yang dikerjakan penuh
- Penyusunan laporan studi kelayakan

> Bagian ROI/NPV adalah titik tersulit bagi mahasiswa semester 3. Sajikan sebagai
> perhitungan bertahap, bukan rumus jadi.

## Bab 4 — Teknik Pengumpulan Kebutuhan
*Minggu 4–5 · Bahan kajian 3*

- Wawancara: persiapan, jenis pertanyaan, teknik menggali, dokumentasi hasil
- Kuesioner: perancangan butir, skala Likert, pengujian instrumen
- Observasi partisipatif dan non-partisipatif
- Studi dokumen: formulir, laporan, prosedur berjalan
- Brainstorming dan *focus group discussion*
- **Matriks pemilihan teknik** menurut situasi dan jenis narasumber
- Lampiran bab: contoh panduan wawancara dan kuesioner siap pakai

## Bab 5 — Analisis Kebutuhan Fungsional dan Non-Fungsional
*Minggu 6 · Bahan kajian 4*

- Kebutuhan fungsional: fitur, proses, aturan bisnis
- Kebutuhan non-fungsional: kinerja, keamanan, *usability*, keterpeliharaan
- Teknik penomoran dan penelusuran kebutuhan
- **Prioritas dengan MoSCoW** dan teknik lain
- Menangani kebutuhan yang saling bertentangan antar pemangku kepentingan

## Bab 6 — Spesifikasi Kebutuhan Perangkat Lunak (SRS)
*Minggu 7 · Bahan kajian 4*

- Struktur SRS: pendahuluan, deskripsi umum, kebutuhan spesifik, lampiran
- Menulis pernyataan kebutuhan yang dapat diuji
- Validasi dan verifikasi kebutuhan bersama pengguna
- Pengelolaan perubahan kebutuhan
- **Satu contoh SRS lengkap** sebagai acuan — bukan potongan

## Bab 7 — Pemodelan Proses dengan DFD
*Minggu 8 · Bahan kajian 5*

- Notasi DFD dan variannya
- Diagram konteks, DFD level 0, level 1 dan 2
- **Aturan balancing** antar level dan kesalahan yang sering terjadi
- Kamus data
- Latihan terbimbing dengan draw.io

## Bab 8 — Pemodelan Proses Bisnis dengan BPMN
*Minggu 9 · Bahan kajian 5*

- Elemen BPMN: *event*, aktivitas, *gateway*, aliran
- Kolam (*pool*) dan jalur (*lane*) untuk memisahkan pelaku
- Kapan memakai BPMN dan kapan DFD lebih tepat
- Contoh proses bisnis nyata dimodelkan utuh

## Bab 9 — Pemodelan Berorientasi Objek dengan UML
*Minggu 11–12 · Bahan kajian 6*

- *Use case diagram*: aktor, use case, `include`, `extend`, generalisasi
- Penulisan **skenario use case** yang lengkap
- *Class diagram*: kelas, atribut, metode, dan relasi (asosiasi, agregasi,
  komposisi, pewarisan)
- *Sequence diagram*: *lifeline*, pesan, aktivasi
- Konsistensi antar diagram — kesalahan paling sering di tugas mahasiswa
- Latihan terbimbing dengan StarUML

> Bab terpanjang. Pertimbangkan memecahnya menjadi 9A (use case) dan
> 9B (class & sequence) bila melebihi 40 halaman.

## Bab 10 — Perancangan Arsitektur Sistem
*Minggu 13 · Bahan kajian 7*

- Arsitektur 1-tier sampai n-tier dan konsekuensi tiap pilihan
- Pola MVC
- *Deployment diagram*
- Pemilihan platform: pertimbangan biaya, SDM, dan keberlanjutan

## Bab 11 — Perancangan Basis Data
*Minggu 14 · Bahan kajian 8*

- ERD: entitas, atribut, kardinalitas hubungan
- **Normalisasi 1NF, 2NF, 3NF** — dikerjakan langkah demi langkah
- Konversi ERD menjadi tabel relasional
- Penulisan DDL dan latihan dengan MySQL Workbench
- Perancangan fisik: indeks, tipe data, batasan

## Bab 12 — Perancangan Antarmuka Pengguna
*Bahan kajian 9*

- Prinsip perancangan antarmuka dan kaidah *usability*
- *Wireframe*, *mockup*, dan *prototype* — beda dan kegunaannya
- Perancangan alur navigasi
- Antarmuka untuk peranti bergerak
- Pengujian antarmuka bersama pengguna

> **Bahan kajian 9 tercantum di RPS tetapi tidak punya minggu tersendiri** — UI hanya
> muncul menumpang di minggu 15 dan 16. Buku ini justru bisa menutup celah tersebut.
> Sekalian, ini bahan pertimbangan bagi pengampu apakah RPS-nya perlu ditata ulang.

## Bab 13 — Dokumentasi, Manajemen Konfigurasi, dan Laporan Proyek
*Minggu 15 · Bahan kajian 10*

- Struktur laporan analisis dan perancangan: pendahuluan, analisis kebutuhan,
  perancangan (DFD, UML, arsitektur, basis data, UI), kesimpulan
- **Manajemen konfigurasi**: penomoran versi, kendali perubahan, dasar Git untuk
  dokumen rancangan
- Teknik presentasi rancangan kepada pemangku kepentingan
- Daftar periksa kelengkapan dokumen

> *Manajemen konfigurasi* juga tidak punya minggu tersendiri di RPS, padahal
> tercantum sebagai bahan kajian 10. Sama seperti Bab 12, buku menutup celahnya.

## Lampiran — Proyek Menyeluruh
*Minggu 16*

Satu studi kasus dikerjakan **dari awal sampai akhir**: investigasi, pengumpulan
kebutuhan, SRS, DFD, BPMN, UML, arsitektur, basis data, antarmuka, sampai laporan.
Disarankan mengambil kasus dari lingkungan ITEKES atau UMKM Bali agar dekat dengan
pengalaman mahasiswa.

Lampiran kedua: **panduan pemasangan dan penggunaan draw.io, StarUML, dan
MySQL Workbench** — dipisahkan agar mudah diperbarui saat versi perkakas berubah.

---

## Elemen pedagogis tiap bab

| Elemen | Isi |
|---|---|
| Capaian pembelajaran | Sub-CPMK dari RPS |
| Istilah kunci | Padanan Inggris–Indonesia di awal bab |
| Contoh dikerjakan | Kasus yang sama dipakai lintas bab agar berkesinambungan |
| Latihan terbimbing | Langkah bernomor memakai perkakas pemodelan |
| Kesalahan lazim | Kekeliruan yang sering muncul di tugas, beserta perbaikannya |
| Latihan mandiri | Selaras dengan indikator penilaian RPS |
| Rangkuman dan evaluasi | Sesuai bobot minggu di RPS |

## Pustaka acuan

Sudah tercantum di RPS dan tinggal dipakai:

- Kendall, K. E., & Kendall, J. E. (2018). *Systems analysis and design* (10th ed.). Pearson.
- Dennis, A., Wixom, B. H., & Tegarden, D. (2015). *Systems analysis and design:
  An object-oriented approach with UML* (5th ed.). Wiley.
- Pressman, R. S. (2014). *Software engineering: A practitioners approach* (8th ed.). McGraw-Hill.
- Satzinger, J. W., Jackson, R. B., & Burd, S. D. (2016). *Systems analysis and design
  in a changing world* (7th ed.). Cengage Learning.
- Whitten, J. L., & Bentley, L. D. (2007). *Systems analysis and design methods* (7th ed.). McGraw-Hill.

**Perlu ditambahkan sendiri:** spesifikasi resmi **BPMN 2.0 (OMG)** dan **UML 2.5 (OMG)**
sebagai rujukan notasi, serta **ISO/IEC/IEEE 29148:2018** (pengganti IEEE 830) untuk
struktur SRS. Tanpa ketiganya, bab notasi dan bab SRS bersandar pada buku sekunder saja.

## Catatan penggarapan

**Garap lebih dulu Bab 7, 8, 9, dan 11.** Keempatnya adalah inti keterampilan yang diuji
dan bagian yang paling sering membuat mahasiswa tersandung — sekaligus paling sedikit
tersedia panduannya dalam bahasa Indonesia dengan contoh yang dikerjakan tuntas.

**Bab 12 dan 13 adalah nilai tambah buku ini**, karena menutup dua bahan kajian yang di
RPS belum punya minggu tersendiri. Justru di sini buku memberi sesuatu yang tidak
didapat mahasiswa dari jadwal kuliah.

**Kunci mutu buku ini ada pada satu keputusan awal: pilih satu studi kasus dan pakai
konsisten dari Bab 3 sampai Lampiran.** Pembaca lalu melihat satu sistem tumbuh dari
wawancara pertama sampai rancangan basis data — bukan dua belas contoh terputus.
Ini pula yang membedakannya dari kelima buku acuan di atas.

Risiko keusangan rendah: notasi DFD, BPMN, UML, dan normalisasi stabil bertahun-tahun.
Yang cepat berubah hanya panduan perkakas — karena itu ditaruh di lampiran terpisah.

# tools/ — perkakas penyusunan RPS

Skrip di sini merekam cara template `template/RPS_MK_TSI0000.docx` dibentuk dan cara JSON
RPS ditingkatkan ke format acuan. Template adalah berkas biner, jadi tanpa skrip
ini perubahannya tidak bisa ditinjau maupun diulang.

Semua skrip dijalankan dari akar repo.

## Acuan yang dipakai

| Dokumen | Dipakai untuk |
|---|---|
| `materi-rps/Buku Kurikulum S1 Sistem Informasi - 20260508.docx` | rumusan CPL resmi (bagian 3.2), daftar MK (Tabel 3.1), bahan kajian (Bab IV) |
| `materi-rps/KFR 4560 Cosmeceutical.docx` | format tabel RPS: susunan kolom, penempatan matriks, istilah |
| `materi-rps/1. Panduan terkait Pembelajaran/PANDUAN PENYUSUNAN RPS ITEKES BP 2023 (1).pdf` | komponen wajib RPS, kode metode pembelajaran, singkatan TM/PT/BM |
| `Buku-Panduan-KPT-2024...pdf` hal. 118 | format band "Korelasi CPL terhadap Sub-CPMK" |

Tabel 3.2 Buku Kurikulum (Pemetaan CPL dengan Mata Kuliah) **berisi 464 tanda ✓
untuk 54 MK** dan merupakan acuan resmi CPL mana yang dibebankan pada tiap MK.
Tandanya tidak terbaca lewat `cell.text` python-docx karena tersimpan di dalam
run bersarang — baca lewat elemen `w:t` (lihat `selaraskan_cpl_kurikulum.py`).

## 1. Membangun template

Dijalankan berurutan di atas template asal. **Selalu mulai dari salinan bersih**;
skrip `tpl_01` dan `tpl_02` tidak idempoten.

```
python tools/tpl_01_perluas_kapasitas.py   template/RPS_MK_TSI0000.docx
python tools/tpl_02_format_acuan.py        template/RPS_MK_TSI0000.docx
python tools/tpl_03_band_korelasi_cpl.py   template/RPS_MK_TSI0000.docx
python tools/tpl_04_perluas_cpl.py         template/RPS_MK_TSI0000.docx 20
```

- `tpl_01` — memperbesar kapasitas: CPL 8→16 baris, CPMK 5→10, Sub-CPMK 8→12,
  pustaka 3→8; menambah matriks Korelasi CPMK×Sub-CPMK; mengganti
  `sub_cpmk.cpl` menjadi `sub_cpmk.taksonomi`.
- `tpl_02` — menyesuaikan dengan RPS acuan: baris CPL/CPMK/Sub-CPMK diciutkan
  jadi dua kolom, menambah band "Penilaian dan Korelasinya dengan CPMK",
  mengganti judul kolom (4) menjadi "Kriteria & Teknik".
- `tpl_03` — menambah band "Korelasi CPL terhadap Sub-CPMK" sesuai KPT 2024.
- `tpl_04` — memperbesar kapasitas CPL dari 16 menjadi 20, baik baris daftar CPL
  maupun kolom matriks Korelasi CPL. Dibutuhkan karena Tugas Akhir (TSI7854)
  membebani 17 CPL. Skrip ini idempoten.

Template asal (sebelum semua perubahan) bisa dipulihkan dari git:
`git show HEAD:template/RPS_MK_TSI0000.docx > template/RPS_MK_TSI0000.docx`.

## 2. Menyiapkan data acuan

```
python tools/cpl_resmi.py
```

Menulis `cpl_resmi.json` berisi 33 CPL resmi. Jalankan ulang setiap Buku
Kurikulum diperbarui.

## 3. Meningkatkan JSON RPS

Berurutan, atas satu folder semester:

```
python tools/json_00_seimbangkan_bobot.py     "input/rps_json/sem2/*.json"
python tools/json_01_cpl_korelasi.py          cpl_resmi.json "input/rps_json/sem2/*.json"
python tools/json_02_indikator_pustaka.py     "input/rps_json/sem2/*.json"
python tools/json_03_baris_tugas.py           "input/rps_json/sem2/*.json"
python tools/json_04_format_acuan.py          "input/rps_json/sem2/*.json"
python tools/selaraskan_cpl_kurikulum.py      "input/rps_json/sem2/*.json"
python tools/json_04_format_acuan.py          "input/rps_json/sem2/*.json"
python tools/json_05_korelasi_cpl.py          "input/rps_json/sem2/*.json"
python tools/json_06_indikator.py             "input/rps_json/sem2/*.json"
```

- `json_00` — membetulkan total bobot mingguan menjadi tepat 100%.

- `json_01` — rumusan CPL verbatim, taksonomi afektif, matriks korelasi
  CPMK×Sub-CPMK, notasi TM/PT/BM, blok Kriteria.
- `json_02` — deskripsi Sub-CPMK bertaksonomi, indikator bernomor, rujukan pustaka.
- `json_03` — merapikan baris `Tugas n:` pada kolom Bentuk Pembelajaran.
- `json_04` — label CPL, rujukan menyatu, matriks penilaian, `minggu` jadi `n/16`,
  blok Metode Penilaian/Kriteria/Teknik.
- `selaraskan_cpl_kurikulum` — menyamakan himpunan CPL dengan Tabel 3.2 Buku
  Kurikulum. Dijalankan setelah `json_04` karena butuh label CPL, lalu `json_04`
  dan `json_05` diulang supaya label dan kedua matriks ikut menyesuaikan.
  Penempatan CPL yang baru ditambahkan ke CPMK **perlu ditinjau dosen**.
- `json_05` — matriks Korelasi CPL×Sub-CPMK dan field `nomor` pada CPL.
  Pembulatan memakai metode sisa terbesar agar kolom tabel berjumlah tepat 100.
- `json_06` — menyusun ulang indikator butir ke-2 dan seterusnya dari pokok
  bahasan mingguan. Butir pertama (rumusan dosen) tidak pernah diubah.
  Pemenggalan dilakukan pada aspek tingkat atas, bukan pada tiap koma, supaya
  tidak muncul potongan seperti "Ketepatan menganalisis kelas A".

Setelah `selaraskan_cpl_kurikulum`, periksa apakah ada CPMK yang kehilangan
seluruh CPL-nya — `validasi_rps.py` melaporkannya sebagai "CPMK tanpa CPL".
Penempatan CPL ke CPMK sebaiknya ditinjau isinya, bukan sekadar dibiarkan pada
hasil pencocokan domain.

`json_01`–`json_02` bekerja dari skema lama; sisanya idempoten.

### Lembar isian Bab pustaka

```
python tools/lembar_bab_pustaka.py buat  "input/rps_json/sem2/*.json" isian/bab_pustaka_sem2.csv
python tools/lembar_bab_pustaka.py terap "input/rps_json/sem2/*.json" isian/bab_pustaka_sem2.csv
```

Kolom Materi kini merujuk seluruh pustaka utama (`[P1, P2, P3]`). Lembar ini
memuat tiap minggu beserta materinya; dosen mengisi kolom `bab`
(mis. `P1 Bab 3; P4 Bab 1-2`), lalu mode `terap` menuliskannya ke JSON.

## 4. Memeriksa hasil

```
python tools/validasi_rps.py "input/rps_json/sem2/*.json"
```

Memeriksa rantai CPL→CPMK→Sub-CPMK, rumusan CPL terhadap Buku Kurikulum, total
bobot 100%, konsistensi ketiga matriks, kapasitas template, dan format kolom
tabel mingguan. Status keluar 1 bila ada temuan.

## 5. Menghasilkan dokumen

```
python tools/edit_rps.py -i "input/rps_json/sem2/TSI3211_Sistem Operasi.json" -o "outputs/rps/sem2/TSI3211_Sistem Operasi.docx"
python tools/docx_to_pdf_folder.py -i outputs/rps/sem2
```

`tools/edit_rps.py` keluar dengan status 1 bila ada bagian wajib yang kosong sama
sekali di dokumen hasil — pertanda nama field JSON tidak cocok dengan template.

## Perkakas bantu

| Skrip | Guna |
|---|---|
| `dump_docx.py` | mencetak struktur tabel sebuah DOCX, untuk membandingkan dengan acuan |
| `pdf_ke_teks.py` | mengekstrak teks PDF per halaman |
| `pdf_ke_docx.py` | mengonversi PDF ke DOCX (butuh `pdf2docx`) |

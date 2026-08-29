Saya butuh file JSON Rencana Pembelajaran Semester (RPS) untuk satu mata kuliah di Program Studi S1 Sistem Informasi, Fakultas Teknologi, ITEKES Bintang Persada. JSON ini akan diisikan ke template `template/RPS_MK_TSI0000.docx` oleh `tools/edit_rps.py`, jadi nama field harus persis seperti di bawah.

Data yang saya berikan: nama MK, kode MK, jumlah SKS, semester, dan dosen pengampu. Kalau ada yang belum saya sebutkan, tanyakan dulu — jangan mengarang kode CPL.

**CPL yang dibebankan pada MK ini TIDAK boleh dipilih sendiri.** Penentunya adalah
Tabel 3.2 "Pemetaan Capaian Pembelajaran Lulusan (CPL) dengan Mata Kuliah" pada
`materi-rps/Buku Kurikulum S1 Sistem Informasi - 20260508.docx`: cari baris mata
kuliah ini, lalu ambil persis kolom-kolom yang bertanda ✓. Rumusan tiap CPL
disalin verbatim dari bagian 3.2 buku yang sama (tersedia siap pakai di
`cpl_resmi.json`). Jangan menambah CPL yang menurut Anda relevan, dan jangan
membuang CPL yang bertanda — himpunannya harus sama persis. Kalau saya tidak
melampirkan daftar CPL-nya, jalankan `python tools/selaraskan_cpl_kurikulum.py
"<file>.json" --periksa` untuk melihat selisihnya, atau tanyakan ke saya.

Catatan teknis: tanda ✓ di Tabel 3.2 tersimpan di dalam run bersarang sehingga
tidak terbaca lewat `cell.text` python-docx — baca lewat elemen `w:t`.

## Aturan isi

1. **Rantai capaian harus nyambung.** CPL → CPMK → Sub-CPMK → pertemuan mingguan. Setiap CPL yang dicantumkan wajib dirujuk minimal satu CPMK; setiap CPMK wajib dirujuk minimal satu Sub-CPMK; setiap Sub-CPMK wajib muncul di minimal satu minggu. Jangan mencantumkan CPL yang tidak dibebankan ke MK ini.

2. **CPL lintas domain.** Ambil dari empat domain sesuai kebutuhan MK: Sikap (`S-xx`), Pengetahuan (`P-xx`), Keterampilan Umum (`KU-xx`), Keterampilan Khusus (`KK-xx`). MK Wajib Nasional (Agama, Pancasila, Kewarganegaraan, Bahasa Indonesia) umumnya hanya membebani Sikap dan Keterampilan Umum — itu wajar, jangan dipaksakan menambah P/KK. MK keilmuan inti wajib memuat P dan KK.

3. **Taksonomi ganda.** Field `taksonomi` pada Sub-CPMK diisi level kognitif **dan** afektif, mis. `"C2, A3"` atau `"C4–C5, A4"`. MK berpraktikum tambahkan psikomotor, mis. `"C3, P3, A3"`.

4. **Kode dan rujukan ditulis menyatu dengan kalimatnya**, mengikuti RPS acuan `materi-rps/KFR 4560 Cosmeceutical.docx`. Tabel RPS hanya punya dua kolom untuk bagian ini, jadi:
   - `cpl_prodi[].label` berisi `"CPL 1 (S-01)"` — nomor urut tampil, lalu kode resmi Buku Kurikulum dalam kurung. `cpl_prodi[].nomor` berisi versi pendeknya (`"CPL 1"`) untuk header kolom matriks.
   - `cpmk[].deskripsi` diakhiri rujukan CPL memakai nomor urut tadi, mis. `"... secara mandiri (CPL 1, CPL 4)"`. Field `cpl` tetap diisi kode resmi untuk keperluan validasi.
   - `sub_cpmk[].deskripsi` diakhiri taksonomi lalu CPMK, mis. `"Mampu menjelaskan ... (C2, A3) (CPMK-1)"`.

5. **Notasi waktu SN-Dikti.** Gunakan `TM` (Tatap Muka), `PT` (Penugasan Terstruktur), `BM` (Belajar Mandiri) — jangan pakai singkatan lain seperti `BT`, karena legenda di kaki dokumen hanya mendefinisikan tiga itu. Format: `[TM: 1x(2x50')]` dan `[PT+BM: (1+1)x(2x60')]`, dengan angka `2x50'` menyesuaikan jumlah SKS teori (1 sks = 50 menit TM, 60 menit PT, 60 menit BM per minggu). MK berpraktikum menambahkan `[P: 1x(1x170')]`. Setiap minggu harus punya TM dan PT+BM, bukan hanya minggu pertama.

6. **Susunan field `tatap_muka`.** Kolom (5) sempit, jadi urutan barisnya baku dan label `Metode:` berdiri sendiri — kalau digabung dengan nama metode, barisnya melewati lebar kolom dan terpotong saat dicetak:
   ```
   Bentuk: Kuliah
   Metode:
   Cooperative Learning (CoL)
   [TM: 1x(2x50')]
   Tugas 3: studi kasus — Segmentasi pasar
   [PT+BM: (1+1)x(2x60')]
   ```
   Nama metode memakai daftar baku Pedoman BPM 2023: Small Group Discussion (SGD), Role-Play & Simulation (RPS), Discovery Learning (DL), Self-Directed Learning (SDL), Cooperative Learning (CoL), Collaborative Learning (CbL), Contextual Learning (CtL), Project Based Learning (PjBL), Problem Based Learning (PBL).

7. **Indikator bernomor.** Isi 2–4 indikator per minggu, diberi nomor sesuai nomor minggu (`1.1`, `1.2`, `1.3` untuk minggu 1), dipisah `\n`.

8. **Kolom (4) berisi tiga blok berurutan** — Metode Penilaian, Kriteria, lalu Teknik. Perhatikan istilahnya: judul kolomnya "Kriteria & Teknik", dan label teknik memakai `Test` / `Non Test` (tanpa tanda hubung):
   ```
   Metode Penilaian:
   Kuis (3%)
   Kriteria:
   • Pedoman penskoran
   • Rubrik penilaian tugas
   Teknik:
   Test: Kuis online
   Non Test: tanya jawab
   ```
   Jenis penilaian dibatasi lima: Kuis, Tugas, Aktivitas Partisipatif, Ujian Tengah Semester, Ujian Akhir Semester.

9. **Materi merujuk pustaka.** Akhiri field `materi` dengan baris rujukan kode pustaka, mis. `\n[P1, P2]`. Kode ini harus ada di `pustaka_utama` atau `pustaka_pendukung`.

10. **Bobot total tepat 100%** dijumlah dari seluruh 16 baris `detail`, termasuk UTS dan UAS. Field `bobot` ditulis sebagai angka tanpa tanda persen (`"3"`, bukan `"3%"`), karena judul kolomnya sudah memuat `(%)`.

11. **Nomor minggu memakai format `"n/16"`** pada field `minggu` di `detail`, mis. `"1/16"`.

12. **Matriks penilaian** (`penilaian`) memetakan jenis penilaian terhadap CPMK. Kolom `c1` = CPMK-1, `c2` = CPMK-2, dan seterusnya. Baris terakhir wajib berjudul `"Total"`, dengan `bobot` = 100% dan tiap kolom berisi jumlah kontribusi CPMK yang bersangkutan. Bobot tiap minggu disebar rata ke CPMK yang ditopang Sub-CPMK minggu itu.

13. **Matriks korelasi CPL** (`korelasi_cpl`) mengikuti Panduan KPT 2024 hal. 118: baris = Sub-CPMK, kolom `p1`…`pN` = sebaran bobot ke CPL 1…N dalam persen, lalu `bobot` (bobot penilaian Sub-CPMK itu) dan `minggu` (jumlah minggu). Baris terakhir berjudul `"Total"` dengan `bobot` 100. Bobot tiap minggu masuk ke Sub-CPMK yang dibahas minggu itu, lalu dibagi rata ke CPL yang ditopang CPMK-nya; minggu UTS/UAS dibagi rata ke seluruh Sub-CPMK yang diujikan. Sel bernilai nol dikosongkan, bukan ditulis `0`.

14. **UTS (minggu 8) dan UAS (minggu 16)** mengisi seluruh kolom seperti minggu biasa. Kolom (2) memuat daftar Sub-CPMK yang diujikan, mis. `"Sub-CPMK 1,2,3,4,5,6,7
(Ujian Tengah Semester)"`.

15. **Judul buku dimiringkan** dengan penanda `*judul*` pada field `referensi` — `edit_rps.py` mengubahnya menjadi italic Word. Jangan pakai penanda markdown lain di field mana pun; hanya `*...*` yang dikenali.

16. **Matriks korelasi** (`korelasi`) harus konsisten dengan field `cpmk` pada tiap Sub-CPMK. Kolom `m1` = Sub-CPMK 1, `m2` = Sub-CPMK 2, dan seterusnya. Isi `"√"` bila terkait, `""` bila tidak. Sertakan kunci `m1` sampai `m<jumlah Sub-CPMK>` pada setiap baris — kunci untuk Sub-CPMK yang tidak ada boleh dihilangkan.

## Batas kapasitas template

Kalau melebihi angka ini, template tidak muat dan datanya akan terpotong:

| Array | Maksimum |
|---|---|
| `cpl_prodi` | 20 |
| `cpmk` | 10 |
| `sub_cpmk` | 12 |
| `korelasi` | 10 baris (satu per CPMK) |
| `penilaian` | 10 baris termasuk baris Total |
| `korelasi_cpl` | 13 baris termasuk baris Total |
| `pustaka_utama` | 8 |
| `pustaka_pendukung` | 8 |
| `detail` | tepat 16 (minggu 1–16) |

Slot yang tidak terpakai dibuang otomatis saat pengisian, jadi tidak perlu diisi placeholder kosong.

## Struktur JSON

```json
{
  "meta": {
    "kode_mk": "TSI1107",
    "nama_mk": "Agama",
    "sks_total": 2,
    "sks_teori": 2,
    "sks_praktik": 0,
    "semester": 1,
    "status": "Wajib",
    "kategori": "Mata Kuliah Wajib Nasional (MKWN)",
    "tanggal_penyusunan": "2026-03-01",
    "dosen_pengampu": "I Made Hendra Wijaya, S.Kom., M.Kom.",
    "dosen_sign": "sign/hendra.png",
    "nuptk": "5138772673130293",
    "pangkat_golongan": "-",
    "jabatan": "Asisten Ahli"
  },

  "cpl_prodi": [
    {"kode": "S-01", "tipe": "Sikap", "label": "CPL 1 (S-01)", "nomor": "CPL 1", "deskripsi": "..."},
    {"kode": "KU-01", "tipe": "Keterampilan Umum", "label": "CPL 2 (KU-01)", "nomor": "CPL 2", "deskripsi": "..."}
  ],

  "cpmk": [
    {"kode": "CPMK-1", "cpl": "S-01, KU-01", "deskripsi": "Mampu ... (CPL 1, CPL 2)"}
  ],

  "sub_cpmk": [
    {"kode": "Sub-CPMK 1", "cpmk": "CPMK-1", "minggu": "1", "taksonomi": "C2, A2",
     "deskripsi": "Mampu menjelaskan ... (C2, A2) (CPMK-1)"}
  ],

  "korelasi": [
    {"cpmk": "CPMK-1", "m1": "√", "m2": "", "m3": "", "m4": "", "m5": "",
     "m6": "", "m7": "", "m8": "", "m9": "", "m10": "√"}
  ],

  "korelasi_cpl": [
    {"sub": "Sub-CPMK 1", "p1": "", "p2": "2.6", "bobot": "5.1", "minggu": "1"},
    {"sub": "Total", "p1": "13.5", "p2": "5.6", "bobot": "100", "minggu": "14"}
  ],

  "penilaian": [
    {"jenis": "Kuis", "bobot": "12%", "c1": "6%", "c2": "6%"},
    {"jenis": "Tugas", "bobot": "40%", "c1": "20%", "c2": "20%"},
    {"jenis": "Ujian Tengah Semester", "bobot": "15%", "c1": "15%", "c2": "0%"},
    {"jenis": "Ujian Akhir Semester", "bobot": "33%", "c1": "0%", "c2": "33%"},
    {"jenis": "Total", "bobot": "100%", "c1": "41%", "c2": "59%"}
  ],

  "detail": [
    {
      "minggu": "1/16",
      "deskripsi": "Sub-CPMK 1 : Mampu menjelaskan tujuan dan fungsi pendidikan agama (C2, A2) (CPMK-1)",
      "indikator": "1.1 ...
1.2 ...
1.3 ...",
      "kriteria": "Metode Penilaian:
Kuis (3%)
Kriteria:
• Pedoman penskoran
• Rubrik penilaian tugas
Teknik:
Test: Kuis online
Non Test: tanya jawab",
      "tatap_muka": "Bentuk: Kuliah
Metode:
Ceramah interaktif, tanya jawab
[TM: 1x(2x50')]
Tugas 1: latihan soal — Tujuan pendidikan agama
[PT+BM: (1+1)x(2x60')]",
      "daring": "eLearning ITEKES BP (LMS)
Google Meet (sinkron)",
      "materi": "Tujuan pendidikan agama, fungsi membangun kepribadian humanis
[P1, P2]",
      "bobot": "3"
    }
  ],

  "bahan_kajian": "1. ...\n2. ...",

  "pustaka_utama": [
    {"kode": "P1", "jenis": "Utama", "referensi": "Nama, A. (2020). *Judul buku*. Penerbit."}
  ],
  "pustaka_pendukung": [
    {"kode": "P4", "jenis": "Pendukung", "referensi": "..."}
  ],

  "deskripsi_singkat": "...",
  "matakuliah_syarat": "-"
}
```

## Sebelum menyerahkan hasil, periksa

- [ ] `detail` berisi tepat 16 entri, `minggu` 1 sampai 16 berurutan.
- [ ] Jumlah seluruh `bobot` = 100%.
- [ ] Tidak ada CPL yang tidak dirujuk CPMK mana pun, dan tidak ada CPMK yang merujuk kode CPL di luar `cpl_prodi`.
- [ ] Setiap Sub-CPMK muncul minimal sekali di kolom `deskripsi` pada `detail`.
- [ ] Baris `korelasi` cocok dengan field `cpmk` di tiap Sub-CPMK.
- [ ] Baris terakhir `korelasi_cpl` berjudul `Total`, `bobot` = 100, dan tiap kolom `pN` sama dengan jumlah kolom di atasnya.
- [ ] Baris terakhir `penilaian` berjudul `Total`, bobotnya 100%, dan tiap kolom CPMK sama dengan jumlah kolom di atasnya.
- [ ] Setiap `cpl_prodi` punya `label`; `cpmk[].deskripsi` diakhiri `(CPL n)`; `sub_cpmk[].deskripsi` diakhiri `(taksonomi) (CPMK-n)`.
- [ ] `detail[].minggu` berformat `n/16` dan `detail[].bobot` tanpa tanda persen.
- [ ] Semua kode pustaka yang dirujuk di `materi` ada di daftar pustaka.
- [ ] Setiap array masih di bawah batas kapasitas di tabel atas.
- [ ] JSON valid (UTF-8, tanpa trailing comma) dan siap diparsing.

Contoh lengkap yang sudah memenuhi semua aturan di atas: `input/rps_json/sem1.1/TSI1107_Agama.json`. Seluruh isi folder `input/rps_json/sem1.1/` sudah mengikuti standar ini dan bisa dipakai sebagai rujukan.

Rumusan CPL resmi diambil verbatim dari `materi-rps/Buku Kurikulum S1 Sistem Informasi - 20260508.docx` bagian 3.2 (S-01…S-10, P-01…P-05, KU-01…KU-07, KK-01…KK-11). Jangan menyalin rumusan generik SN-Dikti — beberapa butir di Buku Kurikulum berbeda kalimatnya.

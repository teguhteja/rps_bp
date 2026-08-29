Saya memiliki file RPS mata kuliah dalam format JSON (skema lengkapnya ada di `prompt/rps.md`). Tolong buatkan file JSON untuk Satuan Acara Pengajaran (SAP) dengan ketentuan berikut.

## 1. Bentuk keluaran

JSON SAP berisi 16 pertemuan (minggu 1 s.d. 16), satu objek per pertemuan, dengan field persis seperti contoh di bagian akhir. Sertakan `meta`: `kode_mk`, `nama_mk`, `sks_total`, dan `template_sap` (mis. `"SAP_MK_TSI0000.docx"`). Nama field tidak boleh diubah karena dibaca langsung oleh `tools/edit_sap.py`.

## 2. Cara mengambil data dari RPS JSON

Sumber utama adalah array `detail` (16 entri, satu per minggu). Field `cpl_prodi`, `korelasi`, `penilaian`, dan `korelasi_cpl` tidak dipakai di SAP — abaikan saja.

| Field SAP | Diambil dari | Catatan pengolahan |
|---|---|---|
| `no` | `detail[i].minggu` | Nilainya berformat `"1/16"`; ambil angka sebelum garis miring saja. |
| `waktu_pertemuan` | `detail[i].tatap_muka` | Field ini multi-baris dengan urutan baku: `Bentuk: …`, `Metode:`, nama metode di baris tersendiri, `[TM: …]`, `Tugas n: …`, `[PT+BM: …]`. Ambil baris `Bentuk:` dan baris `[TM: …]` saja, gabung jadi satu kalimat pendek, mis. `"Kuliah, TM: 1x(2x50')"`. |
| `detail_cpmk` | array `cpmk` | Baca kode CPMK di dalam kurung pada `detail[i].deskripsi` (mis. `(CPMK-3)` atau `(CPMK-3, CPMK-5)`), lalu ambil `deskripsi` CPMK tersebut. Kalau lebih dari satu, gabungkan dengan `; `. |
| `detail_sub_cpmk` | `detail[i].deskripsi` | Boleh dipakai apa adanya, atau buang penanda taksonomi dan rujukan CPMK di ujungnya agar lebih ringkas. |
| `indikator_1`, `indikator_2` | `detail[i].indikator` | Field ini berisi indikator bernomor (`1.1`, `1.2`, `1.3`) yang dipisah `\n`. **Pecah per baris, bukan per koma.** Baris pertama → `indikator_1`; sisanya digabung `\n` → `indikator_2`. Kalau hanya ada satu baris, isi `indikator_2` dengan string kosong. |
| `tujuan_pembelajaran` | parafrase `detail[i].deskripsi` + indikator | Tulis sebagai kalimat "Mahasiswa mampu ...". |
| `pokok_bahasan` | `detail[i].materi` | **Baris terakhir `materi` adalah rujukan pustaka seperti `[P1, P2]` — buang baris itu lebih dulu.** Pokok bahasan diambil dari bagian awal materi sebelum koma pertama. |
| `sub_pokok_bahasan_1`, `sub_pokok_bahasan_2` | `detail[i].materi` | Pecah sisa poin materi (setelah baris rujukan dibuang) menjadi dua bagian yang seimbang. |
| `evaluasi_1`, `evaluasi_2` | `detail[i].kriteria` dan `detail[i].bobot` | `kriteria` punya tiga blok berurutan: `Metode Penilaian:` (jenis penilaian beserta bobotnya), `Kriteria:` (rubrik/pedoman), lalu `Teknik:` yang berisi `Test:` dan/atau `Non Test:` — perhatikan ejaannya, bukan `Bentuk:`/`Tes:`/`Non-Tes:`. Ambil isi blok `Teknik:` sebagai jenis evaluasi dan tambahkan bobotnya. **`detail[i].bobot` sudah berupa angka tanpa tanda persen**, jadi tambahkan sendiri, mis. `"Kuis online - Bobot 3%"`. Kalau ada dua teknik (Test dan Non Test), pisahkan ke `evaluasi_1` dan `evaluasi_2`. |
| `referensi_1`, `referensi_2` | `pustaka_utama` / `pustaka_pendukung` | Baris rujukan pada `materi` menyebut kode pustaka (`[P1, P2]`). Gunakan kode itu untuk mengambil entri yang tepat lewat field `kode`. **Hapus penanda `*` pada judul buku** — SAP tidak memakai penanda miring. Tambahkan nomor bab bila relevan. |

## 3. Kegiatan pembelajaran

Field `kegiatan` berisi objek `pendahuluan`, `penyajian`, dan `penutup`; masing-masing punya `pengajar`, `mahasiswa`, dan `media`. Isi dengan teks realistis yang menyesuaikan materi pertemuan tersebut, dan selaraskan `media` dengan `detail[i].daring` di RPS (mis. LMS eLearning ITEKES BP, Google Meet, forum diskusi asinkron).

- Pendahuluan: doa, presensi, apersepsi, penyampaian tujuan pembelajaran.
- Penyajian: penjelasan materi, contoh/studi kasus, latihan atau diskusi. Metode harus konsisten dengan nama metode yang tertulis satu baris di bawah label `Metode:` pada `detail[i].tatap_muka`.
- Penutup: kesimpulan, kuis/tugas, informasi pertemuan berikutnya.

## 4. Pertemuan ujian

Minggu 8 (UTS) dan minggu 16 (UAS) memakai struktur khusus yang berfokus pada pelaksanaan ujian: pendahuluan berisi pembagian soal dan penjelasan tata tertib, penyajian berisi pengerjaan soal dan pengawasan, penutup berisi pengumpulan lembar jawaban. Pada kedua minggu ini `detail[i].deskripsi` berbentuk `"Sub-CPMK 1,2,3,4,5,6,7
(Ujian Tengah Semester)"` — daftar Sub-CPMK yang diujikan, bukan kalimat capaian. Pakai apa adanya untuk `detail_sub_cpmk`, dan susun `detail_cpmk` dari gabungan CPMK seluruh Sub-CPMK yang disebut.

## 5. Konsistensi yang harus dijaga

- Jumlah pertemuan tepat 16, `no` berurutan 1–16.
- Total bobot yang muncul di seluruh field `evaluasi_*` harus sama dengan total `bobot` di RPS, yaitu 100%.
- Nilai `waktu_pertemuan` konsisten dengan SKS teori MK; jangan menyalin notasi dari MK lain.
- Setiap Sub-CPMK yang ada di RPS muncul di minimal satu pertemuan SAP.
- Tidak ada field yang berisi placeholder `{...}` atau teks contoh yang belum diganti.

## 6. Format JSON yang diinginkan

Ilustrasi dua pertemuan; hasil akhir harus lengkap 16 pertemuan.

```json
{
  "meta": { "kode_mk": "...", "nama_mk": "...", "sks_total": "...", "template_sap": "SAP_MK_TSI0000.docx" },
  "pertemuan": [
    {
      "no": 1,
      "waktu_pertemuan": "Kuliah, TM: 1x(2x50')",
      "detail_cpmk": "...",
      "detail_sub_cpmk": "...",
      "indikator_1": "...",
      "indikator_2": "...",
      "tujuan_pembelajaran": "Mahasiswa mampu ...",
      "pokok_bahasan": "...",
      "sub_pokok_bahasan_1": "...",
      "sub_pokok_bahasan_2": "...",
      "kegiatan": {
        "pendahuluan": { "pengajar": "...", "mahasiswa": "...", "media": "..." },
        "penyajian": { "pengajar": "...", "mahasiswa": "...", "media": "..." },
        "penutup": { "pengajar": "...", "mahasiswa": "...", "media": "..." }
      },
      "evaluasi_1": "...",
      "evaluasi_2": "...",
      "referensi_1": "...",
      "referensi_2": "..."
    },
    { "no": 2, "...": "..." }
  ]
}
```

Silakan generate untuk semua 16 pertemuan berdasarkan RPS JSON yang saya berikan. Output harus JSON valid dan siap diparsing.

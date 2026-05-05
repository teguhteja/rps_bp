Saya memiliki file RPS mata kuliah dalam format JSON. Tolong buatkan file JSON untuk Satuan Acara Pengajaran (SAP) dengan ketentuan berikut:

1. JSON SAP harus berisi 16 pertemuan (minggu 1 s.d. 16).
2. Struktur JSON SAP mengikuti pola seperti contoh di bawah. Setiap pertemuan memiliki field:
   - no (nomor pertemuan)
   - waktu_pertemuan (ambil dari detail[i].tatap_muka, ubah jika perlu)
   - detail_cpmk (ambil dari cpmk yang relevan dengan pertemuan tersebut, bisa digabung dari beberapa CPMK)
   - detail_sub_cpmk (ambil dari detail[i].deskripsi)
   - indikator_1 dan indikator_2 (ambil dari detail[i].indikator, pecah jika ada koma/titik koma)
   - tujuan_pembelajaran (parafrase dari detail[i].deskripsi atau indikator)
   - pokok_bahasan (ambil dari detail[i].materi, gunakan bagian awal sebelum koma/dan)
   - sub_pokok_bahasan_1 dan sub_pokok_bahasan_2 (ambil poin-poin dari materi)
   - kegiatan: berisi objek pendahuluan, penyajian, penutup. Masing-masing memiliki pengajar, mahasiswa, media. 
     Isi dengan teks yang realistis sesuai materi dan aktivitas perkuliahan.
   - evaluasi_1 dan evaluasi_2 (ambil dari detail[i].kriteria dan bobot)
   - referensi_1 dan referensi_2 (ambil dari pustaka_utama, tambahkan nomor bab jika perlu)

3. Untuk kegiatan (pengajar, mahasiswa, media), buatkan secara otomatis dengan gaya yang sesuai dengan materi di pertemuan tersebut. Contoh:
   - Pendahuluan: doa, presensi, apersepsi, penyampaian tujuan.
   - Penyajian: penjelasan materi, contoh, latihan.
   - Penutup: kesimpulan, kuis/tugas, informasi pertemuan berikutnya.

4. Untuk pertemuan UTS (biasanya minggu 8) dan UAS (minggu 16), buat struktur khusus dengan kegiatan yang berfokus pada ujian.

5. Output JSON harus lengkap dan siap diparsing. Sertakan meta: kode_mk, nama_mk, sks_total, dan template_sap (misal "SAP_MK_TSI0000.docx").

6. Gunakan data dari file RPS JSON yang saya upload. Pastikan mengambil detail dari array "detail" dan pustaka dari "pustaka_utama". Jika ada sub_cpmk, boleh digunakan sebagai referensi.

Berikut adalah contoh format JSON SAP yang diinginkan (hanya 2 pertemuan sebagai ilustrasi):

{
  "meta": { "kode_mk": "...", "nama_mk": "...", "sks_total": "...", "template_sap": "..." },
  "pertemuan": [
    {
      "no": 1,
      "waktu_pertemuan": "...",
      "detail_cpmk": "...",
      "detail_sub_cpmk": "...",
      "indikator_1": "...",
      "indikator_2": "...",
      "tujuan_pembelajaran": "...",
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
    { ... }
  ]
}

Silakan generate untuk semua 16 pertemuan berdasarkan RPS yang diberikan.
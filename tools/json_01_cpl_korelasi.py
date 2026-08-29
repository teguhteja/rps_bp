# -*- coding: utf-8 -*-
"""
Tingkatkan JSON RPS semester 1 ke standar TSI1107_Agama.
Bagian yang dikerjakan di sini hanya yang bisa diturunkan secara pasti:
  - rumusan CPL diganti verbatim dari Buku Kurikulum
  - sub_cpmk.cpl -> sub_cpmk.taksonomi, ditambah level afektif
  - matriks korelasi CPMK x Sub-CPMK diturunkan dari sub_cpmk.cpmk
  - kalimat baku UTS/UAS sesuai Pedoman BPM 2023
  - notasi waktu TM/PT/BM sesuai SKS
  - kriteria dipecah menjadi blok Kriteria / Bentuk (Tes, Non-Tes)
  - platform daring diseragamkan
Indikator bernomor dan rujukan pustaka per minggu ditulis terpisah.
"""
import json, re, sys, glob, os
from collections import OrderedDict

CPL_FILE = sys.argv[1]
TARGETS = sorted(glob.glob(sys.argv[2]))
CPL = json.load(open(CPL_FILE, encoding='utf-8'))

TIPE = {'S': 'Sikap', 'P': 'Pengetahuan',
        'KU': 'Keterampilan Umum', 'KK': 'Keterampilan Khusus'}

UTS = ('UTS / Evaluasi Tengah Semester : melakukan validasi hasil penilaian, '
       'evaluasi, dan perbaikan proses pembelajaran berikutnya')
UAS = ('UAS / Evaluasi Akhir Semester : melakukan validasi penilaian akhir '
       'dan menentukan kelulusan mahasiswa')
DARING = 'eLearning ITEKES BP (LMS)\nGoogle Meet (sinkron)'
DARING_ASINKRON = 'eLearning ITEKES BP (LMS)\nForum diskusi asinkron'

# Pemetaan level kognitif tertinggi -> level afektif yang sepadan (Krathwohl).
AFEKTIF = {1: 'A2', 2: 'A2', 3: 'A3', 4: 'A4', 5: 'A4', 6: 'A5'}

# Kata kunci -> metode pembelajaran baku Pedoman BPM 2023 (hal. 17-18).
METODE = [
    ('praktik', 'Project Based Learning (PjBL)'),
    ('proyek', 'Project Based Learning (PjBL)'),
    ('presentasi', 'Project Based Learning (PjBL)'),
    ('makalah', 'Collaborative Learning (CbL)'),
    ('studi kasus', 'Contextual Learning (CtL)'),
    ('kasus', 'Contextual Learning (CtL)'),
    ('kelompok', 'Cooperative Learning (CoL)'),
    ('diskusi', 'Small Group Discussion (SGD)'),
    ('simulasi', 'Role-Play & Simulation (RPS)'),
    ('latihan', 'Discovery Learning (DL)'),
]


def taksonomi(nilai):
    """'C2' atau 'C2-C3' -> 'C2, A2' / 'C2-C3, A3' (afektif dari level tertinggi)."""
    nilai = (nilai or 'C2').strip()
    levels = [int(n) for n in re.findall(r'C(\d)', nilai)]
    if not levels:
        return nilai
    return '%s, %s' % (nilai, AFEKTIF[max(levels)])


def cpmk_terkait(teks, semua_cpmk):
    """Baca rujukan CPMK pada Sub-CPMK, termasuk bentuk 'CPMK-1 s.d. CPMK-5'."""
    if 's.d.' in teks or 'sd' == teks.strip():
        return list(semua_cpmk)
    return [k for k in re.findall(r'CPMK-\d+', teks)]


def bangun_korelasi(data):
    kode_cpmk = [c['kode'] for c in data['cpmk']]
    baris = []
    for kode in kode_cpmk:
        row = OrderedDict([('cpmk', kode)])
        for i, sub in enumerate(data['sub_cpmk'], start=1):
            row['m%d' % i] = '√' if kode in cpmk_terkait(sub['cpmk'], kode_cpmk) else ''
        baris.append(row)
    return baris


def blok_kriteria(teks):
    """'Kuis online, tanya jawab' -> blok Kriteria/Bentuk dengan pemisahan Tes & Non-Tes."""
    butir = [b.strip() for b in re.split(r'[;,]', teks or '') if b.strip()]
    tes = [b for b in butir if re.search(r'kuis|ujian|tes\b|uts|uas', b, re.I)]
    non = [b for b in butir if b not in tes]
    baris = ['Kriteria:', '• Pedoman penskoran']
    baris.append('• Rubrik penilaian ' + ('tes' if tes and not non else 'tugas'))
    baris.append('Bentuk:')
    if tes:
        baris.append('Tes: ' + ', '.join(tes))
    if non:
        baris.append('Non-Tes: ' + ', '.join(non))
    return '\n'.join(baris)


def blok_tatap_muka(teks_lama, konteks, meta, nomor_tugas, ujian=False):
    """Susun kolom (5) sesuai notasi SN-Dikti: bentuk, metode, TM, tugas, PT+BM."""
    teori = meta.get('sks_teori') or meta.get('sks_total') or 2
    praktik = meta.get('sks_praktik') or 0
    if ujian:
        baris = ['Bentuk: Ujian', 'Metode: Ujian tertulis',
                 '[TM: 1x(%dx50\')]' % teori,
                 '[PT+BM: (1+1)x(%dx60\')]' % teori]
        return '\n'.join(baris)

    bentuk = 'Praktikum' if praktik and re.search(r'praktik', konteks, re.I) else 'Kuliah'
    metode = 'Ceramah interaktif, tanya jawab'
    for kunci, nama in METODE:
        if kunci in konteks.lower():
            metode = nama
            break
    baris = ['Bentuk: %s' % bentuk, 'Metode: %s' % metode,
             '[TM: 1x(%dx50\')]' % teori]
    if praktik:
        baris.append('[P: 1x(%dx170\')]' % praktik)
    baris.append('Tugas %d: %s' % (nomor_tugas, ringkas_tugas(konteks)))
    baris.append('[PT+BM: (1+1)x(%dx60\')]' % teori)
    return '\n'.join(baris)


def ringkas_tugas(konteks):
    butir = [b.strip() for b in re.split(r'[;,]', konteks) if b.strip()]
    non_tes = [b for b in butir if not re.search(r'kuis|ujian|tes\b', b, re.I)]
    return (non_tes[0] if non_tes else butir[0] if butir else 'latihan terstruktur').lower()


def upgrade(path):
    data = json.load(open(path, encoding='utf-8'))

    # 1. CPL verbatim Buku Kurikulum
    asing = []
    for c in data['cpl_prodi']:
        kode = c['kode']
        if kode in CPL:
            c['deskripsi'] = CPL[kode]
            c['tipe'] = TIPE[kode.split('-')[0]]
        else:
            asing.append(kode)

    # 2. taksonomi
    for sub in data['sub_cpmk']:
        nilai = sub.pop('cpl', None) or sub.get('taksonomi')
        # Idempoten: kalau level afektif sudah ada, biarkan.
        sub['taksonomi'] = nilai if re.search(r'A\d', nilai or '') else taksonomi(nilai)

    # 3. matriks korelasi, disisipkan setelah sub_cpmk
    baru = OrderedDict()
    for k, v in data.items():
        baru[k] = v
        if k == 'sub_cpmk':
            baru['korelasi'] = bangun_korelasi(data)
    data = baru

    # 4. detail per minggu
    tugas = 0
    for d in data['detail']:
        mg = int(d['minggu'])
        ujian = mg in (8, 16)
        # Hanya kriteria yang dipakai sebagai konteks tugas; deskripsi memuat
        # penanda taksonomi '(C2, A2)' yang mengotori ringkasan tugas.
        konteks = d.get('kriteria', '')
        sudah_rapi = konteks.startswith('Kriteria:')
        if ujian:
            if not d['deskripsi'].startswith(('UTS / Evaluasi', 'UAS / Evaluasi')):
                d['deskripsi'] = UTS if mg == 8 else UAS
            d['kriteria'] = ('Kriteria:\n• Kunci jawaban dan pedoman penskoran\n'
                             'Bentuk:\nTes: Ujian tertulis online (LMS)')
            d['daring'] = 'eLearning ITEKES BP (LMS)\nUjian daring sinkron'
        else:
            tugas += 1
            if not sudah_rapi:
                d['kriteria'] = blok_kriteria(konteks)
                d['daring'] = (DARING_ASINKRON
                               if re.search(r'diskusi|forum|kasus', konteks, re.I) else DARING)
        if not d.get('tatap_muka', '').startswith('Bentuk:'):
            d['tatap_muka'] = blok_tatap_muka(d.get('tatap_muka', ''), konteks,
                                              data['meta'], tugas, ujian)

    json.dump(data, open(path, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    return len(data['cpl_prodi']), len(data['korelasi']), asing


for f in TARGETS:
    n_cpl, n_kor, asing = upgrade(f)
    print('%-42s CPL %2d verbatim | korelasi %d baris %s'
          % (os.path.basename(f)[:42], n_cpl, n_kor,
             '| KODE ASING: ' + ','.join(asing) if asing else ''))

# -*- coding: utf-8 -*-
"""
Selaraskan JSON RPS dengan format acuan 'KFR 4560 Cosmeceutical.docx'.

  1. cpl_prodi[].label      : 'CPL 1 (S-01)'
  2. cpmk[].deskripsi       : diakhiri '(CPL 1, CPL 4)'
  3. sub_cpmk[].deskripsi   : diakhiri '(C2, A2) (CPMK-1)'
  4. penilaian[]            : matriks jenis penilaian x bobot x kontribusi CPMK
  5. detail[].minggu        : '1/16'
  6. detail[].kriteria      : blok 'Metode Penilaian: / Kriteria: / Teknik:'
  7. detail[].bobot         : angka tanpa tanda persen
  8. baris UTS/UAS          : kolom (2) memuat daftar Sub-CPMK yang diujikan
"""
import json, re, sys, glob, os
from collections import OrderedDict


def nomor_cpl(data):
    """kode CPL resmi -> nomor urut tampil, mis. {'S-01': 1, 'KU-01': 2}."""
    return {c['kode']: i for i, c in enumerate(data['cpl_prodi'], start=1)}


def cpmk_dari_sub(teks, semua):
    if 's.d.' in teks:
        return list(semua)
    return re.findall(r'CPMK-\d+', teks)


def sub_pada_minggu(d, item):
    m = re.match(r'\s*(Sub-CPMK\s*\d+)', item['deskripsi'])
    return m.group(1).strip() if m else None


def jenis_penilaian(item, mg):
    # Kenali ujian dari isi barisnya, bukan dari nomor minggu: sebagian MK
    # menaruh UTS di minggu 10, dan MK proyek/magang tidak punya ujian tulis.
    teks = '%s %s' % (item.get('deskripsi', ''), item.get('materi', ''))
    if re.search(r'Ujian Tengah Semester|UTS', teks):
        return 'Ujian Tengah Semester'
    if re.search(r'Ujian Akhir Semester|UAS', teks):
        return 'Ujian Akhir Semester'
    if baris_ujian(item) and mg in (8, 16):
        return 'Ujian Tengah Semester' if mg == 8 else 'Ujian Akhir Semester'
    k = item.get('kriteria', '')
    # Terima label sebelum maupun sesudah diubah ke gaya acuan.
    pisah = 'Non-Tes:' if 'Non-Tes:' in k else ('Non Test:' if 'Non Test:' in k else None)
    non = k.split(pisah)[1] if pisah else ''
    if re.search(r'tugas|studi kasus|makalah|esai|laporan|presentasi|proyek', non, re.I):
        return 'Tugas'
    if re.search(r'Tes:|Test:', k):
        return 'Kuis'
    return 'Aktivitas Partisipatif'


URUTAN = ['Kuis', 'Tugas', 'Aktivitas Partisipatif',
          'Ujian Tengah Semester', 'Ujian Akhir Semester']


def bangun_penilaian(data):
    """Sebarkan bobot tiap minggu ke CPMK yang ditopang Sub-CPMK minggu itu."""
    kode_cpmk = [c['kode'] for c in data['cpmk']]
    sub_by_kode = {s['kode']: s for s in data['sub_cpmk']}
    agregat = OrderedDict()
    for item in data['detail']:
        mg = int(str(item['minggu']).split('/')[0])
        bobot = float(str(item['bobot']).rstrip('%').replace(',', '.'))
        jenis = jenis_penilaian(item, mg)

        if mg in (8, 16):
            cakupan = range(1, 8) if mg == 8 else range(9, 16)
            target = []
            for lain in data['detail']:
                if int(str(lain['minggu']).split('/')[0]) in cakupan:
                    kode = sub_pada_minggu(data, lain)
                    if kode and kode in sub_by_kode:
                        target += cpmk_dari_sub(sub_by_kode[kode]['cpmk'], kode_cpmk)
        else:
            kode = sub_pada_minggu(data, item)
            target = cpmk_dari_sub(sub_by_kode[kode]['cpmk'], kode_cpmk) if kode in sub_by_kode else []

        target = sorted(set(target)) or kode_cpmk
        baris = agregat.setdefault(jenis, {'bobot': 0.0, 'per_cpmk': {k: 0.0 for k in kode_cpmk}})
        baris['bobot'] += bobot
        for k in target:
            baris['per_cpmk'][k] += bobot / len(target)

    def rapi(x):
        return ('%.1f' % x).rstrip('0').rstrip('.') + '%'

    hasil, total = [], {'bobot': 0.0, 'per_cpmk': {k: 0.0 for k in kode_cpmk}}
    for jenis in URUTAN:
        if jenis not in agregat:
            continue
        b = agregat[jenis]
        row = OrderedDict([('jenis', jenis), ('bobot', rapi(b['bobot']))])
        for i, k in enumerate(kode_cpmk, start=1):
            row['c%d' % i] = rapi(b['per_cpmk'][k])
        hasil.append(row)
        total['bobot'] += b['bobot']
        for k in kode_cpmk:
            total['per_cpmk'][k] += b['per_cpmk'][k]
    row = OrderedDict([('jenis', 'Total'), ('bobot', rapi(total['bobot']))])
    for i, k in enumerate(kode_cpmk, start=1):
        row['c%d' % i] = rapi(total['per_cpmk'][k])
    hasil.append(row)
    return hasil


def blok_teknik(kriteria):
    """Ubah blok 'Kriteria:/Bentuk:' menjadi 'Kriteria:/Teknik:' gaya acuan."""
    if 'Teknik:' in kriteria:
        return kriteria
    kriteria = kriteria.replace('\nBentuk:\n', '\nTeknik:\n')
    kriteria = kriteria.replace('Tes: ', 'Test: ').replace('Non-Test: ', 'Non Test: ')
    return kriteria.replace('Non-Tes: ', 'Non Test: ')


POLA_MATERI_UJIAN = re.compile(r'^\s*(Materi Minggu|Materi seluruh|Seluruh materi)', re.I)


def baris_ujian(item):
    """Minggu 8/16 tidak selalu berisi ujian.

    Sebagian MK menaruh UTS di minggu 10, dan MK proyek/magang/tugas akhir
    memang tidak punya ujian tulis. Tanpa penjaga ini label ujian akan
    menimpa baris yang sebenarnya berisi materi ajar.
    """
    if POLA_MATERI_UJIAN.match(item.get('materi', '')):
        return True
    try:
        return float(str(item['bobot']).rstrip('%')) >= 10
    except (TypeError, ValueError):
        return False


def upgrade(path):
    data = json.load(open(path, encoding='utf-8'))
    nomor = nomor_cpl(data)
    kode_cpmk = [c['kode'] for c in data['cpmk']]
    sub_by_kode = {s['kode']: s for s in data['sub_cpmk']}

    # 1. label CPL
    for i, c in enumerate(data['cpl_prodi'], start=1):
        c['label'] = 'CPL %d (%s)' % (i, c['kode'])

    # 2. rujukan CPL masuk ke deskripsi CPMK
    for c in data['cpmk']:
        if not re.search(r'\(CPL', c['deskripsi']):
            urut = [nomor[k.strip()] for k in c['cpl'].split(',') if k.strip() in nomor]
            if urut:
                c['deskripsi'] = '%s (%s)' % (c['deskripsi'].rstrip(' .'),
                                              ', '.join('CPL %d' % n for n in sorted(urut)))

    # 3. taksonomi dan CPMK masuk ke deskripsi Sub-CPMK
    for s in data['sub_cpmk']:
        if not re.search(r'\(C\d', s['deskripsi']):
            s['deskripsi'] = '%s (%s) (%s)' % (s['deskripsi'].rstrip(' .'),
                                               s['taksonomi'], s['cpmk'])

    # 4. matriks penilaian dihitung lebih dulu, selagi label kriteria masih asli
    penilaian = bangun_penilaian(data)

    # 5-8. tabel mingguan
    for item in data['detail']:
        mg = int(str(item['minggu']).split('/')[0])
        if mg in (8, 16) and baris_ujian(item):
            cakupan = range(1, 8) if mg == 8 else range(9, 16)
            daftar = []
            for lain in data['detail']:
                if int(str(lain['minggu']).split('/')[0]) in cakupan:
                    kode = sub_pada_minggu(data, lain)
                    if kode and kode not in daftar:
                        daftar.append(kode)
            nomor_sub = [re.search(r'\d+', k).group() for k in daftar]
            ujian = 'Ujian Tengah Semester' if mg == 8 else 'Ujian Akhir Semester'
            item['deskripsi'] = 'Sub-CPMK %s\n(%s)' % (','.join(nomor_sub), ujian)
        item['kriteria'] = blok_teknik(item['kriteria'])
        item['bobot'] = str(item['bobot']).rstrip('%')
        if '/' not in str(item['minggu']):
            item['minggu'] = '%d/16' % mg

    baru = OrderedDict()
    for k, v in data.items():
        if k == 'penilaian':
            continue  # dibangun ulang di bawah; jangan pakai nilai lama
        baru[k] = v
        if k == 'korelasi':
            baru['penilaian'] = penilaian
    if 'penilaian' not in baru:
        baru['penilaian'] = penilaian
    json.dump(baru, open(path, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    return penilaian[-1]['bobot'], len(penilaian) - 1


for f in sorted(glob.glob(sys.argv[1])):
    total, n = upgrade(f)
    print('%-42s penilaian %d jenis, total %s' % (os.path.basename(f)[:42], n, total))

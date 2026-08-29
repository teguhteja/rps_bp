# -*- coding: utf-8 -*-
"""
Turunkan array 'korelasi_cpl' — matriks Korelasi CPL terhadap Sub-CPMK
sesuai Panduan KPT 2024 hal. 118.

Untuk tiap Sub-CPMK dihitung:
  - bobot penilaian  = jumlah bobot minggu yang memuat Sub-CPMK tersebut
  - jumlah minggu    = banyaknya minggu itu
  - sebaran per CPL  = bobot dibagi rata ke CPL yang ditopang CPMK Sub-CPMK ini

Bobot minggu UTS/UAS dibagi rata ke seluruh Sub-CPMK yang diujikan pada
minggu tersebut. Baris terakhir adalah Total; bobotnya harus 100%.
"""
import json, re, sys, glob, os
from collections import OrderedDict


def sub_pada(item):
    """Daftar nomor Sub-CPMK yang dibahas minggu ini."""
    kepala = item['deskripsi'].split('\n')[0]
    m = re.match(r'\s*Sub-CPMK\s*([\d,\s]+)', kepala)
    return [int(n) for n in re.findall(r'\d+', m.group(1))] if m else []


def rapi(x):
    if abs(x) < 0.05:
        return ''
    return ('%.1f' % x).rstrip('0').rstrip('.')


def bulatkan_pas(nilai, sasaran, desimal=1):
    """Bulatkan daftar angka ke `desimal` tempat sehingga jumlahnya tepat
    `sasaran` (metode sisa terbesar). Tanpa ini, pembulatan tiap sel membuat
    kolom tabel tidak berjumlah persis 100."""
    skala = 10 ** desimal
    kasar = [x * skala for x in nilai]
    bulat = [int(x) for x in kasar]
    sisa_total = int(round(sasaran * skala)) - sum(bulat)
    urutan = sorted(range(len(nilai)), key=lambda i: kasar[i] - bulat[i], reverse=True)
    for k in range(sisa_total):
        bulat[urutan[k % len(urutan)]] += 1
    return [b / skala for b in bulat]


def upgrade(path):
    data = json.load(open(path, encoding='utf-8'))
    cpl_kode = [c['kode'] for c in data['cpl_prodi']]
    urut_cpl = {k: i for i, k in enumerate(cpl_kode, start=1)}
    cpmk_cpl = {c['kode']: [k.strip() for k in c['cpl'].split(',') if k.strip()]
                for c in data['cpmk']}
    semua_cpmk = list(cpmk_cpl)

    # nomor pendek untuk header kolom, mis. 'CPL 1'
    for i, c in enumerate(data['cpl_prodi'], start=1):
        c['nomor'] = 'CPL %d' % i

    n_sub = len(data['sub_cpmk'])
    bobot = [0.0] * (n_sub + 1)
    minggu = [0] * (n_sub + 1)
    sebar = [[0.0] * (len(cpl_kode) + 1) for _ in range(n_sub + 1)]

    for item in data['detail']:
        nilai = float(str(item['bobot']).rstrip('%').replace(',', '.'))
        target = [n for n in sub_pada(item) if 1 <= n <= n_sub]
        if not target:
            continue
        for n in target:
            porsi = nilai / len(target)
            bobot[n] += porsi
            minggu[n] += 1 if len(target) == 1 else 0
            sub = data['sub_cpmk'][n - 1]
            rujuk = (semua_cpmk if 's.d.' in sub['cpmk']
                     else re.findall(r'CPMK-\d+', sub['cpmk']))
            kode_cpl = sorted({c for k in rujuk for c in cpmk_cpl.get(k, [])})
            if not kode_cpl:
                continue
            for c in kode_cpl:
                sebar[n][urut_cpl[c]] += porsi / len(kode_cpl)

    # Bobot tiap Sub-CPMK dibulatkan agar jumlahnya tepat 100, lalu sebaran
    # per CPL dibulatkan agar jumlah tiap baris tepat sama dengan bobotnya.
    bobot_pas = bulatkan_pas(bobot[1:n_sub + 1], 100)
    baris = []
    for n in range(1, n_sub + 1):
        b = bobot_pas[n - 1]
        kolom_isi = [i for i in range(1, len(cpl_kode) + 1) if sebar[n][i] > 0]
        sebar_pas = bulatkan_pas([sebar[n][i] for i in kolom_isi], b) if kolom_isi else []
        row = OrderedDict([('sub', data['sub_cpmk'][n - 1]['kode'])])
        nilai_kolom = dict(zip(kolom_isi, sebar_pas))
        for i in range(1, len(cpl_kode) + 1):
            row['p%d' % i] = rapi(nilai_kolom.get(i, 0.0))
        row['bobot'] = rapi(b)
        row['minggu'] = str(minggu[n]) if minggu[n] else ''
        baris.append(row)

    # Total dijumlah dari angka yang benar-benar tercetak, bukan dari nilai
    # sebelum pembulatan — supaya kolom tabel betul-betul berjumlah.
    def nilai(teks):
        return float(teks) if teks else 0.0

    total = OrderedDict([('sub', 'Total')])
    for i in range(1, len(cpl_kode) + 1):
        total['p%d' % i] = rapi(sum(nilai(r['p%d' % i]) for r in baris))
    total['bobot'] = rapi(sum(nilai(r['bobot']) for r in baris))
    total['minggu'] = str(sum(int(r['minggu'] or 0) for r in baris))
    baris.append(total)

    baru = OrderedDict()
    for k, v in data.items():
        if k == 'korelasi_cpl':
            continue                      # dibangun ulang, jangan salin yang lama
        baru[k] = v
        if k == 'penilaian':
            baru['korelasi_cpl'] = baris
    if 'korelasi_cpl' not in baru:
        baru['korelasi_cpl'] = baris
    json.dump(baru, open(path, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    return total['bobot'], total['minggu']


for f in sorted(glob.glob(sys.argv[1])):
    b, m = upgrade(f)
    print('%-42s total bobot %s%%, %s minggu berbobot penuh' % (os.path.basename(f)[:42], b, m))

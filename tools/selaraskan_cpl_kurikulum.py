#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Selaraskan CPL pada JSON RPS dengan Tabel 3.2 Buku Kurikulum.

Tabel 3.2 (Pemetaan CPL dengan Mata Kuliah) adalah acuan resmi CPL mana yang
dibebankan pada tiap MK. Skrip ini membaca tabel itu, lalu untuk tiap JSON:

  - membuang CPL yang tidak ada di Tabel 3.2;
  - menambahkan CPL yang ada di Tabel 3.2 tetapi belum tercantum;
  - merapikan rujukan `cpmk[].cpl` supaya tidak menunjuk kode yang sudah hilang,
    dan memastikan setiap CPL dirujuk minimal satu CPMK.

CPL yang baru ditambahkan dilekatkan ke CPMK yang sudah memuat CPL sedomain
(S/P/KU/KK); kalau tidak ada, ke CPMK dengan CPL paling sedikit. **Penempatan
ini perlu ditinjau dosen pengampu** — yang dijamin skrip ini hanyalah bahwa
himpunan CPL-nya persis sama dengan Tabel 3.2.

Setelah menjalankan skrip ini, jalankan ulang `json_04_format_acuan.py` dan
`json_05_korelasi_cpl.py` agar label CPL dan kedua matriks ikut diperbarui.

Pemakaian:
    python tools/selaraskan_cpl_kurikulum.py "input/rps_json/sem1.1/*.json"
    python tools/selaraskan_cpl_kurikulum.py "input/rps_json/sem2/*.json" --periksa
"""
import glob
import json
import os
import re
import sys

from docx import Document
from docx.oxml.ns import qn

BUKU = 'materi-rps/Buku Kurikulum S1 Sistem Informasi - 20260508.docx'
CPL_RESMI = 'cpl_resmi.json'
INDEKS_TABEL = 3
TIPE = {'S': 'Sikap', 'P': 'Pengetahuan',
        'KU': 'Keterampilan Umum', 'KK': 'Keterampilan Khusus'}
# Tabel 3.1 menyebut Sistem Informasi Manajemen TSI3105; Tabel 3.2 menulis TSI3107.
ALIAS_KODE = {'TSI3107': 'TSI3105'}


def teks_sel(tc):
    """Isi sel dari elemen w:t saja — `cell.text` melewatkan run bersarang."""
    return ' '.join(''.join(t.text or '' for t in tc.iter(qn('w:t'))).split())


def baca_tabel(path=BUKU):
    tbl = Document(path).tables[INDEKS_TABEL]
    kolom = {}
    for i, tc in enumerate(tbl.rows[1]._tr.findall(qn('w:tc'))):
        m = re.fullmatch(r'((?:S|P|KU|KK)-\d{2})', teks_sel(tc))
        if m:
            kolom[i] = m.group(1)
    peta = {}
    for row in tbl.rows:
        tcs = row._tr.findall(qn('w:tc'))
        m = re.search(r'\[(TSI\d+)\]', teks_sel(tcs[0]))
        if not m:
            continue
        kode = ALIAS_KODE.get(m.group(1), m.group(1))
        peta[kode] = [kolom[i] for i in sorted(kolom)
                      if i < len(tcs) and teks_sel(tcs[i])]
    return peta


def urut(kode):
    return (['S', 'P', 'KU', 'KK'].index(kode.split('-')[0]), int(kode.split('-')[1]))


def selaraskan(path, peta, cpl_resmi):
    data = json.load(open(path, encoding='utf-8'))
    kode_mk = data['meta']['kode_mk']
    resmi = peta.get(kode_mk)
    if resmi is None:
        return None, 'tidak ada baris di Tabel 3.2'

    lama = [c['kode'] for c in data['cpl_prodi']]
    dibuang = [k for k in lama if k not in resmi]
    ditambah = [k for k in resmi if k not in lama]

    data['cpl_prodi'] = [
        {'kode': k, 'tipe': TIPE[k.split('-')[0]],
         'deskripsi': cpl_resmi.get(k, ''), 'label': '', 'nomor': ''}
        for k in sorted(resmi, key=urut)]
    for i, c in enumerate(data['cpl_prodi'], start=1):
        c['label'] = 'CPL %d (%s)' % (i, c['kode'])
        c['nomor'] = 'CPL %d' % i

    # rujukan cpmk[].cpl: buang kode yang hilang
    for c in data['cpmk']:
        tetap = [k.strip() for k in c['cpl'].split(',') if k.strip() in resmi]
        c['cpl'] = ', '.join(sorted(set(tetap), key=urut))

    # CPL yang belum dirujuk CPMK mana pun dilekatkan ke CPMK yang sedomain;
    # kalau tidak ada, ke CPMK dengan rujukan paling sedikit. Ini mencakup CPL
    # yang baru ditambahkan MAUPUN yang sejak awal ada tetapi tidak dirujuk.
    dirujuk = {k.strip() for c in data['cpmk'] for k in c['cpl'].split(',') if k.strip()}
    belum = [k for k in resmi if k not in dirujuk]
    for kode in sorted(belum, key=urut):
        domain = kode.split('-')[0]
        kandidat = [c for c in data['cpmk']
                    if any(k.strip().split('-')[0] == domain for k in c['cpl'].split(',') if k.strip())]
        target = (kandidat or sorted(data['cpmk'], key=lambda c: len(c['cpl'])))[0]
        isi = [k.strip() for k in target['cpl'].split(',') if k.strip()] + [kode]
        target['cpl'] = ', '.join(sorted(set(isi), key=urut))

    # rujukan '(CPL n)' pada deskripsi CPMK ikut diperbarui
    nomor = {c['kode']: i for i, c in enumerate(data['cpl_prodi'], start=1)}
    for c in data['cpmk']:
        angka = sorted(nomor[k.strip()] for k in c['cpl'].split(',') if k.strip() in nomor)
        bersih = re.sub(r'\s*\(CPL[^)]*\)\s*$', '', c['deskripsi']).rstrip(' .')
        c['deskripsi'] = '%s (%s)' % (bersih, ', '.join('CPL %d' % n for n in angka)) if angka else bersih

    json.dump(data, open(path, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    return (dibuang, ditambah), None


def main():
    pola = sys.argv[1] if len(sys.argv) > 1 else 'input/rps_json/sem*/*.json'
    hanya_periksa = '--periksa' in sys.argv
    peta = baca_tabel()
    cpl_resmi = json.load(open(CPL_RESMI, encoding='utf-8'))
    print('Tabel 3.2 terbaca: %d mata kuliah, %d tanda\n'
          % (len(peta), sum(len(v) for v in peta.values())))

    for f in sorted(glob.glob(pola)):
        if hanya_periksa:
            data = json.load(open(f, encoding='utf-8'))
            resmi = peta.get(data['meta']['kode_mk'], [])
            punya = [c['kode'] for c in data['cpl_prodi']]
            beda = sorted(set(resmi) ^ set(punya), key=urut)
            print('%-46s %s' % (os.path.basename(f)[:46], ','.join(beda) or 'cocok'))
            continue
        hasil, galat = selaraskan(f, peta, cpl_resmi)
        if galat:
            print('%-46s DILEWATI: %s' % (os.path.basename(f)[:46], galat))
        else:
            dibuang, ditambah = hasil
            print('%-46s -%s +%s' % (os.path.basename(f)[:46],
                                     ','.join(dibuang) or '0', ','.join(ditambah) or '0'))


if __name__ == '__main__':
    main()

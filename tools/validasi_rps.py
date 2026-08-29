#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Periksa konsistensi JSON RPS terhadap Buku Kurikulum dan format acuan.

Pemakaian:
    python tools/validasi_rps.py "input/rps_json/sem1.1/*.json"
    python tools/validasi_rps.py "input/rps_json/sem*/*.json" --ringkas

Status keluar 1 bila ada temuan, supaya bisa dipakai di skrip lain.
"""
import glob
import json
import os
import re
import sys

CPL_RESMI = 'cpl_resmi.json'
KAPASITAS = {'cpl_prodi': 20, 'cpmk': 10, 'sub_cpmk': 12,
             'korelasi': 10, 'penilaian': 10, 'korelasi_cpl': 13,
             'pustaka_utama': 8, 'pustaka_pendukung': 8}


def cpmk_dari(teks, semua):
    return list(semua) if 's.d.' in teks else re.findall(r'CPMK-\d+', teks)


def angka(nilai):
    if nilai is None:
        return 0.0
    teks = str(nilai).rstrip('%').replace(',', '.').strip()
    return float(teks) if teks else 0.0


def periksa(path, cpl_resmi):
    d = json.load(open(path, encoding='utf-8'))
    t = []
    kode_cpl = [c['kode'] for c in d['cpl_prodi']]
    kode_cpmk = [c['kode'] for c in d['cpmk']]

    # --- rantai capaian
    dirujuk = {k.strip() for c in d['cpmk'] for k in c['cpl'].split(',') if k.strip()}
    if [k for k in kode_cpl if k not in dirujuk]:
        t.append('CPL tak dirujuk CPMK: ' + ','.join(k for k in kode_cpl if k not in dirujuk))
    if [k for k in dirujuk if k not in kode_cpl]:
        t.append('CPMK merujuk CPL asing: ' + ','.join(k for k in dirujuk if k not in kode_cpl))
    tanpa_cpl = [c['kode'] for c in d['cpmk'] if not c['cpl'].strip()]
    if tanpa_cpl:
        t.append('CPMK tanpa CPL: ' + ','.join(tanpa_cpl))
    tanpa_sub = [c['kode'] for c in d['cpmk']
                 if not any(c['kode'] in cpmk_dari(s['cpmk'], kode_cpmk) for s in d['sub_cpmk'])]
    if tanpa_sub:
        t.append('CPMK tanpa Sub-CPMK: ' + ','.join(tanpa_sub))

    # --- rumusan CPL harus verbatim Buku Kurikulum
    if cpl_resmi:
        beda = [c['kode'] for c in d['cpl_prodi']
                if c['kode'] in cpl_resmi and c['deskripsi'] != cpl_resmi[c['kode']]]
        if beda:
            t.append('rumusan CPL beda dari Buku Kurikulum: ' + ','.join(beda))
        asing = [c['kode'] for c in d['cpl_prodi'] if c['kode'] not in cpl_resmi]
        if asing:
            t.append('kode CPL di luar Buku Kurikulum: ' + ','.join(asing))

    # --- bobot dan jumlah minggu
    if len(d['detail']) != 16:
        t.append('detail %d minggu (harus 16)' % len(d['detail']))
    total = sum(angka(x['bobot']) for x in d['detail'])
    if abs(total - 100) > 0.01:
        t.append('total bobot %.1f%% (harus 100%%)' % total)

    # --- kapasitas template
    for key, maks in KAPASITAS.items():
        if len(d.get(key, [])) > maks:
            t.append('%s %d melebihi kapasitas %d' % (key, len(d[key]), maks))

    # --- matriks korelasi CPMK x Sub-CPMK
    if 'korelasi' in d:
        for i, s in enumerate(d['sub_cpmk'], start=1):
            harus = set(cpmk_dari(s['cpmk'], kode_cpmk))
            ada = {r['cpmk'] for r in d['korelasi'] if r.get('m%d' % i) == '√'}
            if harus != ada:
                t.append('korelasi Sub-CPMK %d tidak cocok' % i)
                break

    # --- matriks penilaian x CPMK
    if 'penilaian' in d:
        p = d['penilaian']
        if p[-1]['jenis'] != 'Total':
            t.append('penilaian: baris terakhir bukan Total')
        else:
            if angka(p[-1]['bobot']) != 100:
                t.append('penilaian: total bobot %s' % p[-1]['bobot'])
            for i in range(1, len(kode_cpmk) + 1):
                jumlah = sum(angka(r.get('c%d' % i)) for r in p[:-1])
                if abs(jumlah - angka(p[-1].get('c%d' % i))) > 0.15:
                    t.append('penilaian: kolom c%d tidak sama dengan Total' % i)
                    break

    # --- matriks korelasi CPL x Sub-CPMK
    if 'korelasi_cpl' in d:
        k = d['korelasi_cpl']
        if k[-1]['sub'] != 'Total':
            t.append('korelasi_cpl: baris terakhir bukan Total')
        else:
            if len(k) - 1 != len(d['sub_cpmk']):
                t.append('korelasi_cpl: %d baris Sub-CPMK, seharusnya %d'
                         % (len(k) - 1, len(d['sub_cpmk'])))
            if angka(k[-1]['bobot']) != 100:
                t.append('korelasi_cpl: total bobot %s' % k[-1]['bobot'])
            for i in range(1, len(kode_cpl) + 1):
                jumlah = sum(angka(r.get('p%d' % i)) for r in k[:-1])
                if abs(jumlah - angka(k[-1].get('p%d' % i))) > 0.15:
                    t.append('korelasi_cpl: kolom p%d tidak sama dengan Total' % i)
                    break

    # --- format kolom tabel mingguan
    for x in d['detail']:
        if '/' not in str(x['minggu']):
            t.append('minggu %s bukan format n/16' % x['minggu']); break
        if '%' in str(x['bobot']):
            t.append('bobot minggu %s masih memakai tanda persen' % x['minggu']); break
        if not re.match(r'\d+\.\d', x.get('indikator', '')):
            t.append('indikator minggu %s belum bernomor' % x['minggu']); break

    # --- label tampilan
    for i, c in enumerate(d['cpl_prodi'], start=1):
        if c.get('label') != 'CPL %d (%s)' % (i, c['kode']) or c.get('nomor') != 'CPL %d' % i:
            t.append('label/nomor CPL tidak berurutan mulai dari CPL %d' % i)
            break
    return t


def main():
    pola = sys.argv[1] if len(sys.argv) > 1 else 'input/rps_json/sem*/*.json'
    ringkas = '--ringkas' in sys.argv
    cpl_resmi = json.load(open(CPL_RESMI, encoding='utf-8')) if os.path.exists(CPL_RESMI) else None
    if cpl_resmi is None:
        print('Catatan: %s tidak ada, pemeriksaan rumusan CPL dilewati.\n' % CPL_RESMI)

    berkas = sorted(glob.glob(pola))
    if not berkas:
        raise SystemExit('Tidak ada file cocok dengan pola: %s' % pola)

    bermasalah = 0
    for f in berkas:
        temuan = periksa(f, cpl_resmi)
        if temuan:
            bermasalah += 1
        if temuan or not ringkas:
            print('%-46s %s' % (os.path.basename(f)[:46], '; '.join(temuan) or 'OK'))
    print('\n%d file diperiksa, %d bermasalah' % (len(berkas), bermasalah))
    return 1 if bermasalah else 0


if __name__ == '__main__':
    sys.exit(main())

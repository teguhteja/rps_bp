#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Buat dan terapkan lembar isian Bab pustaka per minggu.

Saat ini kolom Materi merujuk seluruh pustaka utama (`[P1, P2, P3]`) untuk
setiap minggu — tidak memberi petunjuk apa pun. RPS acuan menyebut halaman
(`[1, hal 237-329]`); Bab dipilih di sini karena stabil antar cetakan.

Dua mode:

  buat    membuat CSV berisi tiap minggu beserta materinya dan daftar pustaka
          MK tersebut. Dosen tinggal mengisi kolom `bab`.
  terap   membaca CSV yang sudah diisi dan menuliskannya ke JSON, sehingga
          kolom Materi berubah dari `[P1, P2, P3]` menjadi mis. `[P1 Bab 3]`.

Kolom `bab` diisi dengan kode pustaka dan babnya, dipisah titik koma:
    P1 Bab 3; P4 Bab 1-2
Baris yang dibiarkan kosong tidak diubah.

Pemakaian:
    python tools/lembar_bab_pustaka.py buat  "input/rps_json/sem1.1/*.json" bab_pustaka.csv
    python tools/lembar_bab_pustaka.py terap "input/rps_json/sem1.1/*.json" bab_pustaka.csv
"""
import csv
import glob
import json
import os
import re
import sys

KOLOM = ['kode_mk', 'nama_mk', 'minggu', 'materi', 'pustaka_tersedia', 'bab']


def daftar_pustaka(d):
    semua = d.get('pustaka_utama', []) + d.get('pustaka_pendukung', [])
    return ' | '.join('%s = %s' % (p['kode'], re.sub(r'\*', '', p['referensi'])[:60])
                      for p in semua)


def materi_bersih(teks):
    """Kolom materi tanpa baris rujukan pustaka di ujungnya."""
    baris = [b for b in teks.split('\n') if not re.fullmatch(r'\[[^\]]*\]', b.strip())]
    return ' '.join(' '.join(baris).split())


def buat(pola, keluaran):
    baris = []
    for f in sorted(glob.glob(pola)):
        d = json.load(open(f, encoding='utf-8'))
        m = d['meta']
        for x in d['detail']:
            baris.append({
                'kode_mk': m['kode_mk'], 'nama_mk': m['nama_mk'],
                'minggu': x['minggu'], 'materi': materi_bersih(x['materi']),
                'pustaka_tersedia': daftar_pustaka(d), 'bab': ''})
    with open(keluaran, 'w', encoding='utf-8-sig', newline='') as fh:
        w = csv.DictWriter(fh, fieldnames=KOLOM)
        w.writeheader()
        w.writerows(baris)
    print('%d baris ditulis ke %s' % (len(baris), keluaran))
    print('Isi kolom "bab", mis. "P1 Bab 3; P4 Bab 1-2", lalu jalankan mode terap.')


def terap(pola, sumber):
    isian = {}
    with open(sumber, encoding='utf-8-sig', newline='') as fh:
        for r in csv.DictReader(fh):
            bab = (r.get('bab') or '').strip()
            if bab:
                isian[(r['kode_mk'], str(r['minggu']).strip())] = bab
    if not isian:
        raise SystemExit('Kolom "bab" masih kosong semua di %s' % sumber)

    total = 0
    for f in sorted(glob.glob(pola)):
        d = json.load(open(f, encoding='utf-8'))
        kode = d['meta']['kode_mk']
        n = 0
        for x in d['detail']:
            bab = isian.get((kode, str(x['minggu']).strip()))
            if not bab:
                continue
            rujukan = '[%s]' % ', '.join(b.strip() for b in bab.split(';') if b.strip())
            baris = [b for b in x['materi'].split('\n')
                     if not re.fullmatch(r'\[[^\]]*\]', b.strip())]
            x['materi'] = '\n'.join(baris + [rujukan])
            n += 1
        if n:
            json.dump(d, open(f, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
            print('%-46s %2d minggu diperbarui' % (os.path.basename(f)[:46], n))
            total += n
    print('\ntotal %d minggu diperbarui' % total)


def main():
    if len(sys.argv) < 4 or sys.argv[1] not in ('buat', 'terap'):
        raise SystemExit(__doc__)
    (buat if sys.argv[1] == 'buat' else terap)(sys.argv[2], sys.argv[3])


if __name__ == '__main__':
    main()

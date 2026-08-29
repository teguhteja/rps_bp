#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Seimbangkan bobot penilaian mingguan menjadi tepat 100%.

Sejumlah JSON RPS memiliki total bobot 99%-106% — cacat yang sudah ada sejak
data disusun. Skrip ini menurunkan (atau menaikkan) bobot minggu non-ujian
yang paling besar/kecil satu persen demi satu sampai totalnya 100%. Bobot UTS
dan UAS dipertahankan karena porsinya sudah baku.

Pemakaian:
    python tools/json_00_seimbangkan_bobot.py "input/rps_json/sem2/*.json"
"""
import glob
import json
import os
import sys


def minggu_ujian(item):
    kepala = str(item['deskripsi']).split('\n')[0]
    return (str(item['minggu']).split('/')[0].strip() in ('8', '16')
            or kepala.startswith(('UTS', 'UAS'))
            or 'Ujian Tengah Semester' in item['deskripsi']
            or 'Ujian Akhir Semester' in item['deskripsi'])


def seimbangkan(path):
    d = json.load(open(path, encoding='utf-8'))
    nilai = [float(str(x['bobot']).rstrip('%').replace(',', '.')) for x in d['detail']]
    awal = sum(nilai)
    if abs(awal - 100) < 0.01:
        return awal, awal, []

    bebas = [i for i, x in enumerate(d['detail']) if not minggu_ujian(x)]
    if not bebas:
        return awal, awal, []

    jejak = []
    batas = 0
    while abs(sum(nilai) - 100) >= 0.01 and batas < 500:
        batas += 1
        if sum(nilai) > 100:
            kandidat = [i for i in bebas if nilai[i] > 1]
            if not kandidat:
                break
            i = max(kandidat, key=lambda k: nilai[k])
            nilai[i] -= 1
        else:
            i = min(bebas, key=lambda k: nilai[k])
            nilai[i] += 1
        jejak.append(str(d['detail'][i]['minggu']))

    persen = '%' in str(d['detail'][0]['bobot'])
    for x, v in zip(d['detail'], nilai):
        x['bobot'] = ('%g%%' if persen else '%g') % v
    json.dump(d, open(path, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    return awal, sum(nilai), jejak


def main():
    pola = sys.argv[1] if len(sys.argv) > 1 else 'input/rps_json/sem*/*.json'
    for f in sorted(glob.glob(pola)):
        awal, akhir, jejak = seimbangkan(f)
        if jejak:
            print('%-46s %.0f%% -> %.0f%% (minggu diubah: %s)'
                  % (os.path.basename(f)[:46], awal, akhir, ', '.join(sorted(set(jejak)))))
        else:
            print('%-46s %.0f%% (sudah pas)' % (os.path.basename(f)[:46], awal))


if __name__ == '__main__':
    main()

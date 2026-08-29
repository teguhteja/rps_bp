# -*- coding: utf-8 -*-
"""Perbaiki baris 'Tugas N:' pada kolom Bentuk Pembelajaran.

Sebelumnya baris ini mengambil potongan kolom kriteria, sehingga muncul teks
yang bukan tugas ('tanya jawab'). Sekarang jenis tugas diambil dari bentuk
penilaian non-tes, dan pokok bahasannya dari kolom materi.
"""
import json, re, sys, glob, os

JENIS = [('makalah', 'makalah'), ('presentasi', 'presentasi'),
         ('praktikum', 'praktikum'), ('studi kasus', 'studi kasus'),
         ('proyek', 'proyek'), ('esai', 'esai'), ('laporan', 'laporan'),
         ('latihan', 'latihan soal'), ('tugas', 'tugas terstruktur')]


def topik_utama(materi):
    # Kapitalisasi asli dipertahankan: menurunkannya merusak nama diri dan
    # akronim ('Tuhan' -> 'tuhan', 'OS' -> 'os').
    pokok = materi.split('\n')[0].split(',')[0]
    return re.sub(r'\([^)]*\)', '', pokok).strip(' .;')


def jenis_tugas(kriteria):
    bagian = kriteria.lower()
    non = bagian.split('non-tes:')[1] if 'non-tes:' in bagian else bagian
    for kunci, nama in JENIS:
        if kunci in non:
            return nama
    return 'latihan terstruktur'


def upgrade(path):
    data = json.load(open(path, encoding='utf-8'))
    n = 0
    for d in data['detail']:
        baris = d.get('tatap_muka', '').split('\n')
        for i, b in enumerate(baris):
            m = re.match(r'(Tugas \d+):\s*(.*)', b)
            if not m:
                continue
            baru = '%s: %s — %s' % (m.group(1), jenis_tugas(d.get('kriteria', '')),
                                    topik_utama(d.get('materi', '')))
            # Idempoten: baris selalu disusun ulang dari kriteria dan materi,
            # sehingga bisa dijalankan berkali-kali dengan hasil sama.
            if baru != b:
                baris[i] = baru
                n += 1
        d['tatap_muka'] = '\n'.join(baris)
    json.dump(data, open(path, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    return n


for f in sorted(glob.glob(sys.argv[1])):
    print('%-42s baris tugas diperbaiki: %2d' % (os.path.basename(f)[:42], upgrade(f)))

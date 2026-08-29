#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ekstrak daftar CPL resmi dari Buku Kurikulum ke cpl_resmi.json.

Sumber : materi-rps/Buku Kurikulum S1 Sistem Informasi - 20260508.docx, bagian
         3.2 Capaian Pembelajaran Lulusan Program Studi.
Hasil  : {"S-01": "Bertakwa kepada ...", ...} berisi 33 CPL
         (S-01..S-10, P-01..P-05, KU-01..KU-07, KK-01..KK-11).

Catatan: Buku Kurikulum memuat catatan editor "(diperbaiki - sebelumnya
duplikat S-05)" di dalam rumusan S-06. Karena catatan itu memuat kode CPL,
ia HARUS dibuang sebelum teks dipisah per kode; kalau tidak, deskripsi S-05
ikut terpotong dan hilang.

Pemakaian:
    python tools/cpl_resmi.py [buku_kurikulum.docx] [keluaran.json]
"""
import json
import re
import sys
import zipfile

SUMBER = 'materi-rps/Buku Kurikulum S1 Sistem Informasi - 20260508.docx'
KELUARAN = 'cpl_resmi.json'

AWAL = 'I. Aspek Sikap'
AKHIR = 'optimasi pemasaran digital'          # kalimat penutup KK-11
ASPEK = r'I{1,3}V?\.\s*Aspek\s+(?:Sikap|Pengetahuan|Keterampilan Umum|Keterampilan Khusus)'


def ekstrak(path_docx):
    teks = re.sub(r'<[^>]+>', '',
                  zipfile.ZipFile(path_docx).read('word/document.xml').decode('utf-8'))
    mulai = teks.find(AWAL)
    if mulai < 0:
        raise SystemExit('Bagian "%s" tidak ditemukan di %s' % (AWAL, path_docx))
    selesai = teks.find(AKHIR, mulai)
    if selesai < 0:
        raise SystemExit('Penutup daftar CPL tidak ditemukan')

    blok = teks[mulai:selesai + len(AKHIR)]
    blok = re.sub(r'\s*\(diperbaiki[^)]*\)', '', blok)     # buang catatan editor
    blok = re.sub(ASPEK, '|', blok)

    bagian = re.split(r'((?:S|P|KU|KK)-\d{2})', blok)
    return {bagian[i]: re.sub(r'\s+', ' ', bagian[i + 1].strip(' |').strip())
            for i in range(1, len(bagian) - 1, 2)}


def main():
    sumber = sys.argv[1] if len(sys.argv) > 1 else SUMBER
    keluaran = sys.argv[2] if len(sys.argv) > 2 else KELUARAN
    cpl = ekstrak(sumber)

    urut = lambda k: (['S', 'P', 'KU', 'KK'].index(k.split('-')[0]), int(k.split('-')[1]))
    cpl = {k: cpl[k] for k in sorted(cpl, key=urut)}

    if len(cpl) != 33:
        print('PERINGATAN: terbaca %d CPL, seharusnya 33. '
              'Periksa apakah Buku Kurikulum berubah.' % len(cpl))
    with open(keluaran, 'w', encoding='utf-8') as f:
        json.dump(cpl, f, ensure_ascii=False, indent=1)
    print('%d CPL disimpan ke %s' % (len(cpl), keluaran))
    for kode in ('S-01', 'P-01', 'KU-01', 'KK-01'):
        print('  %-6s %s' % (kode, cpl.get(kode, '(TIDAK ADA)')[:70]))


if __name__ == '__main__':
    main()

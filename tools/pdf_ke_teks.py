#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ekstrak teks PDF per halaman.

Dipakai untuk membaca dokumen acuan (Buku Kurikulum, Pedoman BPM, Panduan KPT)
tanpa perlu mengonversinya ke DOCX lebih dulu.

Pemakaian:
    python tools/pdf_ke_teks.py dokumen.pdf
    python tools/pdf_ke_teks.py dokumen.pdf 118 122     # rentang halaman
"""
import sys

import pymupdf          # alias lama `fitz` sudah deprecated


def main():
    if len(sys.argv) < 2:
        raise SystemExit(__doc__)
    doc = pymupdf.open(sys.argv[1])
    awal = int(sys.argv[2]) if len(sys.argv) > 2 else 1
    akhir = int(sys.argv[3]) if len(sys.argv) > 3 else len(doc)

    for i in range(awal - 1, min(akhir, len(doc))):
        print('\n########## HALAMAN %d/%d ##########' % (i + 1, len(doc)))
        print(doc[i].get_text('text'))


if __name__ == '__main__':
    main()

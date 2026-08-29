# -*- coding: utf-8 -*-
"""
Perluas RPS_MK_TSI0000.docx:
  - cpl_prodi  : 8  -> 16 baris   (agar domain S/P/KU/KK muat)
  - cpmk       : 5  -> 10 baris
  - sub_cpmk   : 8  -> 12 baris, field .cpl diganti .taksonomi
  - pustaka    : 3  -> 8  entri (utama & pendukung), diberi label kode [P1]
  - tambah blok "Korelasi CPMK terhadap Sub-CPMK" berupa tabel bersarang
Slot berlebih dibuang saat pengisian oleh edit_rps.py.
"""
import copy, re, sys
from docx import Document
from docx.table import _Cell
from docx.oxml.ns import qn
from docx.oxml import parse_xml, OxmlElement
from docx.shared import Pt, Twips
from docx.enum.text import WD_ALIGN_PARAGRAPH

SRC = sys.argv[1] if len(sys.argv) > 1 else 'template/RPS_MK_TSI0000.docx'

# Kapasitas baru template. Terbesar yang dipakai 54 JSON saat ini:
# 15 CPL (Tugas Akhir), 5 CPMK, 11 Sub-CPMK (Statistika), 6 pustaka.
MAX_CPL, MAX_CPMK, MAX_SUB, MAX_PUSTAKA = 16, 10, 12, 8
# Jumlah slot yang sudah ada di template asal.
SRC_CPL, SRC_CPMK, SRC_SUB = 8, 5, 8
# Lebar sel isi (gridSpan 12) dalam twips, dipakai untuk matriks korelasi.
HOLDER_WIDTH = 13782

doc = Document(SRC)
tbl = doc.tables[4]


def normalize_paragraph(p):
    """Gabungkan run yang terpecah-pecah menjadi satu run (format run pertama)."""
    text = ''.join(r.text for r in p.runs)
    if p.runs:
        p.runs[0].text = text
        for r in p.runs[1:]:
            r._r.getparent().remove(r._r)
    return text


def normalize_row(tr):
    for tc in tr.findall(qn('w:tc')):
        for p_el in tc.findall(qn('w:p')):
            from docx.text.paragraph import Paragraph
            normalize_paragraph(Paragraph(p_el, None))


def retarget(tr, new_index):
    """Ubah semua '[n]' pada placeholder di baris ini menjadi '[new_index]'."""
    for t in tr.iter(qn('w:t')):
        if t.text and '[' in t.text:
            t.text = re.sub(r'\[\s*\d+\s*\]', '[%d]' % new_index, t.text)


def clone_after(tr, count, start_index):
    anchor = tr
    for i in range(count):
        new_tr = copy.deepcopy(tr)
        anchor.addnext(new_tr)
        retarget(new_tr, start_index + i)
        anchor = new_tr
    return anchor


def row_of(placeholder_fragment):
    """Cari indeks baris tabel yang mengandung potongan teks tertentu."""
    for i, row in enumerate(tbl.rows):
        if placeholder_fragment in row_text_raw(row):
            return i
    raise SystemExit('Baris dengan "%s" tidak ditemukan' % placeholder_fragment)


def row_text_raw(row):
    return ''.join(row._tr.itertext())


# --- dikerjakan dari bawah ke atas supaya indeks baris di atasnya tetap sahih ---

# 1. Pustaka: 3 -> 6 entri, tiap entri diberi label kode, mis. "[P1] Kotler ..."
for field in ('pustaka_pendukung', 'pustaka_utama'):
    idx = row_of('{%s[0]' % field)
    tcs = tbl.rows[idx]._tr.findall(qn('w:tc'))
    content_tc = tcs[-1]
    normalize_row(tbl.rows[idx]._tr)
    paras = content_tc.findall(qn('w:p'))
    for n, p_el in enumerate(paras):
        for t in p_el.iter(qn('w:t')):
            if '{' in (t.text or ''):
                t.text = '[{%s[%d].kode}] {%s[%d].referensi}' % (field, n, field, n)
    anchor = paras[-1]
    for n in range(len(paras), MAX_PUSTAKA):
        new_p = copy.deepcopy(paras[-1])
        for t in new_p.iter(qn('w:t')):
            if '{' in (t.text or ''):
                t.text = '[{%s[%d].kode}] {%s[%d].referensi}' % (field, n, field, n)
        anchor.addnext(new_p)
        anchor = new_p

# 2. Blok korelasi CPMK x Sub-CPMK, disisipkan setelah baris sub_cpmk terakhir
label_idx = row_of('Kemampuan akhir tiap tahapan belajar')
last_sub_idx = row_of('{sub_cpmk[%d]' % (SRC_SUB - 1))

label_tr = tbl.rows[label_idx]._tr
matrix_tr = copy.deepcopy(label_tr)
normalize_row(matrix_tr)
# Baris asalnya memakai trHeight hRule="exact" (tinggi mati ~0,2 inci). Kalau
# diwariskan, matriks di dalamnya terpotong di batas halaman. Dibuang supaya
# tinggi baris mengikuti isi.
mt_trPr = matrix_tr.find(qn('w:trPr'))
if mt_trPr is not None:
    for h in mt_trPr.findall(qn('w:trHeight')):
        mt_trPr.remove(h)
mt_cells = matrix_tr.findall(qn('w:tc'))
# sisakan dua sel: label kiri (gridSpan 2, vMerge) dan satu sel isi (gridSpan 12)
for tc in mt_cells[2:]:
    matrix_tr.remove(tc)
holder = mt_cells[1]
tcPr = holder.find(qn('w:tcPr'))
gs = tcPr.find(qn('w:gridSpan'))
if gs is None:
    gs = OxmlElement('w:gridSpan')
    tcPr.append(gs)
gs.set(qn('w:val'), '12')
for p_el in holder.findall(qn('w:p')):
    for t in p_el.iter(qn('w:t')):
        t.text = ''
tbl.rows[last_sub_idx]._tr.addnext(matrix_tr)

# Judul blok ditaruh di dalam sel yang sama dengan matriksnya, bukan sebagai
# baris terpisah, supaya seluruh blok bisa dibuang sekaligus oleh edit_rps.py
# saat JSON tidak memuat data korelasi.
cell = _Cell(holder, tbl)
title = cell.paragraphs[0]
title_run = title.add_run('Korelasi CPMK terhadap Sub-CPMK')
title_run.bold = True
nested = cell.add_table(rows=MAX_CPMK + 1, cols=MAX_SUB + 1)
nested.autofit = False
nested._tbl.tblPr.append(parse_xml(
    '<w:tblBorders xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
    + ''.join('<w:%s w:val="single" w:sz="4" w:space="0" w:color="000000"/>' % e
              for e in ('top', 'left', 'bottom', 'right', 'insideH', 'insideV'))
    + '</w:tblBorders>'))

label_w = 1900
widths = [Twips(label_w)] + [Twips((HOLDER_WIDTH - label_w) // MAX_SUB)] * MAX_SUB
for r_i, row in enumerate(nested.rows):
    for c_i, cell_n in enumerate(row.cells):
        cell_n.width = widths[c_i]
        if r_i == 0:
            text = '' if c_i == 0 else '{sub_cpmk[%d].kode}' % (c_i - 1)
        elif c_i == 0:
            text = '{korelasi[%d].cpmk}' % (r_i - 1)
        else:
            text = '{korelasi[%d].m%d}' % (r_i - 1, c_i)
        p = cell_n.paragraphs[0]
        if c_i > 0:
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run(text)
        run.font.size = Pt(8)

# 3. sub_cpmk: 8 -> 10 baris, dan .cpl -> .taksonomi
src_idx = row_of('{sub_cpmk[%d]' % (SRC_SUB - 1))
src_tr = tbl.rows[src_idx]._tr
normalize_row(src_tr)
clone_after(src_tr, MAX_SUB - SRC_SUB, SRC_SUB)
# Rapikan run dulu: tanpa ini '{sub_cpmk[0].cpl}' terpecah antar-run sehingga
# luput dari regex di bawah.
for row in tbl.rows:
    if '{sub_cpmk[' in row_text_raw(row):
        normalize_row(row._tr)
for i, row in enumerate(tbl.rows):
    for t in row._tr.iter(qn('w:t')):
        if t.text:
            t.text = re.sub(r'\{\s*sub_cpmk\s*\[\s*(\d+)\s*\]\s*\.\s*cpl\s*\}',
                            r'{sub_cpmk[\1].taksonomi}', t.text)

# 4. cpmk: 5 -> 8 baris
src_idx = row_of('{cpmk [%d]' % (SRC_CPMK - 1))
src_tr = tbl.rows[src_idx]._tr
normalize_row(src_tr)
clone_after(src_tr, MAX_CPMK - SRC_CPMK, SRC_CPMK)

# 5. cpl_prodi: 8 -> 12 baris
src_idx = row_of('{cpl_prodi[%d]' % (SRC_CPL - 1))
src_tr = tbl.rows[src_idx]._tr
normalize_row(src_tr)
clone_after(src_tr, MAX_CPL - SRC_CPL, SRC_CPL)

doc.save(SRC)
print('Template diperbarui:', SRC)
print('Tabel RPS sekarang', len(Document(SRC).tables[4].rows), 'baris')

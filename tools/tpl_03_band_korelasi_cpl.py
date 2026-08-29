# -*- coding: utf-8 -*-
"""
Tambahkan band 'Korelasi CPL terhadap Sub-CPMK' ke template RPS.

Formatnya mengikuti Panduan KPT 2024 (Direktorat Pembelajaran dan
Kemahasiswaan) halaman 118: baris = Sub-CPMK, kolom = CPL dalam persen,
ditutup kolom 'Bobot penilaian (%)' dan 'Jumlah Minggu', lalu baris Total.
Band ini yang dikosongkan pada RPS acuan KFR 4560 Cosmeceutical.
"""
import copy, sys
from docx import Document
from docx.table import _Cell
from docx.oxml.ns import qn
from docx.oxml import parse_xml
from docx.shared import Pt, Twips
from docx.enum.text import WD_ALIGN_PARAGRAPH

MAX_CPL, MAX_SUB = 16, 12
HOLDER_WIDTH = 13782

doc = Document(sys.argv[1] if len(sys.argv) > 1 else 'template/RPS_MK_TSI0000.docx')
tbl = doc.tables[4]

anchor = None
for row in tbl.rows:
    if 'Deskrisi' in ''.join(row._tr.itertext()):
        anchor = row._tr
        break
if anchor is None:
    raise SystemExit("baris 'Deskrisi Singkat MK' tidak ditemukan")


def tulis(tc, teks):
    from docx.text.paragraph import Paragraph
    paras = tc.findall(qn('w:p'))
    p = Paragraph(paras[0], None)
    if p.runs:
        p.runs[0].text = teks
        for r in p.runs[1:]:
            r._r.getparent().remove(r._r)
    else:
        p.add_run(teks)
    for extra in paras[1:]:
        tc.remove(extra)


band = copy.deepcopy(anchor)
trPr = band.find(qn('w:trPr'))
if trPr is not None:
    for h in trPr.findall(qn('w:trHeight')):
        trPr.remove(h)
tcs = band.findall(qn('w:tc'))
tulis(tcs[0], 'Korelasi CPL terhadap Sub-CPMK')
for p_el in tcs[1].findall(qn('w:p')):
    for t in p_el.iter(qn('w:t')):
        t.text = ''
anchor.addprevious(band)

cell = _Cell(tcs[1], tbl)
judul = cell.paragraphs[0]
r = judul.add_run('Korelasi CPL terhadap Sub-CPMK (Panduan KPT 2024)')
r.bold = True

kolom = 1 + MAX_CPL + 2                      # label + CPL + bobot + jumlah minggu
nested = cell.add_table(rows=MAX_SUB + 2, cols=kolom)   # header + Sub-CPMK + Total
nested.autofit = False
nested._tbl.tblPr.append(parse_xml(
    '<w:tblBorders xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
    + ''.join('<w:%s w:val="single" w:sz="4" w:space="0" w:color="000000"/>' % e
              for e in ('top', 'left', 'bottom', 'right', 'insideH', 'insideV'))
    + '</w:tblBorders>'))

lebar_label, lebar_tepi = 1700, 1000
sisa = (HOLDER_WIDTH - lebar_label - 2 * lebar_tepi) // MAX_CPL
for r_i, row in enumerate(nested.rows):
    for c_i, sel in enumerate(row.cells):
        sel.width = Twips(lebar_label if c_i == 0
                          else lebar_tepi if c_i > MAX_CPL else sisa)
        if r_i == 0:
            teks = ('' if c_i == 0 else
                    'Bobot penilaian (%)' if c_i == MAX_CPL + 1 else
                    'Jumlah Minggu' if c_i == MAX_CPL + 2 else
                    '{cpl_prodi[%d].nomor}' % (c_i - 1))
        else:
            i = r_i - 1
            teks = ('{korelasi_cpl[%d].sub}' % i if c_i == 0 else
                    '{korelasi_cpl[%d].bobot}' % i if c_i == MAX_CPL + 1 else
                    '{korelasi_cpl[%d].minggu}' % i if c_i == MAX_CPL + 2 else
                    '{korelasi_cpl[%d].p%d}' % (i, c_i))
        p = sel.paragraphs[0]
        if c_i > 0:
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run(teks)
        run.font.size = Pt(7)
        if r_i == 0:
            run.bold = True

doc.save(sys.argv[1] if len(sys.argv) > 1 else 'template/RPS_MK_TSI0000.docx')
print('band ditambahkan: %d baris x %d kolom' % (MAX_SUB + 2, kolom))

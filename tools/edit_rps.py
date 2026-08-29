#!/usr/bin/env python3
"""
RPS Generator - Mengisi template DOCX dengan data dari JSON.
Usage: python edit_rps_bp.py -i data.json [-o output.docx] [--template template.docx]
"""

import argparse
import sys
import copy
import json
import re
import os
from docx import Document
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls, qn
from docx.text.run import Run
from PIL import Image
import io

# Template berada di template/ pada akar repo. Jalurnya diturunkan dari lokasi
# skrip ini supaya tetap ketemu walau skrip dipanggil dari direktori lain.
AKAR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_BAKU = os.path.join(AKAR, 'template', 'RPS_MK_TSI0000.docx')


# Pola placeholder generik, mis. '{nama_mk}' atau '{cpl_prodi[3].kode}'
PLACEHOLDER_RE = re.compile(r'\{[^{}]+\}')
# Placeholder yang menunjuk elemen list, mis. '{cpl_prodi[3].kode}'. Hanya
# placeholder jenis ini yang boleh memicu penghapusan baris/kolom template.
INDEXED_RE = re.compile(r'\{[^{}]*\[\s*\d+\s*\][^{}]*\}')

# Alias nama field supaya template versi baru tetap bisa membaca JSON versi lama.
# Kunci = nama di template, nilai = daftar nama alternatif di JSON.
FIELD_ALIASES = {
    'pangkat': ['pangkat_golongan'],
    'taksonomi': ['cpl'],
    # JSON lama belum punya 'label' ('CPL 1 (S-01)'); pakai kodenya saja.
    'label': ['kode'],
}

def parse_placeholder(placeholder):
    """
    Parse placeholder seperti '{cpl_prodi[0].kode}' menjadi path list.
    Contoh: 'cpl_prodi[0].kode' -> ['cpl_prodi', 0, 'kode']
    """
    # Hapus kurung kurawal dan spasi
    if placeholder.startswith('{') and placeholder.endswith('}'):
        placeholder = placeholder[1:-1]
    placeholder = placeholder.replace(' ', '')
    # Split dengan regex yang menangani tanda kurung siku
    parts = re.split(r'\.|\[|\]', placeholder)
    # Buang string kosong
    parts = [p for p in parts if p]
    # Konversi angka menjadi int
    for i, p in enumerate(parts):
        if p.isdigit():
            parts[i] = int(p)
    return parts

def lookup_key(mapping, key):
    """Ambil key dari dict, dengan fallback ke nama alias (lihat FIELD_ALIASES)."""
    if key in mapping:
        return mapping[key]
    for alias in FIELD_ALIASES.get(key, []):
        if alias in mapping:
            return mapping[alias]
    return None

def get_value(data, path_parts):
    """Ambil nilai dari dictionary/list berdasarkan path parts."""
    # Handle meta variables like {nama_mk} which is actually in data['meta']['nama_mk']
    if len(path_parts) == 1 and isinstance(data, dict) and path_parts[0] not in data and 'meta' in data:
        value = lookup_key(data['meta'], path_parts[0])
        if value is not None:
            return value

    value = data
    try:
        for part in path_parts:
            if isinstance(value, dict):
                value = lookup_key(value, part)
            elif isinstance(value, list):
                value = value[part]
            else:
                return None
            if value is None:
                return None
        return value
    except (IndexError, KeyError, TypeError):
        return None

def set_image_in_front_of_text(picture):
    """Mengubah format gambar menjadi 'In Front of Text' menggunakan modifikasi XML."""
    # Mendapatkan elemen 'inline' dari gambar yang baru ditambahkan
    drawing = picture._inline.getparent()
    inline = drawing.find('.//wp:inline', namespaces=drawing.nsmap)
    
    if inline is None:
        return
    
    # Mendapatkan properti dan konten dari elemen inline
    extent = inline.find('.//wp:extent', namespaces=inline.nsmap)
    effectExtent = inline.find('.//wp:effectExtent', namespaces=inline.nsmap)
    docPr = inline.find('.//wp:docPr', namespaces=inline.nsmap)
    cNvGraphicFramePr = inline.find('.//wp:cNvGraphicFramePr', namespaces=inline.nsmap)
    graphic = inline.find('.//a:graphic', namespaces=inline.nsmap)
    
    if None in [extent, docPr, graphic]:
        return

    # Membuat elemen 'anchor' (floating) baru untuk 'In Front of Text' (behindDoc="0")
    anchor_xml = f'''
        <wp:anchor xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing" 
                   xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"
                   distT="0" distB="0" distL="114300" distR="114300" simplePos="0" relativeHeight="251658240"
                   behindDoc="0" locked="0" layoutInCell="1" allowOverlap="1">
            <wp:simplePos x="0" y="0"/>
            <wp:positionH relativeFrom="column">
                <wp:posOffset>0</wp:posOffset>
            </wp:positionH>
            <wp:positionV relativeFrom="paragraph">
                <wp:posOffset>0</wp:posOffset>
            </wp:positionV>
        </wp:anchor>
    '''
    anchor = parse_xml(anchor_xml)
    
    # Memindahkan elemen-elemen dari inline ke anchor dengan urutan spesifik (WAJIB)
    anchor.append(extent)
    if effectExtent is not None:
        anchor.append(effectExtent)
        
    wrap_none = parse_xml('<wp:wrapNone xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing"/>')
    anchor.append(wrap_none)
    
    anchor.append(docPr)
    if cNvGraphicFramePr is not None:
        anchor.append(cNvGraphicFramePr)
    anchor.append(graphic)
    
    # Mengganti elemen inline dengan anchor di dalam elemen drawing
    drawing.replace(inline, anchor)

def replace_placeholders_in_text(text, data):
    """Ganti semua placeholder dalam string teks."""
    if not text:
        return text
    pattern = r'\{[^{}]+\}'
    def replacer(match):
        placeholder = match.group(0)
        path = parse_placeholder(placeholder)
        value = get_value(data, path)
        if value is None:
            # Jika placeholder tidak ditemukan, kembalikan teks aslinya
            return placeholder
        # Jika value adalah list, gabungkan dengan newline
        if isinstance(value, list):
            return '\n'.join(str(v) for v in value)
        return str(value)
    return re.sub(pattern, replacer, text)

def replace_placeholders_in_paragraph(paragraph, data):
    """Ganti placeholder dalam satu paragraf dengan mempertahankan format dasar, atau tambahkan gambar."""
    # Gabungkan semua run menjadi teks utuh
    full_text = ''.join(run.text for run in paragraph.runs)
    if not full_text.strip():
        return
    
    # Cek khusus untuk image (jika teks mengandung "{dosen_sign}" atau "{dosen_sign_small}")
    is_sign = '{dosen_sign}' in full_text
    is_sign_small = '{dosen_sign_small}' in full_text
    
    if is_sign or is_sign_small:
        image_path = get_value(data, ['dosen_sign'])
        # Tentukan ukuran berdasarkan placeholder yang ditemukan
        img_width = Inches(0.5) if is_sign_small else Inches(1.0)
        
        if image_path and os.path.exists(image_path):
            # Bersihkan teks lama
            for run in paragraph.runs:
                run.text = ''
            # Tambahkan gambar
            run = paragraph.add_run()
            try:
                # docx membutuhkan path absolut atau path yang benar
                abs_path = os.path.abspath(image_path)
                
                # Coba konversi image terlebih dahulu untuk memastikan docx bisa membacanya
                try:
                    with Image.open(abs_path) as img:
                        # Jika gambar memiliki transparansi (RGBA), konversi ke RGB/PNG
                        if img.mode != 'RGB' and img.mode != 'RGBA':
                            img = img.convert('RGBA')
                        img_byte_arr = io.BytesIO()
                        img.save(img_byte_arr, format='PNG')
                        img_byte_arr.seek(0)
                        pic = run.add_picture(img_byte_arr, width=img_width)
                        set_image_in_front_of_text(pic)
                except Exception as img_err:
                    # Fallback
                    pic = run.add_picture(abs_path, width=img_width)  # Sesuaikan ukuran
                    set_image_in_front_of_text(pic)
            except Exception as e:
                # Jika error 'unrecognized image part format', abaikan exception dan jangan hapus teks
                print(f"Warning: Gagal menambahkan gambar {abs_path}: {e}")
            return
        else:
            # Jika tidak ada gambar, kosongkan saja tanda tangannya
            for run in paragraph.runs:
                run.text = ''
            return

    new_text = replace_placeholders_in_text(full_text, data)
    if new_text == full_text:
        return

    # Pertahankan run pertama untuk format, kosongkan run lainnya lebih dulu
    # supaya run italic yang ditambahkan di bawah tidak ikut terhapus.
    if paragraph.runs:
        for run in paragraph.runs[1:]:
            run.text = ''
        write_text_with_markdown_italic(paragraph, new_text)
    else:
        paragraph.add_run(new_text)

def write_text_with_markdown_italic(paragraph, text):
    """
    Tulis teks ke run pertama paragraf, dan ubah penanda *miring* gaya markdown
    (lazim pada judul buku di daftar pustaka) menjadi italic Word yang sebenarnya.
    """
    first = paragraph.runs[0]
    segments = re.split(r'\*([^*\n]+)\*', text)
    if len(segments) == 1:
        first.text = text
        return

    # Hasil split berselang-seling: teks biasa, teks miring, teks biasa, ...
    first.text = segments[0]
    anchor = first._r
    for i, segment in enumerate(segments[1:], start=1):
        if not segment:
            continue
        new_r = copy.deepcopy(first._r)
        anchor.addnext(new_r)
        anchor = new_r
        run = Run(new_r, paragraph)
        run.text = segment
        run.italic = (i % 2 == 1)

def row_text(row):
    """Gabungan teks seluruh sel pada satu baris tabel."""
    return '\n'.join(cell.text for cell in row.cells)

def has_merged_cells(table):
    """True bila tabel memakai gridSpan atau vMerge (tidak aman untuk hapus kolom)."""
    tbl = table._tbl
    return bool(tbl.findall('.//' + qn('w:gridSpan')) or tbl.findall('.//' + qn('w:vMerge')))

def prune_unresolved_columns(table):
    """
    Hapus kolom yang header-nya masih berisi placeholder list yang tidak terisi.
    Dipakai oleh matriks Korelasi CPMK-Sub-CPMK: template menyediakan kolom
    maksimum, JSON menentukan berapa yang benar-benar dipakai.
    Hanya untuk tabel tanpa merge, supaya struktur tidak rusak.
    """
    if not table.rows or has_merged_cells(table):
        return
    doomed = [i for i, cell in enumerate(table.rows[0].cells)
              if INDEXED_RE.search(cell.text)]
    if not doomed:
        return

    tbl = table._tbl
    grid = tbl.find(qn('w:tblGrid'))
    total_before = grid_width(grid)

    for i in sorted(doomed, reverse=True):
        for tr in tbl.findall(qn('w:tr')):
            cells = tr.findall(qn('w:tc'))
            if i < len(cells):
                tr.remove(cells[i])
        if grid is not None:
            grid_cols = grid.findall(qn('w:gridCol'))
            if i < len(grid_cols):
                grid.remove(grid_cols[i])

    widen_columns(table, grid, total_before)

def grid_width(grid):
    """Total lebar tblGrid dalam twips, 0 bila tidak diketahui."""
    if grid is None:
        return 0
    total = 0
    for col in grid.findall(qn('w:gridCol')):
        try:
            total += int(col.get(qn('w:w')))
        except (TypeError, ValueError):
            return 0
    return total

def scale_width(element, factor):
    """Kalikan atribut w:w sebuah gridCol/tcW dengan factor."""
    try:
        element.set(qn('w:w'), str(int(int(element.get(qn('w:w'))) * factor)))
    except (TypeError, ValueError):
        pass

def widen_columns(table, grid, total_before):
    """
    Bagikan lebar kolom yang terhapus ke kolom yang tersisa, supaya tabel tetap
    memenuhi sel induknya dan tidak menyisakan ruang kosong di kanan. Lebar
    masing-masing kolom diskalakan dari nilainya sendiri agar proporsi kolom
    label terhadap kolom centang tetap terjaga.
    """
    total_after = grid_width(grid)
    if not total_before or not total_after or total_after >= total_before:
        return

    factor = total_before / total_after
    for col in grid.findall(qn('w:gridCol')):
        scale_width(col, factor)
    for row in table.rows:
        for cell in row.cells:
            tcPr = cell._tc.find(qn('w:tcPr'))
            tcW = tcPr.find(qn('w:tcW')) if tcPr is not None else None
            if tcW is not None and tcW.get(qn('w:type')) == 'dxa':
                scale_width(tcW, factor)

# Nama array JSON yang slot pertamanya (indeks 0) ternyata kosong. Hampir selalu
# berarti nama field di JSON tidak cocok dengan template, bukan section yang
# memang kosong. Dikumpulkan selama pengisian, dilaporkan di akhir.
EMPTY_ARRAYS = set()

# Array yang wajib ada isinya. Kalau kosong, dokumen hasil cacat berat --
# mis. 'detail' kosong berarti seluruh tabel mingguan hilang. Array di luar
# daftar ini (mis. 'korelasi') memang boleh tidak ada.
REQUIRED_ARRAYS = {'cpl_prodi', 'cpmk', 'sub_cpmk', 'detail', 'pustaka_utama'}

def note_empty_arrays(placeholders):
    """Catat array yang bahkan elemen pertamanya tidak terisi."""
    for ph in placeholders:
        match = re.match(r'\{\s*([A-Za-z0-9_]+)\s*\[\s*0\s*\]', ph)
        if match:
            EMPTY_ARRAYS.add(match.group(1))

def is_unused_slot(before, after):
    """
    True bila teks tadinya berisi placeholder list dan tidak satu pun terisi.
    Artinya slot cadangan di template memang tidak dipakai oleh JSON ini.
    Kalau sebagian terisi, hasilnya False: placeholder sisa sengaja dibiarkan
    tercetak supaya salah ketik nama field ketahuan dan bisa diperbaiki.
    """
    if not before or not after or len(after) != len(before):
        return False
    return all(INDEXED_RE.fullmatch(ph) for ph in after)

def process_cell(cell, data):
    """
    Isi placeholder di satu sel, lalu buang paragraf slot yang tidak terpakai
    (mis. baris ke-5 dan ke-6 daftar pustaka pada MK yang hanya punya 4 pustaka).
    Sel selalu menyisakan minimal satu paragraf, sesuai syarat format DOCX.
    """
    doomed = []
    for paragraph in cell.paragraphs:
        before = PLACEHOLDER_RE.findall(paragraph.text)
        replace_placeholders_in_paragraph(paragraph, data)
        if is_unused_slot(before, PLACEHOLDER_RE.findall(paragraph.text)):
            doomed.append(paragraph)

    if doomed and len(doomed) < len(cell.paragraphs):
        for paragraph in doomed:
            paragraph._p.getparent().remove(paragraph._p)

    for nested in cell.tables:
        replace_placeholders_in_table(nested, data)

def replace_placeholders_in_table(table, data):
    """
    Ganti placeholder di semua sel tabel, lalu buang baris cadangan yang tidak
    terpakai. Template menyediakan lebih banyak baris daripada yang umumnya
    dibutuhkan (mis. 12 baris CPL); baris yang seluruh placeholder-nya tidak
    terisi dibuang agar tidak tercetak mentah sebagai '{cpl_prodi[11].kode}'.
    """
    for indeks, row in enumerate(list(table.rows)):
        before = PLACEHOLDER_RE.findall(row_text(row))
        for cell in row.cells:
            process_cell(cell, data)
        after = PLACEHOLDER_RE.findall(row_text(row))
        # Baris pertama adalah header tabel; label kolomnya harus tetap ada
        # walau seluruh placeholder di dalamnya tidak terisi.
        if indeks == 0:
            continue
        if is_unused_slot(before, after) or holds_empty_nested_table(row):
            note_empty_arrays(after)
            row._tr.getparent().remove(row._tr)

    prune_unresolved_columns(table)

def holds_empty_nested_table(row):
    """
    True bila baris ini memuat tabel bersarang yang tinggal baris header saja.
    Terjadi pada matriks Korelasi CPMK-Sub-CPMK ketika JSON belum memuat kunci
    'korelasi'; seluruh blok (judul + matriks) dibuang, bukan disisakan kosong.
    """
    for cell in row.cells:
        for nested in cell.tables:
            if len(nested.rows) <= 1:
                return True
    return False

def process_document(template_path, json_data, output_path):
    """Proses template DOCX dan simpan ke output."""
    EMPTY_ARRAYS.clear()
    doc = Document(template_path)

    # Proses paragraf di body
    for paragraph in doc.paragraphs:
        replace_placeholders_in_paragraph(paragraph, json_data)
    
    # Proses tabel
    for table in doc.tables:
        replace_placeholders_in_table(table, json_data)
    
    # Proses header dan footer (jika ada)
    for section in doc.sections:
        for paragraph in section.header.paragraphs:
            replace_placeholders_in_paragraph(paragraph, json_data)
        for paragraph in section.footer.paragraphs:
            replace_placeholders_in_paragraph(paragraph, json_data)
        for table in section.header.tables:
            replace_placeholders_in_table(table, json_data)
        for table in section.footer.tables:
            replace_placeholders_in_table(table, json_data)
    
    doc.save(output_path)
    print(f"Berhasil menyimpan RPS ke: {output_path}")

    missing = EMPTY_ARRAYS & REQUIRED_ARRAYS
    if missing:
        print("PERINGATAN: bagian wajib berikut kosong sama sekali di dokumen hasil: "
              + ", ".join(sorted(missing)))
        print("  Kemungkinan besar nama field di JSON tidak cocok dengan template.")
        return False
    return True

def main():
    parser = argparse.ArgumentParser(description='Generate RPS DOCX from JSON template.')
    parser.add_argument('-i', '--input', required=True, help='Input JSON file')
    parser.add_argument('-o', '--output', help='Output DOCX file (optional, defaults to output/filename.docx)')
    parser.add_argument('--template', default=TEMPLATE_BAKU, 
                        help='Template DOCX file (default: RPS_MK_TSI0000.docx)')
    args = parser.parse_args()
    
    # Auto-generate output filename if not provided
    if not args.output:
        # Dapatkan nama file tanpa ekstensi dari input (misal: "data.json" -> "data")
        base_name = os.path.splitext(os.path.basename(args.input))[0]
        # Buat folder output jika belum ada
        os.makedirs('output', exist_ok=True)
        args.output = os.path.join('output', f"{base_name}.docx")

    # Baca JSON
    try:
        with open(args.input, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: File input '{args.input}' tidak ditemukan.")
        return 1
    except json.JSONDecodeError as e:
        print(f"Error: File JSON tidak valid: {e}")
        return 1

    # Cek template
    try:
        ok = process_document(args.template, data, args.output)
    except FileNotFoundError:
        print(f"Error: File template '{args.template}' tidak ditemukan.")
        return 1

    # Status keluar tidak nol supaya run_batch.py menandai file ini gagal dan
    # peringatannya ikut tercetak, bukan tenggelam di output yang dibuang.
    return 0 if ok else 1

if __name__ == '__main__':
    sys.exit(main() or 0)
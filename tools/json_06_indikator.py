#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Susun ulang indikator butir ke-2 dan seterusnya dari pokok bahasan mingguan.

Butir pertama adalah rumusan dosen dan tidak pernah diubah. Butir berikutnya
diturunkan dari kolom `materi` minggu tersebut.

Penurunan versi pertama memenggal `materi` pada setiap koma sehingga
menghasilkan potongan tak bermakna ("Ketepatan menganalisis kelas A") dan
merusak akronim ("IPv4" -> "iPv4"). Versi ini:

  - memenggal pada pemisah tingkat atas (baris baru, titik koma, penomoran),
    lalu pada koma hanya bila kedua sisi masih >= MIN_KATA kata;
  - menggabungkan potongan pendek ke potongan sebelumnya;
  - mempertahankan akronim dan nama diri (IPv4, SQL, Pancasila);
  - memvariasikan kata kerja sesuai level kognitif Sub-CPMK, tidak mengulang
    kata kerja yang sama dalam satu minggu;
  - melewati pokok yang sudah disebut pada butir pertama.

Skrip idempoten: butir turunan selalu dibangun ulang dari `materi`.

Pemakaian:
    python tools/json_06_indikator.py "input/rps_json/sem2/*.json"
"""
import glob
import json
import os
import re
import sys

MIN_KATA = 3
MAKS_BUTIR = 3

# level kognitif -> pilihan kata kerja, dipakai bergantian dalam satu minggu
KERJA = {
    1: ['Ketepatan menyebutkan', 'Ketepatan mengidentifikasi'],
    2: ['Ketepatan menjelaskan', 'Ketepatan menguraikan', 'Kemampuan membedakan'],
    3: ['Ketepatan menerapkan', 'Kemampuan menggunakan', 'Ketepatan menunjukkan'],
    4: ['Ketepatan menganalisis', 'Kemampuan membandingkan', 'Ketepatan memerinci'],
    5: ['Ketepatan mengevaluasi', 'Kemampuan menilai', 'Ketepatan menyimpulkan'],
    6: ['Ketepatan merancang', 'Kemampuan menyusun', 'Ketepatan mengembangkan'],
}


def level(taksonomi):
    angka = [int(n) for n in re.findall(r'C(\d)', taksonomi or '')]
    return max(angka) if angka else 2


def buang_rujukan(materi):
    """Buang baris rujukan pustaka seperti '[P1, P2]' di ujung kolom materi."""
    return [b for b in materi.split('\n') if not re.fullmatch(r'\[[^\]]*\]', b.strip())]


def pisah_koma(teks):
    """Pecah pada koma tingkat atas (koma di dalam kurung diabaikan)."""
    potong, dalam, buf = [], 0, ''
    for ch in teks:
        if ch == '(':
            dalam += 1
        elif ch == ')':
            dalam = max(0, dalam - 1)
        if ch == ',' and dalam == 0:
            potong.append(buf)
            buf = ''
        else:
            buf += ch
    potong.append(buf)
    return [p.strip(' .;') for p in potong if p.strip(' .;')]


def penggal(materi):
    """
    Pecah materi menjadi aspek-aspek yang layak jadi indikator terpisah.

    Titik koma dan penomoran adalah pemisah aspek yang paling dapat dipercaya.
    Koma baru dipakai bila materi hanya berisi satu aspek panjang; potongan
    yang terlalu pendek digabung dengan tetangganya agar tidak muncul indikator
    seperti "Ketepatan menganalisis kelas A".
    """
    aspek = []
    for baris in buang_rujukan(materi):
        for bagian in re.split(r';|(?<=\S)\s+(?=\d+\.\s)', baris):
            bagian = re.sub(r'^\s*\d+\.\s*', '', bagian).strip(' .;')
            if bagian:
                aspek.append(bagian)

    if len(aspek) == 1 and len(aspek[0].split()) > 8:
        aspek = pisah_koma(aspek[0]) or aspek

    # gabungkan potongan yang terlalu pendek dengan tetangga terdekat
    hasil = []
    for a in aspek:
        if hasil and len(a.split()) < MIN_KATA and len(hasil[-1].split()) < 8:
            hasil[-1] += ', ' + a
        else:
            hasil.append(a)
    if len(hasil) > 1 and len(hasil[-1].split()) < MIN_KATA:
        # pop dulu, baru gabung: `hasil[-2] += hasil.pop()` menggeser indeks
        # tujuan sebelum penugasan dan memicu IndexError saat panjangnya 2.
        ekor = hasil.pop()
        hasil[-1] += ', ' + ekor
    return [h for h in hasil if h.split()]


def awali_kecil(teks):
    """Turunkan huruf pertama, kecuali kata itu akronim atau nama diri."""
    kata = teks.split(' ', 1)[0].strip('.,:')
    if len(kata) > 1 and any(c.isupper() for c in kata[1:]):
        return teks                     # IPv4, NoSQL, SQL, MapReduce
    if kata[:1].isupper() and kata.lower() not in KATA_UMUM:
        return teks                     # Pancasila, Hadoop, Agile
    return teks[0].lower() + teks[1:] if teks else teks


# kata berawalan kapital yang sekadar awal kalimat, bukan nama diri
KATA_UMUM = {
    'konsep', 'definisi', 'pengertian', 'jenis', 'model', 'prinsip', 'struktur',
    'arsitektur', 'komponen', 'metode', 'teknik', 'strategi', 'proses', 'sistem',
    'manajemen', 'analisis', 'perancangan', 'implementasi', 'pengujian', 'dasar',
    'penerapan', 'pengelolaan', 'penyajian', 'pemodelan', 'peran', 'fungsi',
    'tahapan', 'langkah', 'kriteria', 'faktor', 'aspek', 'ruang', 'materi',
    'pengantar', 'sejarah', 'tujuan', 'manfaat', 'kelebihan', 'kekurangan',
}


def sudah_disebut(pokok, teks):
    """True bila hampir seluruh kata kunci pokok ini sudah muncul di butir lain."""
    kata = re.findall(r'\w{4,}', pokok.lower())
    if not kata:
        return False
    cocok = sum(1 for k in kata if k in teks)
    return cocok >= max(2, int(len(kata) * 0.8))


def susun(mg, lama, materi, taksonomi):
    butir = [b.strip() for b in (lama or '').split('\n') if b.strip()]
    pertama = re.sub(r'^\d+\.\d+\s*', '', butir[0]) if butir else ''
    hasil = [pertama] if pertama else []

    pilihan = KERJA[level(taksonomi)]
    dipakai = pertama.lower()
    ke = 0
    for pokok in penggal(materi):
        if len(hasil) >= MAKS_BUTIR:
            break
        if sudah_disebut(pokok, dipakai):
            continue
        hasil.append('%s %s' % (pilihan[ke % len(pilihan)], awali_kecil(pokok)))
        dipakai += ' ' + pokok.lower()
        ke += 1
    return '\n'.join('%d.%d %s' % (mg, i, t) for i, t in enumerate(hasil, start=1))


def upgrade(path):
    data = json.load(open(path, encoding='utf-8'))
    sub = {s['kode']: s for s in data['sub_cpmk']}
    n = 0
    for x in data['detail']:
        mg = int(str(x['minggu']).split('/')[0])
        m = re.match(r'\s*(Sub-CPMK\s*\d+)', x['deskripsi'].split('\n')[0])
        taks = sub[m.group(1)]['taksonomi'] if m and m.group(1) in sub else 'C2'
        baru = susun(mg, x.get('indikator', ''), x.get('materi', ''), taks)
        if baru != x.get('indikator'):
            x['indikator'] = baru
            n += 1
    json.dump(data, open(path, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    return n


def main():
    pola = sys.argv[1] if len(sys.argv) > 1 else 'input/rps_json/sem*/*.json'
    for f in sorted(glob.glob(pola)):
        print('%-46s %2d minggu disusun ulang' % (os.path.basename(f)[:46], upgrade(f)))


if __name__ == '__main__':
    main()

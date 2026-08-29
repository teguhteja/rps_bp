# -*- coding: utf-8 -*-
"""
Lengkapi tabel mingguan: deskripsi Sub-CPMK bertaksonomi, indikator bernomor,
dan rujukan pustaka pada kolom materi.

Indikator butir pertama tetap memakai rumusan dosen yang sudah ada; butir
berikutnya diturunkan dari pokok-pokok pada kolom materi, dengan kata kerja
yang menyesuaikan level kognitif Sub-CPMK. Butir turunan ini perlu ditinjau
dosen pengampu, tetapi isinya bersumber dari materi yang memang direncanakan.
"""
import json, re, sys, glob, os

KATA_KERJA = {1: 'Ketepatan menyebutkan', 2: 'Ketepatan menjelaskan',
              3: 'Ketepatan menerapkan', 4: 'Ketepatan menganalisis',
              5: 'Ketepatan mengevaluasi', 6: 'Ketepatan merancang'}


def pecah_topik(materi):
    """Pisahkan pokok bahasan pada kolom materi, abaikan isi dalam kurung."""
    materi = materi.split('\n')[0]
    potong, dalam_kurung, buffer = [], 0, ''
    for ch in materi:
        if ch == '(':
            dalam_kurung += 1
        elif ch == ')':
            dalam_kurung = max(0, dalam_kurung - 1)
        if ch == ',' and dalam_kurung == 0:
            potong.append(buffer)
            buffer = ''
        else:
            buffer += ch
    potong.append(buffer)
    hasil = []
    for p in potong:
        p = re.sub(r'\([^)]*\)', '', p).strip(' .;')
        if len(p) > 3:
            hasil.append(p)
    return hasil


def level(taksonomi):
    angka = [int(n) for n in re.findall(r'C(\d)', taksonomi or '')]
    return max(angka) if angka else 2


def awali_kecil(teks):
    """Turunkan huruf pertama, kecuali kata pertamanya akronim seperti DBMS/SQL/ERD."""
    kata = teks.split(' ', 1)[0].strip('.,')
    if len(kata) > 1 and kata.isupper():
        return teks
    return teks[0].lower() + teks[1:]


def indikator_bernomor(mg, lama, materi, taks, ujian=False, maksimum=3):
    butir = [b.strip() for b in (lama or '').split('\n') if b.strip()]
    if butir and re.match(r'^\d+\.\d', butir[0]):
        return lama                                    # sudah bernomor
    hasil = [butir[0]] if butir else []
    # Minggu ujian tidak diperluas: indikatornya sudah mencakup seluruh materi.
    if not ujian:
        kerja = KATA_KERJA[level(taks)]
        sudah = hasil[0].lower() if hasil else ''
        for topik in pecah_topik(materi):
            if len(hasil) >= maksimum:
                break
            inti = awali_kecil(topik)
            # Lewati kalau pokok ini sudah disebut di indikator dosen.
            if inti.lower() in sudah:
                continue
            hasil.append('%s %s' % (kerja, inti))
            sudah += ' ' + inti.lower()
    return '\n'.join('%d.%d %s' % (mg, i, t) for i, t in enumerate(hasil, start=1))


def upgrade(path):
    data = json.load(open(path, encoding='utf-8'))
    sub_by_kode = {s['kode']: s for s in data['sub_cpmk']}
    kode_utama = [p['kode'] for p in data.get('pustaka_utama', [])]
    rujukan = '[%s]' % ', '.join(kode_utama) if kode_utama else ''

    diubah = 0
    for d in data['detail']:
        mg = int(d['minggu'])
        ujian = d['deskripsi'].startswith(('UTS / Evaluasi', 'UAS / Evaluasi'))

        # deskripsi: sisipkan taksonomi dan rujukan CPMK seperti pada TSI1107
        taks = ''
        m = re.match(r'\s*(Sub-CPMK\s*\d+)\s*:\s*(.*)', d['deskripsi'])
        if m and not ujian:
            kode = m.group(1).replace('Sub-CPMK', 'Sub-CPMK ').replace('  ', ' ').strip()
            sub = sub_by_kode.get(kode)
            if sub:
                taks = sub['taksonomi']
                if '(C' not in d['deskripsi']:
                    d['deskripsi'] = '%s : %s (%s) (%s)' % (
                        kode, m.group(2).rstrip(' .'), taks, sub['cpmk'])
                    diubah += 1

        d['indikator'] = indikator_bernomor(mg, d.get('indikator', ''),
                                            d.get('materi', ''), taks, ujian)

        if rujukan and rujukan not in d.get('materi', ''):
            d['materi'] = d['materi'].rstrip() + '\n' + rujukan

    json.dump(data, open(path, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    return diubah


for f in sorted(glob.glob(sys.argv[1])):
    n = upgrade(f)
    print('%-42s deskripsi bertaksonomi: %2d minggu' % (os.path.basename(f)[:42], n))

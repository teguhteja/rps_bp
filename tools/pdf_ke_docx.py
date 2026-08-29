import os, sys
from pdf2docx import Converter
outdir = sys.argv[1]
os.makedirs(outdir, exist_ok=True)
for p in sys.argv[2:]:
    dst = os.path.join(outdir, os.path.splitext(os.path.basename(p))[0] + '.docx')
    print('==>', os.path.basename(p), flush=True)
    try:
        cv = Converter(p); cv.convert(dst, start=0); cv.close()
        print('    OK', os.path.getsize(dst), 'bytes', flush=True)
    except Exception as e:
        print('    GAGAL:', e, flush=True)

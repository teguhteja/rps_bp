import sys
from docx import Document
from docx.table import Table
from docx.text.paragraph import Paragraph

def iter_block_items(parent):
    from docx.oxml.ns import qn
    body = parent.element.body
    for child in body.iterchildren():
        if child.tag == qn('w:p'):
            yield Paragraph(child, parent)
        elif child.tag == qn('w:tbl'):
            yield Table(child, parent)

doc = Document(sys.argv[1])
ti = 0
for blk in iter_block_items(doc):
    if isinstance(blk, Paragraph):
        t = blk.text.strip()
        if t:
            print("P:", t)
    else:
        ti += 1
        rows = len(blk.rows); cols = len(blk.columns)
        print(f"=== TABLE {ti} ({rows}x{cols}) ===")
        for r_i, row in enumerate(blk.rows):
            cells = []
            seen = set()
            for c in row.cells:
                if id(c._tc) in seen: continue
                seen.add(id(c._tc))
                cells.append(" ".join(c.text.split()))
            print(f"  R{r_i}: " + " | ".join(cells))

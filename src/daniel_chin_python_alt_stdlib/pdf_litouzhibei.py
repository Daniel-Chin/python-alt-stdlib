'''
LiTouZhiBei(Chinese: '\xe5\x8a\x9b\xe9\x80\x8f\xe7\xba\xb8\xe8\x83\x8c').  
Converts pdf from [p1, p2...] to [p1, p1, p2, p2...]  
'''
from myfile import sysArgvOrInput
import sys
import os
from pdfrw import PdfReader, PdfWriter
from jdt import Jdt

if __name__ == '__main__':
    inpfn = sysArgvOrInput()
    outfn = os.path.join(os.path.dirname(inpfn), 'LiTouZhiBei.' + os.path.basename(inpfn))
    writer = PdfWriter(outfn)
    pages = PdfReader(inpfn).pages
    jdt = Jdt(len(pages))
    for i, page in enumerate(pages):
        writer.addpages([page] * 2)
        jdt.acc()
    writer.write()
    jdt.complete()
    print('written to', outfn)

#!/usr/bin/python3

import sys
import json
import struct

filename = sys.argv[1]

def parsecomment(text):
        champs = [b'Negative prompt', b'Steps', b'Sampler', b'CFG scale', b'Seed', b'Face restoration',
                  b'Size', b'Model hash', b'Denoising strength', b'First pass size' ]
        
        ind = []
        for f in champs :
            try:
                i = text.index(f)
                ind.append((i,f))
            except ValueError:
                pass 
                #print(f"[-] Warning, no {str(f, encoding='utf8')}")
                
        ind = sorted(ind)
        ret = {}
        i,f = ind[0]
        ret["prompt"] = str(text[11:i], encoding='utf8')
        for (i, f),(i1,f1) in zip(ind, ind[1:]):
            fs = str(f, encoding='utf8')
            ret[fs] = str(text[i+len(f)+2:i1], encoding='utf8')
            if(ret[fs][-2:] == ', '):
                ret[fs] = ret[fs][:-2]
        fs = str(f1, encoding='utf8')
        ret[fs] = str(text[i1+len(fs)+2:],encoding='utf8')
        return ret
                
            
def parsechunk(data):
    i = 8
    while i < len(data):
        size, = struct.unpack(">I", data[i:i+4])
        typ =  data[i+4:i+8]
        if typ == b'tEXt':
            return data[i + 8:i + 8 + size]
        i += size + 12
                    

                    
with open(filename, 'rb') as f:
    data = f.read()
comment = parsechunk(data)
infos = parsecomment(comment)
print(json.dumps(infos, indent=True))

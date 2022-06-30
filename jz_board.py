from zlib import decompress
from gc import collect
from sys import exit
from os import getcwd, chdir

VERSION = "1.0-board"

def decompress(filee, directory="."):
    print(f"Decompressing {filee} into {directory if directory != '.' else 'the current directory'}")
    with open(filee,"rb") as inpf:
        dataa = inpf.read()
        inpf.close()
        del inpf
    olddir = getcwd()
    chdir(directory)
    unz = decompress(dataa)
    del dataa
    collect()
    collect()
    ctlstr = str(unz[:unz.find(bytes("|eocf","utf-8"),0)],"utf-8")
    ctlarr = ctlstr.split()
    offset = unz.find(bytes("|eocf","utf-8"),0)+5
    
    for i in range(0, int(len(ctlarr)), 2): # skipping over len
        fname = ctlarr[i]
        lco = int(ctlarr[i+1])
        print(f"Extracting: {fname} ({str(lco)} bytes)")
        try:
            with open(fname,"wb") as fout:
                fout.write(unz[offset:offset+lco])
                fout.flush()
                fout.close()
                del fout
        except OSError:
            print("Error: Could not write file")
            exit(1)
        offset += lco
        del lco, fname
        collect()
        collect()
    del unz
    chdir(olddir)
    del olddir
    exit(0)

def help():
    print(f"""
        About: jz file compression module, board edition.
               Version: {VERSION} - Author: Bill Sideris (bill88t)
               This project is licenced under the MIT licence.
        Usage: jz.decompress(\"jz_archive_name\")
    """)
    exit(0)

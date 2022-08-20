from zlib import decompress as zdecompress
from gc import collect
from os import getcwd, chdir

VERSION = "1.2.1-board"


def decompress(filee, directory=".", quiet=False):
    if not quiet:
        print(
            f"Decompressing {filee} into {directory if directory != '.' else 'the current directory'}"
        )
    with open(filee, "rb") as inpf:
        dataa = inpf.read()
    olddir = getcwd()
    chdir(directory)
    unz = zdecompress(dataa)
    del dataa
    collect()
    collect()
    ctlstr = str(unz[: unz.find(bytes("|eocf", "utf-8"), 0)], "utf-8")
    ctlarr = ctlstr.split()
    offset = unz.find(bytes("|eocf", "utf-8"), 0) + 5
    for i in range(0, int(len(ctlarr)), 2):
        fname = ctlarr[i]
        lco = int(ctlarr[i + 1])
        if not quiet:
            print(f"Extracting: {fname} ({lco} bytes)")
        try:
            with open(fname, "wb") as fout:
                fout.write(unz[offset : offset + lco])
                fout.flush()
        except OSError:
            print("Error: Could not write file")
            return 1
        offset += lco
        del lco, fname
        collect()
        collect()
    del unz
    chdir(olddir)
    del olddir
    return 0


def help():
    print(
        f"""
        About: jz file compression module, board edition.
               Version: {VERSION} - Author: Bill Sideris (bill88t)
               This project is licenced under the MIT licence.
        Usage: jz.decompress(\"jz_archive_name\")
    """
    )
    return 0

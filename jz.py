import zlib
from gc import collect
from sys import argv, exit
from os import getcwd, chdir

VERSION = "1.0"

def compress(*argv):
    """
    Note: compression cannot be done on the controller
          itself at the moment.
    """
    
    #starting print
    objc = len(argv)-1
    targetfile = argv[objc]
    print(f"Compressing {str(objc)} files onto {targetfile}")
    
    #let's create the string
    ctlstr = ""
    datastr = bytes()
    # the control string format is:
    #   file1 file1len file2 file2len |eocf
    for i in range(0, objc):
        ctlstr += f"{argv[i]} " # do not remove the whitespace
        try:
            with open(argv[i], "rb") as togetlelen:
                inpt = togetlelen.read()
                togetlelen.close()
                del togetlelen
                ctlstr += f"{str(len(inpt))} " # do not remove the whitespace
                print(f"Loading: {argv[i]} ({str(len(inpt))} bytes)")
                datastr += inpt #copying bytes, not str
                del inpt
        except OSError:
            print(f"Error: Could not open file {argv[i]}")
            exit(1)
        del i
        collect()
        collect()
    del objc
    ctlstr += "|eocf"
    total = bytes(ctlstr,"utf-8") + datastr
    del datastr
    del ctlstr
    collect()
    collect()
    
    #zlib em
    out = zlib.compress(total)
    del total
    
    #write to .jz
    with open(targetfile, "wb") as jzfile:
        jzfile.write(out)
        del out
        jzfile.flush()
        jzfile.close()
        del jzfile
    del targetfile
    
    #done
    exit(0)

def decompress(filee, directory="."):
    print(f"Decompressing {filee} into {directory if directory != '.' else 'the current directory'}")
    
    #dump file inputted
    with open(filee,"rb") as inpf:
        dataa = inpf.read()
        inpf.close()
        del inpf
    
    #switch to target dir
    olddir = getcwd()
    chdir(directory)
    
    #unzlib data
    unz = zlib.decompress(dataa)
    del dataa
    collect()
    collect()
    
    #read control string
    ctlstr = str(unz[:unz.find(bytes("|eocf","utf-8"),0)],"utf-8")
    ctlarr = ctlstr.split()
    
    #set stepper variables
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
    
    #cleanup
    del unz
    
    #switch back to start dir
    chdir(olddir)
    del olddir
    exit(0)

def help():
    print(f"""
        About: jz file compression module.
               Version: {VERSION} - Author: Bill Sideris (bill88t)
               This project is licenced under the MIT licence.
        Usage: jz.compress(\"file1\", \"file2\", \"jz_archive_name\")
               jz.decompress(\"jz_archive_name\")
    """)
    exit(0)

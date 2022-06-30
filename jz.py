import zlib
from gc import collect
from sys import argv
from os import getcwd, chdir

VERSION = "0.0.1"

def compress(*argv):
    """
    Note: compression cannot be done on the controller
          itself at the moment.
    
    Example:
    >>> import jz
    >>> jz.compress("file1", "file2", "target_filename")
    """
    
    #starting print
    objc = len(argv)-1
    targetfile = argv[objc]
    print(f"Compressing {str(objc)} files onto {targetfile}")
    
    #let's create the control string
    ctlstr = ""
    # the control string format is:
    #   file1 file1len file2 file2len |eocf
    for i in range(0, objc):
        ctlstr += i
        with open(i, "rb") as togetlelen:
            inpt = togetlelen.read()
            togetlelen.close()
            del togetlelen
        del i
        collect()
        collect()
        
    
    #cleanup
    del objc
    del targetfile

def decompress(filee, directory="."):
    """
    Example:
    >>> import jz
    >>> jz.decompress("jzfile", directory="path")
    
    The file will be decompressed onto "directory". "." if not specified
    """
    olddir = getcwd()
    chdir(directory)
    
    chdir(olddir)
    del olddir
    collect()
    
def help():
    print(f"""
        About: jz file compression module.
               Version: {VERSION} - Author: Bill Sideris (bill88t)
               This project is licenced under the MIT licence.
        Usage: jz.compress(\"file1\", \"file2\", \"jz_archive_name\")
               jz.decompress(\"jz_archive_name\")
    """)

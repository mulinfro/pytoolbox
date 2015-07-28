import re,sys,os
from iotool import getFileText

def cd(path):
    os.chdir(path)
    return "SUCCESS pwd: " + path 

def ls(path,filetype=None):
    files = os.listdir(path)
    if not filetype:
        onlyfiles = files
    elif filetype == '-file':
        onlyfiles = [ f for f in files if os.path.isfile(join(path,f)) ]
    else:
        onlyfiles = [ f for f in files if f.endswith(filetype)]
    return onlyfiles

def echo(ss):
    return ss

# at least one file
def cat(files):
    if hasattr(files, '__iter__'):
        txts = map(getFileText,files)
        txts = ''.join(txts)
    else:
        txts = getFileText(files)
    return txts

def edit(filename):
    pass


if __name__ == '__main__':
    path = os.path.abspath(os.path.dirname(__file__))
    os.chdir(path)
    argv = sys.argv
    print cat(["shell.py","test.txt"])


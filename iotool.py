# -*- coding: utf-8 -*-
"""
interface of io: 
1.read files to different type data
2.dump different type data to files
"""
import sys,os
import json
from util import prompt

def ioflag(s):
    SUCCESS = "success"
    FAILED = 'failed'
    return SUCCESS + ': ' + s

def stdPrint(s):
    prompt()
    print str(s)

# read file to text
def getFileText(file,md='r'):
    with open(file,md) as f:
        text = f.read()
    return text

# read file by lines
def getFileLines(file):
    with open(file,'r') as f:
        text = f.readlines()
    return text

def getLines(file):
    lines = getFileLines(file)
    lines = [ line.strip() for line in lines]
    return lines

# load from file
def load(file):
    text = getFileText(file)
    try:
        obj = json.loads(text)
        return obj
    except:
        return text


# output a string to file
def write(file,str2w, tp='w'):
    with open(file,tp) as f:
        f.write(str2w)
    return ioflag('write')

# add a new line to file
def addLineToFile(file,str2w):
    write(file,str2w + '\n', 'a')
    return ioflag('addLineToFile')

# var dump to file; use json
def dump(file,var,tp='w'):
    obj = json.dumps(var)
    write(file,obj,tp)
    return ioflag('dump')

# print list to stdout
# each element is a line
def showList(lt):
    for e in lt:
        print e
    return ioflag('printList')

def showIdxList(lt):
    for idx,e in zip(xrange(len(lt)), lt):
        print idx,  ':\t' , e
    return ioflag('printIdxList')

def list2lines(dlist):
    lt = [ str(ele) for ele in dlist]
    return "\n".join(lt)

# write list to a file
def writeList(out,dlist):
    with open(out,'w') as of:
        of.write(list2lines(dlist))
    return ioflag('writeList')

if __name__ == '__main__':
    path = os.path.abspath(os.path.dirname(__file__))
    os.chdir(path)
    argv = sys.argv
    print eval('load')
    print printIdxList(list("abcdefghijklmnopqrstuvw"))

# -*- coding: utf-8 -*-
"""
some utility functions
"""
import re,sys,traceback

def encase2list(arg):
    if type(arg) == list:
        return arg
    else:
        return [arg]

def wraplist(arg):
    return [arg]

def car(iterable):
    assert(type(iterable) in [list,str,tuple])
    return iterable[0]

def cdr(iterable):
    assert(type(iterable) in [list,str,tuple])
    return iterable[1:]

def cadr(iterable):
    return car(cdr(iterable))

def cons(a,b):
    return (a,b)

def prompt(mes='',p=':>'):
    print p,
    if mes: print mes

def biPartition(commd,sp):
    idx = commd.find(sp)
    assert(idx >=0)
    return (commd[0:idx],commd[idx+len(sp):])

def replace(word,toword,line, num=None):
    if type(num) == int and num >= 1:
        spts = line.split(word,num)
    else:
        spts = line.split(word)
    return toword.join(spts)


def splitBy(mode,text):
    modes = mode.split('|')
    for m in modes:
        if isContain(m,text):
            return text.split(m)
    return [text]

def isContain(v,container):
    typ = type(container)
    if typ in [list,str,tuple,dict,set]:
        return v in container
    else:
        print typ
        raise TypeError

def findall(pattern, text):
    matches = re.findall(pattern,text)
    return matches

def flip(func):
    def flipfunc(a,b):
        return func(b,a)
    return flipfunc

# map reduce
def merge(lst):
    lst.sort()
    dct = {}
    for (k,v) in lst:
        if dct.has_key(k): dct.append(v)
        else: dct = [v]
    return dct.items()

def echof(x):
    return lambda x:x

def mergeList(lst):
    out = []
    for lt in lst:
        if type(lt) is list:
            out.extend(lt)
        else:
            out.append(lt)
    return out
            
def mrReduce(rdc, ktran ,lst):
    keys,vals = zip(*lst)
    keys = map(keys,ktran)
    vals = map(keys,rdc)
    return zip(keys,vals)

def mrMap(mkey, mval, lst):
    keys = map(lst,mkey)
    vals = map(lst,mval)
    return zip(keys,vals)

if __name__ == '__main__':
    a = [1]
    b = [1,2]
    c = '1'
    d = '12'
    print car(a)
    print cdr(a)
    print car(b)
    print cdr(b)
    print car(c)
    print cdr(c)
    print car(d)
    print cdr(d)
    pass

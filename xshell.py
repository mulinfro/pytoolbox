from funcManager import *
from functools import partial
import iotool,pytool
from util import encase2list,prompt,splitBy,car,cdr
from iotool import stdPrint
import re,sys,os,traceback

configure()

def replaceAlias(commd):
    alias = allAlias()
    for w,tw in alias.items():
        commd = replace(w,tw,commd)
    return commd
    
# main function of shell
def commandShell():
    while True:
        prompt()
        commd = raw_input().strip()
        addToHistory(commd)
        if commd == 'quit':
            prompt('good bye!')
            return
        try:
            commandParse(commd) 
        except Exception,e:
            exstr = traceback.format_exc()
            prompt(exstr)

def commandSplit(commd):
    instr = False
    for c in command:
        pass


# parse command
def commandParse(commd,std=stdPrint):
    commd = replaceAlias(commd)
    eles = splitBy('=>|=|>>|>',commd)
    assert(len(eles) <= 2)
    if len(eles) == 1: 
        if std: std(myeval(car(eles)))
    elif commd.count('=>') == 1:
        var, val = car(cdr(eles)), myeval(car(eles))
        assign(var, val)
    elif commd.count('=') == 1:
        var, val = car(eles) , myeval(car(cdr(eles)))
        assign(var, val)
    elif commd.count('>>') == 1:
        vals = map(myeval,eles)
        ioredirect(*vals,mode = 'a')
    elif commd.count('>') == 1:
        vals = map(myeval,eles)
        ioredirect(*vals,mode='w')
    else:
        prompt('undefined syntax')

# assign value to variable
def assign(var,val):
    var = var.strip()
    assert(val is not None)
    if not isPreDefined(var):
        _assign(var,val)
    else:
        prompt('can not cover predefined functions')

def _assign(var,val):
    global _valtmp
    _valtmp = val
    exec(var + '=' + '_valtmp', globals())

def ioredirect(val,out,mode='w'):
    if type(val) == str: iotool.write2file(out,val,mode)
    try:
        iotool.dump(out,val,mode)
    except:
        iotool.write2file(out,str(val),mode)

def isPipe(commd):
    return commd.count('|') > 0

def isFuncComp(commd):
    return commd.count('$') > 0

def isCrried(commd):
    return len(commd) > 0 and car(commd) == '!' 

def isMaped(commd):
    return len(commd) > 0 and car(commd) == '~' 

# eval : pipe and func
def myeval(commd):
    commd = commd.strip()
    if isPipe(commd):
        val = pipe(commd)
    else:
        val = parseFunc(commd)
    return val

# eavl base expression 
def evalPyExp(commd):
    try:
        return eval(commd)
    except Exception:
        return None

def lookupVariables(var):
    if isPreDefined(var): return preDefined(var)
    else: return evalPyExp(var)
    
def getPrefix(ss):
    ss = ss.strip()
    if ss and car(ss) in PREFIXS: return (car(ss), cdr(ss))
    else: return ('',ss)

def baseElementEval(ble):
    ble = ble.strip()
    if isFuncComp(ble):
        return funcCompose(ble)
    elif isBlock(ble):
        return parseBlock(ble)
    return lookupVariables(ble)

def isBlock(ble):
    return len(ble) > 2 and ble[0] == '(' and \
            ble[-1] == ')' and not isCommaSplitEles(ble[1:-1])

def isCommaSplitEles(ble):
    blocks, instr = 0, False
    lp, rp = '([{', ')]}'
    for e in ble: 
        if e is '"': instr = not instr
        if instr: continue
        if e in lp: blocks = blocks + 1
        elif e in rp: blocks = blocks - 1
        elif e is ',': 
            if blocks == 0: return True
    return False

def parseBlock(ble):
    ble = ble.strip()[1:-1]
    return parseFunc(ble)

def parseFunc(commd):
    prefix,eles = parseFuncExp(commd)
    assert(len(eles) > 0)
    vals = map(baseElementEval,eles)
    if None in vals:
        return eval(commd)
    func, args = car(vals), cdr(vals)
    if not hasattr(func,'__call__'):
        assert(len(args) == 0)
        return func
    elif prefix == '':
        return parseFuncCall(func, *args)
    elif isMaped(prefix):
        return parseFuncCall(map, func, *args)
    else:
        raise NameError

def parseFuncCall(func, *args):
    try:
        val = func(*args)
    except:
        val = partial(func,*args)
    return val
        
def parseFuncExp(commd):
    eles = []
    prefix, rest = getPrefix(commd)
    while rest:
        frt,rest = getEle(rest)
        eles.append(frt)
    return (prefix,eles)

# exp analysis;  get basic part of expression
def getEle(commd):
    commd = commd.strip()
    if not commd : return (None,None)
    if car(commd) in '[{("':
       (frt,rest) = pytool.getFirstPareCont(commd, car(commd) ) 
    else:
       eles = commd.split('$')     #  A $ B $ C args -> [A , B,c args]
       part1, part2 = eles[:-1], eles[-1]
       tmp = part2.strip().split(' ', 1)   # tmp = [ C arg1 arg2 ..]
       part2, part3 = tmp[0], tmp[1:]
       part1.append(part2)
       frt = '$'.join(part1).strip()
       rest = ' '.join(part3)

    return (frt,rest)

# pipe implement
def pipe(commd):
    commds = commd.split('|')
    init = car(commds)
    rest = cdr(commds)
    return reduce(pipetransfer,rest,myeval(init))

def pipetransfer(arg,func):
    return (myeval(func))(arg)

# function compose
class _compFun(partial):
    def __mul__(self, y):
        f = lambda *args, **kwargs: self.func(y(*args, **kwargs))
        return _compFun(f)

def fcp():
    return _compFun(lambda arg: arg)

def funcCompose(commd):
    commds = commd.split('$')
    commdexe = [myeval(commd) for commd in commds]
    return reduce(lambda x,y: x*y, commdexe, fcp())

# 
def sh(file,stdout=stdPrint):
    lines = iotool.getLines(file)
    map(partial(commandParse,std=stdout),lines)

if __name__ == '__main__':
    path = os.path.abspath(os.path.dirname(__file__))
    os.chdir(path)
    argv = sys.argv
    ble = '"dasd,fsda ,fsdaf ,"," fasdf fesdf,afsd,fas",1, 2 ,3,  func argv'
    blee = '{1:"2", "2":[1,"2"]}'
    print type(myeval(blee))
    commandShell()
    sh("test.txt")
    lines = myeval( '"test.txt" | getFileLines ')
    for line in lines:
        print line.strip()
        commandParse(line)

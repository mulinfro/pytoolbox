from funcManager import *
from functools import partial
import iotool,pytool
from util import encase2list,prompt,splitBy,car,cdr,caar
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

def lexerWrap():
    types = {'$':'COMP', '~':'MAP', '[':'LIST', '(':'BLOCK','{':'DICT','_':'VAR', '"':'STR'
            ,'|':'PIPE', '=>':'IO RASSIGN','=':'IO LASSIGN', '>':'IO WRITE','>>':'IO APPEND'
            ,'%':'ALIAS'} 
    legalSuccTypes = {'$':'VAR', '~':'VAR', '|':'VAR', '=>':'VAR','=':'ALL', '>':'STR','>>':'STR'} 
    def lexerErrorAna(etype, rtype):
        if etype is not 'ALL' and etype is not rtype:
            prompt('invalid syntax: after $ need function; given %s:'%ltype)
            raise TypeError

    def getType(commd):
        t = _getType(commd[0:2])
        if t: return t
        t = _getType(car(commd))
        if t: 
            return t
        else:
            prompt("error type analysis in %s"%commd)
            raise TypeError
        

    def _getType(ch):
        if ch in types:
            return types[ch]
        elif str.isalnum(ch) or ch in ['-']:
            return types['_']
        else:
            return None

    def legalSucc(ch):
        if ch in legalSuccTypes:
            return legalSuccTypes[ch]
        return 'ALL'

    return (lexerErrorAna, getType, legalSucc)

(lexerErrorAna, getType, legalSucc) = lexerWrap()
# exp analysis;  get basic part of expression
def getEle(commd):
    etp = getType(commd)
    if etp in ['COMP','MAP','PIPE','IO LASSIGN', 'IO WRITE']:
       val, rest = None, cdr(commd)
    elif etp in ['LIST','BLOCK','DICT','STR']:
       (val,rest) = pytool.getFirstPareCont(commd, car(commd) ) 
    elif etp in ['IO RASSIGN','IO APPEND']:
       val, rest = None, cdr(cdr(commd))
    else:
       tmp = commd.split(' ', 1)   # tmp = [ C arg1 arg2 ..]
       val, rest = tmp[0].strip(), tmp[1:]
       rest = ''.join(rest)

    return (etp,val, rest.strip())

def commandParse(commd,std=stdPrint):
    commd = replaceAlias(commd)
    rest = commd.strip()
    lop, rop = [[]], [[]]
    exps = lop
    iotype = None
    while rest:
        etp, frt, rest = getEle(rest)
        if etp.startswith('IO'):
            if iotype is not None:
                prompt('invalid syntax: two IO operationes in command')
                raise SyntaxError
            iotype = etp
            exps = rop
        elif etp is 'PIPE':
            exps.append([])
        else:
            exps[-1].append((etp,frt))
    if iotype == None:
        val = pipeEval(lop)
        if std: std(val)
    elif iotype == 'IO RASSIGN': 
        var, val = eleVal(caar(rop)), pipeEval(lop)
        assign(var, val)
    elif iotype == 'IO LASSIGN':
        var, val = eleVal(caar(lop)), pipeEval(rop)
        assign(var, val)
    elif iotype == "IO APPEND":
        var, val = pipeEval(rop), pipeEval(lop)
        ioredirect(var,val, mode = 'a')
    elif iotype == "IO WRITE":
        var, val = pipeEval(rop), pipeEval(lop)
        ioredirect(var,val, mode = 'w')
    else:
        prompt('undefined syntax')

    return val
    
def eleType(ele):
    return ele[0]

def eleVal(ele):
    return ele[1]

def syntaxAssert():
    pass


# assign value to variable
def assign(var,val):
    assert(val is not None)
    if not isPreDefined(var):
        _assign(var,val)
    else:
        prompt('can not cover predefined functions')

def _assign(var,val):
    global _valtmp
    _valtmp = val
    exec(var + '=' + '_valtmp', globals())

def ioredirect(out,val,mode='w'):
    if type(val) == str: iotool.write(out,val,mode)
    try:
        iotool.dump(out,val,mode)
    except:
        iotool.write(out,str(val),mode)

# eval : pipe and func
def pipeEval(exps):
    if not exps: 
        prompt('empty expression')
    else:
        vals = map(funcEval, exps)
        return reduce(pipetransfer,vals)

def pipetransfer(arg,func):
    return func(arg)

# function compose
class _compFun(partial):
    def __mul__(self, y):
        f = lambda *args, **kwargs: self.func(y(*args, **kwargs))
        return _compFun(f)

def fcp():
    return _compFun(lambda arg: arg)

def funcEval(eles):
    vals = []
    comp = False
    for etype, expr in eles:
        if etype in ['LIST', 'DICT','VAR', 'STR']:
            val = eval(expr)
        elif etype is 'COMP':
            comp = True
            continue
        elif etype is 'BLOCK':
            val = evalPyExp(expr)
            if val is None:
                val = commandParse(expr[1:-1], std=None)
        elif etype is 'MAP':
            val = map

        if comp:
            comp = False
            if not isinstance(vals[-1], _compFun):
                vals[-1] = fcp() * vals[-1]
            vals[-1] = vals[-1] * val
        else:
            vals.append(val)

    return funcCall(vals)

def funcCall(vals):
    assert(len(vals) > 0)
    func, args = car(vals), cdr(vals)
    if not hasattr(func,'__call__'):
        assert(len(args) == 0)
        return func
    else:
        return tryFuncCall(func, *args)

def tryFuncCall(func, *args):
    try:
        print args,func
        val = func(*args)
    except Exception,e:
        val = partial(func,*args)
    return val
        
# eavl base expression 
def evalPyExp(commd):
    try:
        return eval(commd)
    except Exception:
        return None

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
    print type(commandParse(blee))
    commandShell()
    sh("test.txt")
    lines = commandParse( '"test.txt" | getFileLines ')
    for line in lines:
        print line.strip()
        commandParse(line)

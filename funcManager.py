from iotool import *
from oscmd import *
from pytool import *
from util import *
from pipe import *

def cmdHistory(file = 'history'):
    func = ['history','up','addToHistory','down','loadHis']
    his, cnt, length = [],0,0
    def loadHistory():
        his = getFileLines(file)
        length = len(his)
        cnt = length
    def history(n=None):
        if n is None: n = len(his)
        n = max(length - n, 0)
        return history[n:]
    def addToHistory(commd):
        if commd not in func:
            addLineToFile(file,commd)
            his.append(commd)
            length = len(his)
    def up(n=1):
        tmp = cnt - n
        if cnt < 0: return "failed: no more pre-history"
        cnt = tmp
        return history[cnt]
    def down(n=1):
        tmp = cnt + n
        if cnt >= length: return "failed: to end of history"
        cnt = tmp
        return history[cnt]
    loadHistory()
    return (loadHistory,history,addToHistory,up,down)

def preDefinedFunctions():
    funcs = globals()
    def isPreDefined(f):
        return funcs.has_key(f)
    def preDefined(f):
        if isPreDefined(f): return funcs[f]
        else: return None
    return (isPreDefined, preDefined)

# get the number of arguments of a function
def argnum(f):
    import inspect
    if hasattr(f,'__call__'):
        info = inspect.getargspec(f)
        args, defaults = 0,0
        if info.defaults: defaults = len(info.defaults)
        if info.args: args = len(info.args)
        return args - defaults
    else:
        return -1

def contextVars():
    vars = {}
    def hasVar(var):
        return  vars.has_key(var)
    def getVar(var):
        if hasVar(var): return vars[var]
        else: return None
    def addVar(var,val):
        vars[var] = val
    return (hasVar, getVar, addVar)

def getConfDict(file):
    lines = getLines(file)
    dct = {}
    for line in lines:
        comms = line.split('::',1)
        comms = [c.strip() for c in comms]
        dct[comms[0]] = comms[1]
    return dct

# alias manager interface
def alias():
    file = 'alias'
    aia = getConfDict(file)
    def getAlias(var):
        if var in aia:
            return aia[var]
        return None
    def addAlias(var,exp):
        if var in aia:
            prompt('the %s has used'%var)
        else:
            addLineToFile(conffile, '%s::%s'%(var,exp))
    def allAlias():
        return aia

    return (getAlias,addAlias,allAlias)

def configure():
    file = 'configure'
    conf = getConfDict(file)
    if conf.has_key('PATH'):
        cd(conf['PATH'])
        prompt('pwd: ' + conf['PATH'])

cd(os.path.dirname(__file__))

isPreDefined,preDefined = preDefinedFunctions()
hasVar, getVar, addVar = contextVars()
PREFIXS = {'!','~','%'}
getAlias, addAlias,allAlias = alias()
(loadHistory,history,addToHistory,up,down)  = cmdHistory()

# global tmp; used in assign
_valtmp = None

if __name__ == '__main__':
    pass

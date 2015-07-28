import re,sys,os,util,iotool

# get content of the first occurance of  parentheses
def getFirstPareCont(line, tp = '(' ):
    assert(tp in '([{"')
    dt = {'(':')', '[':']', '{':'}', '"':'"'}
    rtp = dt[tp]
    cnt = 1
    idx = line.find(tp)
    for i in xrange(idx+1, len(line)):
        if line[i] == rtp:
            cnt = cnt - 1
        elif line[i] == tp:
            cnt = cnt + 1
        if cnt == 0:
            break
    return (line[idx:i+1], line[i+1:])

def selectCol(k,lines,seq='\t'):
    eles = [line.split(seq) for line in lines]
    tps = zip(*eles)
    assert(len(tps) > k)
    return list(tps[k])
    
# get all the urls in a text
def getAllUrls(text):
    pattern = "\'http:.*?\'|\"http:.*?\""
    urls = util.findall(pattern,text)
    return urls

def difference(opl,opr):
    return list(set(opl).difference(set(opr))) 

def AmB(opl,opr):
    return list(set(opl).difference(set(opr))) 

def BmA(opl,opr):
    return list(set(opr).difference(set(opl))) 

def union(opl,opr):
    return list(set(opl).union(set(opr)))

def intersection(opl,opr):
    return list(set(opl).intersection(set(opr)))

def downloadPdf(url,out=None):
    pass

def words(text):
    return text.split()

def lines(text):
    return text.splitlines()

def downloadAllPdfs(url,out=None):
    pass

def downloadFilesByType(url,dtype):
    pass

def removeSpace(file,out):
    pass

def findWordInDir(word,sdir):
    pass

def switchProduce(pname,argv):
    pass

def crontab(commd):
    pass

if __name__ == '__main__':
    path = os.path.abspath(os.path.dirname(__file__))
    os.chdir(path)
    argv = sys.argv


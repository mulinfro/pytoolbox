#!/usr/bin/env python
""" 
use the functions in https://github.com/JulienPalard/Pipe
while not use it pipe solution
"""
from contextlib import closing
import socket
import itertools
from functools import reduce
import sys

try:
    import builtins
except ImportError:
    import __builtin__ as builtins

__all__ = [
     'take', 'tail', 'skip', 'all', 'any', 'average', 'count',
    'max', 'min', 'as_dict', 'permutations', 'netcat', 'netwrite',
    'traverse', 'concat', 'as_list', 'as_tuple', 'stdout', 'lineout',
    'tee', 'add', 'first', 'lrest','rrest','last','chain', 'select', 'where', 'take_while',
    'skip_while', 'aggregate', 'groupby', 'sort', 'reverse',
      'passed', 'index', 'strip', 'lstrip', 'rstrip', 'run_with', 
      't', 'to_type', 'uniq'
]

# add functions
# ------------------------------------
def uniq(iterable):
    return builtins.list(set(iterable))

"""
def list(iterable):
    return builtins.list(iterable)

def filter(func, iterable):
    return builtins.filter(func, iterable)

def str(v):
    return builtins.str(v)

def type(obj):
    return builtins.type(obj)
"""
# ------------------------------------


def take(qte, iterable):
    return iterable[0:qte]

def tail(qte, iterable):
    bidx = builtins.max(len(iterable) - qte,0)
    return iterable[bidx:]
        
def skip(qte, iterable ):
    "Skip qte elements in the given iterable, then yield others."
    for item in iterable:
        if qte == 0:
            yield item
        else:
            qte -= 1


def all(pred, iterable):
    "Returns True if ALL elements in the given iterable are true for the given pred function"
    return builtins.all(pred(x) for x in iterable)


def any(pred, iterable):
    "Returns True if ANY element in the given iterable is True for the given pred function"
    return builtins.any(pred(x) for x in iterable)


def average(iterable):
    """
    Build the average for the given iterable, starting with 0.0 as seed
    Will try a division by 0 if the iterable is empty...
    """
    total = 0.0
    qte = 0
    for x in iterable:
        total += x
        qte += 1
    return total / qte


def count(iterable):
    "Count the size of the given iterable, walking thrue it."
    count = 0
    for x in iterable:
        count += 1
    return count


def max(iterable, **kwargs):
    return builtins.max(iterable, **kwargs)


def min(iterable, **kwargs):
    return builtins.min(iterable, **kwargs)


def as_dict(iterable):
    return dict(iterable)


def permutations(iterable, r=None):
    # permutations('ABCD', 2) --> AB AC AD BA BC BD CA CB CD DA DB DC
    # permutations(range(3)) --> 012 021 102 120 201 210
    for x in itertools.permutations(iterable, r):
        yield x


def netcat(to_send, host, port):
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.connect((host, port))
        for data in to_send | traverse:
            s.send(data)
        while 1:
            data = s.recv(4096)
            if not data: break
            yield data


def netwrite(to_send, host, port):
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.connect((host, port))
        for data in to_send | traverse:
            s.send(data)


def traverse(args):
    for arg in args:
        try:
            if isinstance(arg, str):
                yield arg
            else:
                for i in arg | traverse:
                    yield i
        except TypeError:
            # not iterable --- output leaf
            yield arg


def concat(iterable, separator=", "):
    return separator.join(map(str,iterable))


def as_list(iterable):
    return list(iterable)


def as_tuple(iterable):
    return tuple(iterable)


def stdout(x):
    sys.stdout.write(str(x))


def lineout(x):
    sys.stdout.write(str(x) + "\n")


def tee(iterable):
    for item in iterable:
        sys.stdout.write(str(item) + "\n")
        yield item


def add(x):
    return sum(x)


def first(iterable):
    return next(iter(iterable))

def snd(iterable):
    return next(next(iter(iterable)))

def rrest(iterable):
    return iterable[1:]

def last(iterable):
    return iterable[-1]

def lrest(iterable):
    return iterable[0:-1]

def chain(iterable):
    return itertools.chain(*iterable)


def select(selector, iterable):
    return (selector(x) for x in iterable)


def where(predicate, iterable):
    return (x for x in iterable if (predicate(x)))


def take_while(predicate, iterable):
    return itertools.takewhile(predicate, iterable)


def skip_while(predicate, iterable):
    return itertools.dropwhile(predicate, iterable)


def aggregate(iterable, function, **kwargs):
    if 'initializer' in kwargs:
        return reduce(function, iterable, kwargs['initializer'])
    else:
        return reduce(function, iterable)

def groupby(keyfunc, iterable):
    return itertools.groupby(sorted(iterable, key = keyfunc), keyfunc)


def sort(iterable, **kwargs):
    return sorted(iterable, **kwargs)


def reverse(iterable):
    return reversed(iterable)


def passed(x):
    pass


def index(iterable, value, start=0, stop=None):
    return iterable.index(value, start, stop or len(iterable))


def strip(iterable, chars=None):
    return iterable.strip(chars)


def rstrip(iterable, chars=None):
    return iterable.rstrip(chars)


def lstrip(iterable, chars=None):
    return iterable.lstrip(chars)


def run_with(func, iterable):
    return  func(**iterable) if isinstance(iterable, dict) else \
            func( *iterable) if hasattr(iterable,'__iter__') else \
            func(  iterable)


def t(y, iterable):
    if hasattr(iterable,'__iter__') and not isinstance(iterable, str):
        return iterable + type(iterable)([y])
    else:
        return [iterable, y]


def to_type(x, t):
    return t(x)

#chain_with = Pipe(itertools.chain)
#islice = Pipe(itertools.islice)

# Python 2 & 3 compatibility
#if "izip" in dir(itertools):
#    izip = Pipe(itertools.izip)
#else:
#    izip = Pipe(zip)

if __name__ == "__main__":
    import doctest

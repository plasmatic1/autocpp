from collections import namedtuple

Lang = namedtuple('Lang', 'dmoj_langs file_ext moss_lang')

'''
MOSS supported languages list: 
@languages = ("c", "cc", "java", "ml", "pascal", "ada", "lisp", "scheme", "haskell", "fortran", "ascii", "vhdl", "perl", "matlab", "python", "mips", "prolog", "spice", "vb", "csharp", "modula2", "a8086", "javascript", "plsql", "verilog");

DMOJ languages list:
https://dmoj.ca/api/problem/info/helloworld

This just covers common languages used on DM::OJ
'''

__langs = (
    Lang(('C', 'C11'), 'c', 'c'),
    Lang(('CPP', 'CPP0X', 'CPP11', 'CPP14', 'CPP17'), 'cpp', 'cc'),
    Lang(('PY2', 'PY3', 'PYPY', 'PYPY3'), 'py', 'python'),
    Lang(('JAVA8', 'JAVA9', 'JAVA10', 'JAVA11'), 'java', 'java'),
    Lang(('HASK',), 'hs', 'haskell'),
    Lang(('PAS',), 'pas', 'pascal'),
    Lang(('V8JS',), 'js', 'javascript')
)

LANG_TO_EXT = {}
LANG_TO_MOSS = {}

for dmoj_langs, file_ext, moss_lang in __langs:
    for dmoj_lang in dmoj_langs:
        LANG_TO_EXT[dmoj_lang] = file_ext
        LANG_TO_MOSS[dmoj_lang] = moss_lang


def get_ext(dmoj_lang):
    return LANG_TO_EXT[dmoj_lang]


def get_moss_lang(dmoj_lang):
    return LANG_TO_MOSS[dmoj_lang]

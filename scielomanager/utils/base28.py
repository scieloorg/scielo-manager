#!/usr/bin/env python
# coding: utf-8

import string
from random import randrange

BASE36 = string.digits+string.ascii_lowercase
# sem vogais, para nao formar palavras em portugues
# sem 1l0, para evitar confusões na leitura
BASE28 = ''.join(d for d in BASE36 if d not in '1l0aeiou')

def reprbase(n, digitos=BASE28):
    ''' devolve a representação do valor `n` usando `digitos` '''
    base = len(digitos)
    s = []
    while n:
        n, d = divmod(n, base)
        s.insert(0, digitos[d])
    if s:
        return ''.join(s)
    else:
        return digitos[0]

def calcbase(s, digitos=BASE28):
    ''' devolve o valor numérico de `s` na base representada pelos dígitos '''
    return sum(digitos.index(dig)*len(digitos)**pot
               for pot, dig in enumerate(reversed(s)))

def genbase(tamanho, digitos=BASE28):
    return reprbase(randrange(len(digitos)**tamanho), digitos).rjust(tamanho,digitos[0])

if __name__=='__main__':
    print 'Amostra de alguns números em base 28'

    l = range(11)
    l.extend([calcbase(x) for x in ('3zz', '422','4zz','522','zzz','3222')])
    l.extend([27,28,29,28**2-1,28**2,1001,1100,1200,2000])

    for n in sorted(l):
        v = reprbase(n)
        assert n == calcbase(v)
        print '%8d\t%8s' % (n, reprbase(n))

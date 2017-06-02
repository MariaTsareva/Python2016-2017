# -*- coding: utf-8 -*-
"""
Created on Thu Jun  1 00:25:01 2017

@author: stsaryov
"""

import random
import re
from pymystem3 import Mystem
from pymorphy2 import MorphAnalyzer

def open_file():
    f  = open('C:\\TBot\War.txt', 'r', encoding = 'utf-8')
    string = f.read()
    f.close()
    return string
def from_str_to_list(string):
    m = Mystem()
    d = re.split("[, \-!?:;.()\\n]+", string)
    dd = ' '.join(d)
    lemmas = m.lemmatize(dd)
    d1 = set(lemmas)
    d2 = list(d1)
    return d2

def find_sent(str1):
    form = []
    str1 = str1.split()
    for s in str1:
        s1 = morph.parse(s)
        sf = s1[0]
#        print(sf.tag)
        
        form.append(sf.tag)
#    print(form)
    return form

def new_list(form, d2):
    words = []
    log_var = False
    for f in form:
        while True:
            
            l1 = random.choice(d2)
            l2 = morph.parse(l1)
            if (l2[0].tag.POS == f.POS) or (l2[0].tag.POS == 'INFN' and f.POS == 'VERB'):
                log_var = True
                if l2[0].tag.POS == 'VERB' or l2[0].tag.POS == 'INFN' or l2[0].tag.POS == 'GRND' :
                    log_var = (l2[0].tag.aspect == f.aspect and l2[0].tag.transitivity == f.transitivity)
                elif l2[0].tag.POS == 'NOUN':
                    log_var = (l2[0].tag.gender == f.gender and l2[0].tag.animacy == f.animacy \
                               and l2[0].tag.number == f.number)
                elif l2[0].tag.POS == 'ADJF':
                    log_var = (l2[0].tag.number == f.number and l2[0].tag.gender == f.gender)
                elif l2[0].tag.POS == 'PRTF':
                    log_var = (l2[0].tag.aspect == f.aspect and l2[0].tag.transitivity == f.transitivity and \
                               l2[0].tag.voice == f.voice)
                elif l2[0].tag.POS == 'NPRO':
                    log_var = (l2[0].tag.person == f.person and l2[0].tag.number == f.number)
                
                if log_var:
                    words.append(l1)
                    break
#    print(words)
    return words
def word_change(form, words):
    form1 = []
    xq = []
    new_sen = []
    for word in words:
        q = morph.parse(word)
        form1.append(q[0])
    for f in form:
        f = str(f)
#        print('f' , f[-4:])
        f = re.split('\W+', f)
        xq.append(f)
    for x, forr in zip(xq, form1):
        if forr.tag.POS == 'ADJF':
#            print('x= ', x)
            w = str(forr.inflect(set(x[-1:-2])))
        elif str(forr.tag) == x:
            w = str(forr)
        else:
            w = str(forr.inflect(set(x)))
        if 'Parse' in w:
           w = re.split('\W+', w)
           new_sen.append(w[2])
#    print(new_sen)
    hurray = ' '.join(new_sen)
    print(hurray)        
str1 = input("Введите предложение: ")
#str1 = 'Девочка поливала кактус'
morph = MorphAnalyzer()
m = Mystem()
new_file = open_file()
#print('1')
converce = from_str_to_list(new_file)
#print('2')
sent = find_sent(str1)
#print('3')
NEW_LIST = new_list(sent, converce)
#print('4')
WORDS = word_change(sent, NEW_LIST)
#print('5')

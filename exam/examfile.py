# -*- coding: utf-8 -*-
"""
Created on Mon Dec 19 13:47:35 2016

@author: MaryTsar
"""
#import  urllib.request
import re
import html
import os

not_parce = open('adyghe-unparsed-words.txt', 'r', encoding = 'utf-8')

r1 = open('output.txt', 'w', encoding = 'utf-8')


l_not_parced = []

for f1 in not_parce:
    l_not_parced.append(f1)



htmlparce= open('politsnip.html', 'r', encoding = 'utf-8')
f2 = htmlparce.read()
html11 = re.compile('<h1 class="page-title"><span>.*?<div class="infinitescroll">', flags=re.U | re.DOTALL)
findsm = html11.findall(f2)
l_for_html = []
for f in findsm:
    t1 = re.sub('<.*?>', "", f)
    clean_t1 = re.sub('\s{2,}',"", t1)
    l_for_html.append(clean_t1)
for l in l_for_html:
    r1.write(l)
fds = ''.join(l_for_html)
fds = fds.replace('I', 'l')

l_html = []
for i in range(len(fds)):
    l = fds.split(" ")
   
setpa = set(l_not_parced)
setht = set(l)
tr &= setpa & setht
tr1 = open('wordlist.txt', 'w', encoding = 'utf-8')
for t in tr:
    print(t)
    tr1.write(t)
tr1.close()



inp1 = "C:" + os.sep + "exam19" + os.sep
os.system(inp1 + "mystem.exe" +  " " + "-nd" + " " + inp1 + "adyghe-unparsed-words.txt" + " " + inp1 + "outpu.txt" )
file1 = open('outpu.txt', 'r', encoding = 'utf-8')
f = []
for f1 in file1:
    f.append(f1)
fds = ''.join(f)
rus = re.findall(r'{(.*)^[\?(?)]}', fds)
rus1 = open('rus_nouns.txt', 'w', encoding = 'utf-8')
for r in rus:
    rus1.write()
rus1.close()





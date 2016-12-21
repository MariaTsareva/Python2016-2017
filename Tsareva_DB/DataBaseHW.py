# -*- coding: utf-8 -*-
"""
Created on Wed Dec 21 20:19:17 2016

@author: tsaryov
"""

import re
import os

inp1 = "D:" + os.sep + "Maria" + os.sep
os.system(inp1 + "mystem.exe" +  " " + "-nd" + " " + inp1 + "mytext.txt" + " " + inp1 + "output.txt" )
file = open(inp1 + "mytext.txt", 'r', encoding = 'utf-8')
file1 = open(inp1 + "output.txt", 'r', encoding = 'utf-8')
file2 = open(inp1 + "incert1.txt", 'w', encoding = 'utf-8')
#file3 = open(inp1 + "incert2.txt", 'w', encoding = 'utf-8')

for l in file:
    l = l.split(' ')

f = []
for f1 in file1:
    f.append(f1)
lTokenDict = list(set(f))    
d = list(a for a in range(len(lTokenDict)))  
dTokenDict = dict(zip( lTokenDict, d))  
lToken_keys = []
for r in f:
    lToken_keys.append(dTokenDict.get(r)) 
fds = ''.join(lTokenDict)
fds = fds.lower()
lLemma1 = re.findall('{.*?}', fds)
lToken_info = []
for r in lLemma1:
    r11 = re.sub('[{|}]', '', r)
    lToken_info.append(r11)
lToken = []
for r in lTokenDict:
    r2 = re.sub('{.*?}', '', r)
    lToken.append(r2)
for i in range(0, len(lToken)):
    line1 = 'insert into Tokens (Token, Lemma) values (' + '"' +lToken[i] +'"' + ',' + '"' + lToken_info[i] + '"' + ');'
    file2.write(line1 + '\n' )         
    
file2 = open(inp1 + "incert1.txt", 'a', encoding = 'utf-8')    
lPunktLeft, lPunktRight =  [], []
sPunkt = None
for i in range (len(l)):
    lPunktLeft.append("")
    lPunktRight.append("")
    if sPunkt != None:
        lPunktLeft[i] = sPunkt.group(0)
        sPunkt = ""
    sPunkt = re.search('[.|,|:|;]', l[i])
    if sPunkt != None:
        l[i] = re.sub('[.|,|:|;]', '', l[i])
        lPunktRight[i] = sPunkt.group(0)
        
for i in range (len(l)):
    line = 'insert into Token_info (Token, Punk_right, Punk_left, Token_ID, Token_in_text_num) values (' + '"' + l[i] +'"' + ',' + '"' + lPunktRight[i] + '"' + ',' +  '"' + lPunktLeft[i] + '"' + ',' + str(lToken_keys[i]) + ',' + str(i) + ');'
    file2.write(line + '\n')

file2.close()
file1.close()
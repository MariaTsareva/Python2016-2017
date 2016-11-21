# -*- coding: utf-8 -*-
"""
Created on Mon Nov 21 11:01:34 2016

@author: Maria Tsareva
"""
import re
import json
thai = {}
file = open('thai_pages' + '/' + 'thai.txt', 'w', encoding = 'utf-8')
file1 = open('thai_pages' + '/' + 'thai1.txt', 'w', encoding = 'utf-8')
file3 = open('thai_pages' + '/' + 'data.json', 'w', encoding = 'utf-8')
file3 = open('thai_pages' + '/' + 'data.json', 'w', encoding = 'utf-8')
file4 = open('thai_pages' + '/' + 'data_inv.json', 'w', encoding = 'utf-8')

for i in range(187, 203):
    for j in range (1, 75):
        try:
            file = open('thai_pages' + '/' + 'thai.txt', 'a', encoding = 'utf-8')
            myfile = open('thai_pages' + '/' + str(i)+'.'+str(j)+'.'+'html', 'r', encoding = 'utf-8')
            data = myfile.read()
            regPostd = re.compile('<td class=th><a href=.*?>(.*?)</a></td>', flags=re.U | re.DOTALL)
            d = regPostd.findall(data)
            regPost = re.compile('<td class=pos>.*?</td><td>(.*?)</td>', flags=re.U | re.DOTALL)
            dw = regPost.findall(data)
            
            new_d = []
            regTag = re.compile('<.*?>', flags=re.U | re.DOTALL)
            regSpace = re.compile('\s{2,}', flags=re.U | re.DOTALL)
            for d1 in d:
                clean_d1 = regSpace.sub("", d1)
                clean_d1 = regTag.sub("", clean_d1)
            new_d.append(clean_d1)
            new_dw = []
            regTag = re.compile('<.*?>', flags=re.U | re.DOTALL)
            regSpace = re.compile('\s{2,}', flags=re.U | re.DOTALL)
            for d1 in dw:
                clean_d1 = regSpace.sub("", d1)
                clean_d1 = regTag.sub("", clean_d1)
            new_dw.append(clean_d1)
            thai = dict(zip(d, dw))
            for dt in new_dw:
                dt = dt.replace('&#34;', '')
                dt = dt.replace('&#39;', '')
                file.write(dt + '\n')
            for dt in new_d:
                dt = dt.replace('&#34;', '')
                dt = dt.replace('&#39;', '')
                file1.write(dt + '\n')
        except FileNotFoundError:
            print('Let us skip this ' + str(i)+'.'+str(j))
myfile = open('thai_pages' + '/' + 'thai.txt', 'r', encoding = 'utf-8')
myfile1 = open('thai_pages' + '/' + 'thai1.txt', 'r', encoding = 'utf-8')
a = myfile.readlines()
b = myfile1.readlines()
thai = dict(zip(b,a))
json.dump(thai, file3)

thai_inv = {thai[b] : b
            for b in thai}
json.dump(thai_inv, file4)
file.close()
file1.close()
file3.close()
file4.close()
myfile.close()
            
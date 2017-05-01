# -*- coding: utf-8 -*-
"""
Created on Thu Apr 27 19:40:09 2017

@author: stsaryov
"""
import urllib.request 
import requests
import json
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib import style
style.use('ggplot') 
from collections import Counter

def vk_post(offsets, k, myfile):
     idi = []
     lenth = []
     post = []
     for off in offsets:
         req = urllib.request.Request('https://api.vk.com/method/wall.get?domain=dota2&count=' + str(k) + '&offset=' + str(off))
         response = urllib.request.urlopen(req) # да, так тоже можно, не обязательно делать это с with, как в примере выше
         result = response.read().decode('utf-8')# импортируем модуль 
         data = json.loads(result)         
         for j in range(1,k+1):
             comments = data['response'][j]['comments']['count']
             if comments != 0 and comments > 100:
                 my_id = data["response"][j]['id']
                 post_text = data["response"][j]["text"]
                 post.append(post_text)
                 lenth.append(len(post_text.split()))
                 idi.append(my_id)
     print(idi)
     for p in post:
         myfile.write(p + '\n')
     return lenth, idi
 

    
def vk_comment(k, idi, myfile, offsets):
    com_len = []
    com_text = []
    users_id = []
    for i in idi:
        for off in offsets:
            req = urllib.request.Request('https://api.vk.com/method/wall.getComments?owner_id=-126093223&count=' + str(k) + '&post_id=' + str(i)  + '&offset=' + str(off))
            response = urllib.request.urlopen(req) 
            result = response.read().decode('utf-8')
            data = json.loads(result)
            j = 1
            while j < (k+1):
                bbb = data['response'][j]['text']
                d_id = data['response'][j]["from_id"]
    #                print('lll=',j)
    #                print('k=', k)
                com_text.append(bbb)
                com_len.append(len(bbb.split()))
                users_id.append(d_id)
                j += 1
    for c in com_text:
        myfile.write(c + '\n')
    return com_text, com_len, users_id

def user_city(users_id):
    cities = []    
    for uid in users_id:
        req = urllib.request.Request('https://api.vk.com/method/users.get?user_ids={}&fields=bdate,home_town'.format(str(uid)))
        response = urllib.request.urlopen(req) 
        result = response.read().decode('utf-8')
        data = json.loads(result)
        if 'home_town' not in (data['response'][0]):
            cities.append('Нет данных')
            continue
        cities.append(data['response'][0]['home_town'])        
#    print(cities)    
    return cities

def user_bday(users_id):
    
    bday = []
    for uid in users_id:
        req = urllib.request.Request('https://api.vk.com/method/users.get?user_ids={}&fields=bdate,home_town'.format(str(uid)))
        response = urllib.request.urlopen(req) 
        result = response.read().decode('utf-8')
        data = json.loads(result)        
        if 'bdate' not in (data['response'][0]):
            bday.append('Нет данных')
            continue
        bday.append(data['response'][0]['bdate'])    
#    print(bday)
    return bday

def count(com_len):
    asd = 0
    for s in range(len(com_len)):
        asd += com_len[s]
    asd1 = asd/len(com_len)
    asd1 = int(asd1)
    print(asd1)
    return asd1

def graph_post_com(post_len, asd1):
    plt.plot(range(len(post_len)),\
             [psl/asd1 for psl in post_len],'g',label='зеленая линия', linewidth=2)
    plt.title('отношение длины поста к длине комментов')
    plt.ylabel('ср. длина комментов')
    plt.xlabel('длина постов')

def bday_time(bday):
    lb_age = []    
    for bth in bday:    
        if len(bth) < 8 or bth == 'Нет данных':
            lb_age.append('Нет данных')        
        else:
            bth = bth.replace('.', '/', 2)
            if len(bth) == 8:
                bth = bth[:2] + '0' + bth[2:]
            b_date = datetime.strptime(bth, '%d/%m/%Y')
            b_age = int((datetime.today() - b_date).days/365)
#            print( "Age : %d" % ((datetime.today() - b_date).days/365))
            lb_age.append(b_age)
    return lb_age
            
def com_and_bday(com_len, lb_age):
    my_res = []
    for i, j in zip(lb_age, com_len):
        my_res.append( (i,j) )
    my_res = sorted(my_res, key=lambda x: str(x[0]))
    LY = []
    SY = []
    age = []
    my_res1 = []
    age_now = 0
    i = 0
    len_s = 0
    for M in my_res:    
        if my_res.index(M) == 0:
            age_now = M[0]
            age.append(M[0])
            i = 1
            len_s = M[1]
        elif M[0] == age_now:        
            if M == my_res[-1]:
                i += 1
                len_s += M[1]
                LY.append(len_s)
                SY.append(i)
            else:
                i += 1
                len_s += M[1]            
        elif age_now != M[0]:
            age.append(M[0])
            age_now = M[0]
            if  M == my_res[-1]:
                LY.append(len_s)
                SY.append(i)
                i += 1
                len_s += M[1]
            else:
                LY.append(len_s)
                SY.append(i)
                i = 0
                len_s = 0
                i += 1
                len_s += M[1]       
    res = []
    for l, s in zip(LY, SY):
        res.append(int(l/s))
    for i, j in zip(age, res):
        my_res1.append( (i,j) )
    return my_res1

def com_and_city(com_len, cities):
    my_res = []
    for i, j in zip(cities, com_len):
        my_res.append( (i,j) )
        my_res = sorted(my_res, key=lambda x: str(x[0]))
    LY = []
    SY = []
    city = []
    my_res1 = []
    ciry = ''
    i = 0
    len_s = 0
    for M in my_res:    
        if my_res.index(M) == 0:
            ciry = M[0]
            city.append(M[0])
            i = 1
            len_s = M[1]
        elif M[0] == ciry:        
            if M == my_res[-1]:
                i += 1
                len_s += M[1]
                LY.append(len_s)
                SY.append(i)
            else:
                i += 1
                len_s += M[1]            
        elif ciry != M[0]:
            city.append(M[0])
            ciry = M[0]
            if  M == my_res[-1]:
                LY.append(len_s)
                SY.append(i)
                i += 1
                len_s += M[1]
            else:
                LY.append(len_s)
                SY.append(i)
                i = 0
                len_s = 0
                i += 1
                len_s += M[1]       
    res = []
    for l, s in zip(LY, SY):
        res.append(int(l/s))                       
    for i, j in zip(city, res):
        my_res1.append( (i,j) )
    return my_res1

def bday_bar(my_res1):
    
    my_res1 = sorted(my_res1, key=lambda x: str(x[0]))
    plt.figure(figsize=(10,5))
    plt.bar(range(len(my_res1)), [i[1] for i in my_res1])
    plt.xticks(range(len(my_res1)), [i[0] for i in my_res1], rotation='vertical')
    plt.title('ср. длина комментов и возраст')
    plt.ylabel('ср. длина комментов')
    plt.xlabel('возраст')
    plt.show()     

def city_bar(my_res1):
    my_res1 = sorted(my_res1, key=lambda x: str(x[0]))
    plt.figure(figsize=(10,5))
    plt.bar(range(len(my_res1)), [i[1] for i in my_res1])
    plt.xticks(range(len(my_res1)), [i[0] for i in my_res1], rotation='vertical')
    plt.title('ср. длина комментов и город')
    plt.ylabel('ср. длина комментов')
    plt.xlabel('город')
    plt.show()

                   
offsets = [0,100,200]
offsets_com = [0, 50, 100]
myfile = open('myprog.txt', 'w', encoding = 'utf-8')
myfile1 = open('myprog1.txt', 'w', encoding = 'utf-8')
posts, lst = vk_post(offsets, 5, myfile)
com_lst_text, com_lst_len, com_us_id= vk_comment(5, lst, myfile1, offsets_com)
count1 = count(com_lst_len)
graph1 = graph_post_com(com_lst_len, count1)
cities_user = user_city(com_us_id)
bdates_user = user_bday(com_us_id)
day_time = bday_time(bdates_user)
bday_com = com_and_bday(com_lst_len, day_time)
city_com = com_and_city(com_lst_len, cities_user)
bday_graph = bday_bar(bday_com)
city_bar1 = city_bar(city_com)
myfile.close()
myfile1.close()
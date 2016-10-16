# -*- coding: utf-8 -*-
"""
Created on Thu Oct  6 13:38:23 2016

@author: Maria Tsareva
"""
import os
import urllib.request
import re
from subprocess import Popen, PIPE
import pandas
import html

def csv_pandas(lPath, d, author, Title, Topic, lPageUrl):
    raw_data = {'path': lPath,
                'author': author,
                'sex': '',
                'birthday': '',
                'header': Title,
                'created': d,
                'sphere': "публицистика", 'genre_fi':'', 'type': '', 
                'topic': Topic,           'chronotop': '', 'style': 'neutral',
                'audience_age': 'n-age',  'audience_level': 'n-level', 
                'audience_size': 'republic', 'source': lPageUrl,
                'publication': 'Мордовия',   'publisher': '',
                'medium': 'газета',          'country': 'Россия', 
                'region': 'Мордовия Республика',
                'language': 'ru'}
    df = pandas.DataFrame(raw_data, columns = ['path', 'author', 'sex', 'birthday', 'header', 'created', 'sphere', 'genre_fi'\
        'type', 'topic', 'chronotop', 'style', 'audience_age','audience_level','audience_size','source'\
        'publication','publisher', 'medium', 'country', 'region', 'language' ])
    df.to_csv('C://Users/Maria Tsareva/Downloads/Zeitung/mycsv.csv', sep='\t', encoding='utf-8')

def find_text(data, myfile):
     html11 = re.compile('<dd class="text">(.*?)<dd class="detail">', flags=re.U | re.DOTALL)
     text = html11.findall(data)
     new_text = []
     regTag = re.compile('<.*?>', flags=re.U | re.DOTALL)
     regSpace = re.compile('\s{2,}', flags=re.U | re.DOTALL)
     for t1 in text:
         clean_t1 = regSpace.sub("", t1)
         clean_t1 = regTag.sub("", clean_t1)
         new_text.append(clean_t1)
     for t1 in new_text:
         t1 = html.unescape(t1)
         #t1 = t1.replace("&nbsp;&rarr;&amp;&laquo;&amp;&raquo;&ndash;", " ")
         myfile.write(t1)


def find_author(data, myfile):
    regPostau = re.compile('(<p style="text-align: right;"><strong>(.*?)</strong></p></dd>|<div style="text-align: right;"><strong>(.*?)</strong></div></dd>)', flags=re.U | re.DOTALL)
    au = regPostau.findall(data)
    if au == []:
        au = ['Noname']
#        myfile.write('@au Noname')
    
    for a in au:
        myfile.write('@au' + ' ' + a[1] + chr(13))
    return a[1]      

def find_title(data, myfile):
    regPosttitle = re.compile('<dd class="title">(.*?)</dd>', flags=re.U | re.DOTALL)
    title = regPosttitle.findall(data)
    if title == []:
        title = ['no title']
    
    for t in title:
        myfile.write('@ti' + ' ' + t + chr(13))
    return t
            
def find_topic(data, myfile):
    regPosttopic = re.compile('<dd class="cont_title"><span class="title_text">.*?<a href="news-.?.htm">(.*?)</a>', flags=re.U | re.DOTALL)
    topic = regPosttopic.findall(data)
    if topic == []:
        topic = ['no topic']
    
    for tp in topic:
        myfile.write('@topic' + ' ' + tp + chr(13))
    return tp        
               
def find_date(data):
    
    regPostd = re.compile('<span class="title_data">.*?(\d{2}.\d{2}.\d{4})</span></dd>', flags=re.U | re.DOTALL)
    d = regPostd.findall(data)
    if d == []:
        d = ['01.01.1000']
    return d
                
def find_url(pageUrl, myfile):
    page1 = '@url' + ' ' + pageUrl  + chr(13)
    myfile.write(page1)
#    return page1
    
def create_path(s, d):
    if d == []:
        fullpath = os.path.join('Zeitung', s, 'deletedpages' )
    else:
        for d1 in d:
            d1 = d1.split('.')
        fullpath = os.path.join('Zeitung', s, d1[2], d1[1] )
    if not os.path.exists(fullpath):
        os.makedirs(fullpath)
    return fullpath

       

commonUrl = 'http://mordovia-news.ru/news-1-'
wkdir = r'"C:/Users/Maria Tsareva/Downloads/"'
s = 'plain'
s1 = 'mystem-xml'
s2 = 'mystem-plain'

lPageUrl, lPath, lDate, lAuthor, lTitle, lTopic = [], [], [], [], [], []
for i in range(1374, 4001):
    pageUrl = commonUrl + str(i) + '.htm'
    with urllib.request.urlopen(pageUrl) as f: #only 1 loop
        try:
            data = f.read().decode('windows-1251')
            d = find_date(data)
            awe = create_path(s, d)
            lPath.append(awe)
            awe1 = create_path(s1, d)
            awe2 = create_path(s2, d)
            myfile = open(awe + os.sep + str(i)+".txt", "w", encoding = 'utf-8')
            
            author = find_author(data, myfile)
            lAuthor.append(author)
            Title = find_title(data, myfile)
            lTitle.append(Title)
            for dt in d:
                myfile.write('@da' + ' ' + dt + chr(13))
            lDate.append(dt)
            Topic = find_topic(data, myfile)
            lTopic.append(Topic)
            Url = find_url(pageUrl, myfile)
            find_text(data, myfile)
            lPageUrl.append(pageUrl)
        
            myfile.close()
            
            pth = wkdir + r'mystem.exe -cnid --format xml --eng-gr ' + \
                wkdir + awe + os.sep + str(i) + \
                ".txt" + " " + wkdir + awe1 + os.sep + str(i) + '.xml'
            
            pth1 = wkdir + r'mystem.exe -cnid --format xml --eng-gr ' + \
                wkdir + awe + os.sep + str(i) + \
                ".txt" + " " + wkdir + awe2 + os.sep + str(i) + '.txt'
            
            p = Popen(pth , shell=True, stdout=PIPE, stderr=PIPE)
            out, err = p.communicate()
            p1 = Popen(pth1 , shell=True, stdout=PIPE, stderr=PIPE)
            out, err = p.communicate()
            print ("Return code: ", p.returncode)
            print (out.rstrip(), err.rstrip())
        except UnicodeDecodeError:
            print('broken reference to article №'+str(i))
csv_pandas(lPath, lDate, lAuthor, lTitle, lTopic, lPageUrl)


 


    
        
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 16 21:25:49 2016

@author: tsaryov
"""
import pandas as pd
import json
from flask import Flask
from flask import url_for, render_template, request, redirect

app = Flask(__name__)

file = open('bigdata.txt', 'w', encoding = 'utf-8')
file = open('data.json', 'w', encoding = 'utf-8')
file.close()

def replace_last(source_string, replace_what, replace_with):
    head, sep, tail = source_string.rpartition(replace_what)
    return head + replace_with + tail
      
@app.route('/')
def index():
    urls = {'главная страница': url_for('index'), 'json': url_for('json_result'),
            'статистика':('stats')}
    if request.args:
        name = request.args['name']
        ausbildung = request.args['ausbildung']
        checked = request.args['sex']
        age = request.args['age']
        idiom = request.args['idiom']
        city = request.args['city']
        oreo = request.args['cookie']

        file = open('checked.txt', 'w', encoding = 'utf-8')
        for index in request.args.keys():
            if index != 'Отправить':
                s = request.args[index] + ','
#                if s.endswith(','):
        #s = replace_last(s, ',', '\n')
                file.write(s)
        file.close()
        
        file = open('data.json', 'a', encoding = 'utf-8')
        json.dump(request.args, file)
        file.close()
        file = open('checked.txt', 'r', encoding = 'utf-8')
        f = file.read()
        f = f[:-1]
        f = f + '\n'
        file1 = open('bigdata.txt', 'a', encoding = 'utf-8')
        file1.write(f)
        file1.close()
        return render_template('thanks.html', name=name, ausbildung=ausbildung, sex=checked, age=age, idiom=idiom, city=city, cookie=oreo)
    else:
        return render_template('index.html', urls=urls)
        
@app.route('/json_result')
def json_result():
    file = open('data.json', 'r', encoding = 'utf-8')
    name = file.read()
    return render_template('json_result.html', txt=name)



@app.route('/stats')
def stats():
    #file = open('bigdata.txt', 'r', encoding = 'utf-8')
    df = pd.read_csv('bigdata.txt', sep=',', header = None) 
    df.columns=[ 'ausbildung', 'name', 'age', 'idiom', 'word', 'city','sex']  
    counts = df.groupby('word').size(); 
    return render_template('stats.html', counts=counts)

    
    
    
if __name__ == '__main__':
    app.run(debug=True)
file.close()

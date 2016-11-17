# -*- coding: utf-8 -*-
"""
Created on Wed Nov  9 22:20:33 2016

@author: Maria Tsareva
"""

from flask import Flask
from flask import url_for, render_template, request, redirect

app = Flask(__name__)

#@app.route('/')
#def index():
#    urls = {'главная страница': url_for('index'),
#            'Спасибо!': url_for('thanks')}
#    #checked = request.form['sex']
#    return render_template('index.html', urls=urls )
file = open('checked.txt', 'w', encoding = 'utf-8')
      
@app.route('/')
def index():
    
    urls = {'главная страница': url_for('index'),}
    
    if request.args:
        name = request.args['name']
        ausbildung = request.args['ausbildung']
        checked = request.args['sex']
        age = request.args['age']
        idiom = request.args['idiom']
        city = request.args['city']
        oreo = request.args['cookie']
        with open('checked.txt', 'a') as file1:
            file1.write("Пользователь:" + name)
            file1.write(ausbildung)
            file1.write("{}".format(checked))
            file1.write(age)
            file1.write(idiom)
            file1.write(city)
            file1.write("{}".format(oreo))
            file1.close()
            return render_template('answer.html', name=name, ausbildung=ausbildung, sex=checked, age=age, idiom=idiom, city=city, cookie=oreo)

    return render_template('index.html', urls=urls)


    
if __name__ == '__main__':
    app.run(debug=True)
file.close()
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 10 23:36:28 2017

@author: tsaryov
"""
import telebot
import conf
import re
import phrases
import random
from random import uniform
from collections import defaultdict

WEBHOOK_URL_BASE = "https://{}:{}".format(conf.WEBHOOK_HOST, conf.WEBHOOK_PORT)
WEBHOOK_URL_PATH = "/{}/".format(conf.TOKEN)

bot = telebot.TeleBot(conf.TOKEN, threaded=False)
r_alphabet = re.compile(u'[а-яА-Я0-9-]+|[.,:;?!]+')
str1 = input("Введите предложение: ")
regEng = re.compile('[a-zA-z]+')
bot.remove_webhook()
bot.set_webhook(url=WEBHOOK_URL_BASE+WEBHOOK_URL_PATH)
app = flask.Flask(__name__)
@app.route('/', methods=['GET', 'HEAD'])
def index():
    return 'ok'


# обрабатываем вызовы вебхука = функция, которая запускается, когда к нам постучался телеграм 
@app.route(WEBHOOK_URL_PATH, methods=['POST'])
def webhook():
    if flask.request.headers.get('content-type') == 'application/json':
        json_string = flask.request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''
    else:
        flask.abort(403)
#def get_word(str1):
#    words = re.compile('\w+').findall(str1)
##    word = random.choice(words)
#    return words
    
def gen_lines(corpus):
    data = open(corpus, encoding = 'utf-8')
    for line in data:
        yield line.lower()

def gen_tokens(lines):
    for line in lines:
        for token in r_alphabet.findall(line):
            yield token

def gen_trigrams(tokens):
    t0, t1 = '$', '$'
    for t2 in tokens:
#        print('t2', t2)
        yield t0, t1, t2
        if t2 in '.!?':
            yield t1, t2, '$'
            yield t2, '$','$'
            t0, t1 = '$', '$'
        else:
            t0, t1 = t1, t2
#def gen_trigrams(tokens, words):
#    t0, t1 = '$', '$'
#    for t2 in words:
##        print('t2', t2)
#    
#        yield t0, t1, t2
#        if t2 in '.!?':
#            yield t1, t2, '$'
#            yield t2, '$','$'
#            t0, t1 = '$', '$'
#        else:
#            t0, t1 = t1, t2
            
def train(corpus):
#    Words = get_word(str1)
    lines = gen_lines(corpus)
    tokens = gen_tokens(lines)
    trigrams = gen_trigrams(tokens)

    bi, tri = defaultdict(lambda: 0.0), defaultdict(lambda: 0.0)

    for t0, t1, t2 in trigrams:
        bi[t0, t1] += 1
        tri[t0, t1, t2] += 1

    model = {}
    for (t0, t1, t2), freq in tri.items():
        if (t0, t1) in model:
            model[t0, t1].append((t2, freq/bi[t0, t1]))
        else:
            model[t0, t1] = [(t2, freq/bi[t0, t1])]
    return model

def generate_sentence(model):
    phrase = ''
    t0, t1 = '$', '$'
    while 1:
        t0, t1 = t1, unirand(model[t0, t1])
        if t1 == '$': break
        if t1 in ('.!?,;:') or t0 == '$':
            phrase += t1
        else:
            phrase += ' ' + t1
    return phrase.capitalize()

def unirand(seq):
    sum_, freq_ = 0, 0
    for item, freq in seq:
        sum_ += freq
    rnd = uniform(0, sum_)
    for token, freq in seq:
        freq_ += freq
        if rnd < freq_:
            return token

if __name__ == '__main__':
    model = train('Harry_Potter.txt')
    #model = train('https://github.com/MariaTsareva/Python2016-2017/blob/master/ProBot/Harry_Potter.txt')
    
#    for i in range(10):
    print ('Ответ', generate_sentence(model))
        
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, phrases.start)

@bot.message_handler(commands=['help'])
def help_command(message):  
    bot.send_message(message.chat.id, phrases.help)
    
@bot.message_handler(content_types=["text"])
def get_phrase(message): 
    if regEng.search(message.text) is not None:
        bot.send_message(message.chat.id, random.choice(phrases.english))
    else:
        bot.send_message(message.chat.id, generate_sentence(model))

# -*- coding: utf-8 -*-
"""
Created on Tue Apr 25 21:00:22 2017

@author: stsaryov
"""
import flask
import telebot
import conf
bot = telebot.TeleBot(conf.TOKEN)

WEBHOOK_URL_BASE = "https://{}:{}".format(conf.WEBHOOK_HOST, conf.WEBHOOK_PORT)
WEBHOOK_URL_PATH = "/{}/".format(conf.TOKEN)

bot = telebot.TeleBot(conf.TOKEN, threaded=False)  # бесплатный аккаунт pythonanywhere запрещает работу с несколькими тредами

# удаляем предыдущие вебхуки, если они были
bot.remove_webhook()

# ставим новый вебхук = Слышь, если кто мне напишет, стукни сюда — url
bot.set_webhook(url=WEBHOOK_URL_BASE+WEBHOOK_URL_PATH)

app = flask.Flask(__name__)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.send_message(message.chat.id, "Здравствуйте! Это бот, который считает количество гласных букв в сообщении.")
    
@bot.message_handler(func=lambda m: True)  # этот обработчик реагирует на любое сообщение
def send_len(message):
   vowels1 = set("ёуеыаоэяию")
   vowels2 = set('eyuioa')
   vowels = set.union(vowels1, vowels2)
   #word_set = set(message.text)
   bot.send_message(message.chat.id, 'В вашем сообщении {} гласных.'.format(sum(letter in vowels for letter in message.text)))

# пустая главная страничка для проверки
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
#@bot.message_handler(...) # здесь описываем, на какие сообщения реагирует функция
#def my_function(message):
#    reply = '' 
#    # здесь код, который генерирует ответ
#	bot.send_message(message.chat.id, reply)  # отправляем в чат наш ответ
if __name__ == '__main__':
    bot.polling(none_stop=True)
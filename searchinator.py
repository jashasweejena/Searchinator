from bs4 import BeautifulSoup
from telegram.ext import Updater, CommandHandler
import requests
import json
import sys
import re
# import telegram

# que = sys.argv[1]

# bot = telegram.bot(token=api_key)

import os
dir_path = os.path.dirname(os.path.realpath(__file__))
print(dir_path)

def getFileContent(pathAndFileName):
    with open(pathAndFileName, 'r') as theFile:
        # Return a list of lines (strings)
        # data = theFile.read().split('\n')

        # Return as string without line breaks
        # data = theFile.read().replace('\n', '')

        # Return as string
        data = theFile.read()
        return data

# api_key = getFileContent({}/'telegram_api_key.txt'.format(dir_path))


updater = Updater(token='', use_context=True)
dispatcher = updater.dispatcher

def getdata(que):
    url="https://eztv.io/search/" + que.replace(" ", "-")
    print(url)
    page=requests.get(url)
    d = dict()
    soup=BeautifulSoup(page.text,'html.parser')

    links=[]
    titles=[]

    namel=soup.select("a[class='magnet']")
    for link in namel:
        links.append(link.get('href'))
        titles.append(link.get('title'))
    d['titles']=titles
    d['links']=links

    json_string = json.dumps(d)
    return d



def start(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, text="I'm a bot, please talk to me!")

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

def fetch(update, context):
    text_fetch = ' '.join(context.args)
    d = getdata(text_fetch)
    context.bot.send_message(chat_id=update.message.chat_id, text=d['titles'][0])
    context.bot.send_message(chat_id=update.message.chat_id, text=d['links'][0])
    print(d['links'][0])


caps_handler = CommandHandler('fetch', fetch)
dispatcher.add_handler(caps_handler)

def forward(update, context):
    message = update.message['reply_to_message']['text']
    print(message)
    user_says = " ".join(context.args)
    update.message.reply_text("You said: " + user_says)

dispatcher.add_handler(CommandHandler("forward", forward, pass_args=True))

updater.start_polling()

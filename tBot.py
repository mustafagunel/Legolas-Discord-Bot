from asyncio.windows_events import NULL
import telebot
import os
import xml.etree.ElementTree as ET
import sqlite3

#with sqlite3.connect("YOUR_DB") as con:
#    cur = con.cursor()
#cur.execute('CREATE TABLE "tbl_users" (	"id"	INTEGER,	"name"	TEXT,	"status"	TEXT,	"date"	TEXT,	PRIMARY KEY("id" AUTOINCREMENT))')
#con.close()

API_KEY = 'YOUR_API'
bot = telebot.TeleBot(API_KEY, parse_mode=None) # You can set parse_mode by default. HTML or MARKDOWN


configTree = ET.parse('config.xml')             # Read Config
configRoot = configTree.getroot()

@bot.message_handler(commands=['start', 'help'])
def Options(message):
	bot.reply_to(message, "/name [isim] : Eşleşen isimlerin kayıtlarını getirir.\n/name [isim] [date]: Eşleşen isimlerin tarih aralığındaki kayıtlarını getirir. YIL-AY-GÜN: 2022-11-03\n/logs : Son 5 değişen kullanıcı durumunu getirir.")

@bot.message_handler(commands=['zort'])
def Zort(message):
	bot.reply_to(message, "Boş Yapma KARDEŞ")


@bot.message_handler(commands=['logs'])
def Logs(message):

    with sqlite3.connect("YOUR_DB") as con:
        data = list(con.execute('SELECT name as "DCAdi", status  as "Durum",date as "Tarih"  from tbl_users ORDER by id desc LIMIT 5'))
    con.close()
    bot.reply_to(message, str(data))

    '''
    for x in configRoot.findall('log'):
        fileName =x.find('fileName').text
    logFile = open(fileName+".log", "rb")

    Lines = logFile.readlines()
    count = 0
    for line in Lines:
        count += 1
        bot.reply_to(message, line.strip())
        if count == 5:
            break   
    '''     
@bot.message_handler(commands=['logFile'])
def LogFile(message):
    '''
    for x in configRoot.findall('log'):
        fileName =x.find('fileName').text
    logFile = open(fileName+".log", "rb")

    bot.send_document(message.chat.id, logFile)
    '''


def extract_arg(arg):
    return arg.split()[1:]

@bot.message_handler(commands=['name'])
def GetByName(message):
    arg = extract_arg(message.text)
    #print(arg[0])
    #print(arg[1])
    argc = len(arg)
    if(argc == 2):
        isim = str(arg[0])
        date = str(arg[1])
        sorgu = 'SELECT name as "DCAdi", status  as "Durum",date as "Tarih"  from tbl_users where date >= "'+date+'" and name like "%'+isim+'%" ORDER by date desc LIMIT 50'
    elif(argc == 1):
        isim = str(arg[0])
        sorgu = 'SELECT name as "DCAdi", status  as "Durum",date as "Tarih"  from tbl_users where name like "%'+isim+'%" ORDER by date desc LIMIT 50'
    else:
        bot.reply_to(message, "En az 1 parametre girmelisin")
    print(sorgu)
    with sqlite3.connect("YOUR_DB") as con:
        data = list(con.execute(sorgu))
        sorgu =""
    con.close()
    print(str(data))
    bot.reply_to(message, str(data))




bot.polling()

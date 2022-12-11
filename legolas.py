from email import message
from fileinput import filename
import discord
import datetime
import os
import xml.etree.ElementTree as ET
import sqlite3

TOKEN = 'YOUR_TOKEN'

'''
configTree = ET.parse('config.xml')             # Read Config
configRoot = configTree.getroot()
for x in configRoot.findall('log'):             # Get config filename and max config file size
    fileName =x.find('fileName').text
    maxFileSize = x.find('maxFileSize').text
    print(fileName+" "+maxFileSize)
'''

con = sqlite3.connect("YOUR_DB")
cur = con.cursor()
#cur.execute('CREATE TABLE "tbl_users" (	"id"	INTEGER,	"name"	TEXT,	"status"	TEXT,	"date"	TEXT,	PRIMARY KEY("id" AUTOINCREMENT))')


class MyClient(discord.Client):
    
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    # new message
    async def on_message(self, message):
        print(f'Message from {message.author}: {message.content} | channel({message.channel})')
    
    # voice chat updates
    async def on_voice_state_update(self, member, before, after):

        dt = datetime.datetime.now()
        try:
            data = [
                (str(member.name),str(member.voice.self_mute),str(member.voice.self_deaf),str(member.voice.self_stream),str(member.voice.channel),str(dt),"ONLINE")
            ]
            cur.executemany("INSERT INTO tbl_voice_chat_log (user, self_mute, self_deaf, self_stream, channel_name, date, isOnlineOnVoiceChat) VALUES (?,?,?,?,?,?,?)", data)
            con.commit()
            print(f'{data}')
        except:
            data = [
                (str(member.name),"NONE","NONE","NONE","NO-CHANNEL",str(dt),"OFFLINE")
            ]
            cur.executemany("INSERT INTO tbl_voice_chat_log (user, self_mute, self_deaf, self_stream, channel_name, date, isOnlineOnVoiceChat) VALUES (?,?,?,?,?,?,?)", data)
            con.commit()

            print(f"{member.name} Left Voice Channels")
        
        
        
    # user status update
    async def on_presence_update(self,before, after):
        dt = datetime.datetime.now()
        print(f'[+] {after.display_name} {after.status}  {dt }' )
        data = [
            (str(after.display_name), str(after.status), str(dt))
        ]
        cur.executemany("INSERT INTO tbl_users (name, status, date) VALUES (?,?,?)", data)
        con.commit()

        '''
        logFile = open(fileName+".log", "a")
        fileSize = os.path.getsize(fileName+".log")
        if fileSize > int(maxFileSize):                                             # create new log file if size larger then 50MB
            newName = str(datetime.datetime.timestamp(dt))
            logFile = open(newName+".log", "a")
            for x in configRoot.findall('log'):
                x.find('fileName').text = str(newName)
                x.set('updated', 'yes') 
                configTree.write('config.xml')

        logFile.write(f'[+] {after.display_name} {after.status}  {dt }\n')  # log status   
        logFile.close()             
        '''
        '''
        if after.status is discord.Status.dnd:
            print(f'[NewStatus] {after.display_name} dont disturb  {datetime.datetime.now()}' )
        elif after.status is discord.Status.online:
            print(f'[NewStatus] {after.display_name} online  {datetime.datetime.now()}')
        elif after.status is discord.Status.idle:
            print(f'[NewStatus] {after.display_name} idle  {datetime.datetime.now()}')
        elif after.status is discord.Status.do_not_disturb:
            print(f'[NewStatus] {after.display_name} do_not_disturb  {datetime.datetime.now()}' )
        elif after.status is discord.Status.invisible:
            print(f'[NewStatus] {after.display_name} invisible  {datetime.datetime.now()}' )
        else:
            print(f'[NewStatus] {after.display_name} OFFLINE  {datetime.datetime.now()}')
        '''

intents = discord.Intents.all()     # Permissions

client = MyClient(intents=intents)
client.run(TOKEN)

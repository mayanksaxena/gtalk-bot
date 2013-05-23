import sys
import xmpp
import time,os
import json
from utility import *
from commands import *

onlineUsers = []

db = MySQLdb.connect(host="localhost", user="root", passwd="", db="gtalkbot") 

cur = db.cursor() 

def messageCB(conn,mess):

    nick=mess.getFrom().getResource()
    text=mess.getBody()
    LOG(mess,nick,text)
    if text != None:
        text=mess.getBody()
        user=mess.getFrom()
        user.lang='en'      # dup
        if text.find(' ')+1: command,args=text.split(' ',1)
        else: command,args=text,''
        cmd=command.lower()
        if commands.has_key(cmd): reply=commands[cmd](user,command,args,mess)
        else: reply=("UNKNOWN COMMAND",cmd)

        if type(reply)==type(()):
            key,args=reply
            if my_commands.has_key(key): pat=my_commands[key]
            elif my_commands.has_key(key): pat=my_commands[key]
            else: pat="%s"
            if type(pat)==type(''): reply=pat%args
            else: reply=pat(**args)
        else:
            try: reply=my_commands[reply]
            except KeyError:
                try: reply=my_commands[reply]
                except KeyError: pass
        if reply: conn.send(xmpp.Message(mess.getFrom(),reply))

############################# bot logic stop #####################################

def StepOn(conn):
    try:
        conn.Process(1)
    except KeyboardInterrupt: return 0
    return 1

def GoOn(conn):
    while StepOn(conn): pass

def start_bot():
    if len(sys.argv)<3:
        print "Usage: start_bot.py username@server.net password"
    else:
        jid=xmpp.JID(sys.argv[1])
        user,server,password=jid.getNode(),jid.getDomain(),sys.argv[2]

        conn=xmpp.Client(server)#,debug=[])
        conres=conn.connect()
        if not conres:
            print "Unable to connect to server %s!"%server
            sys.exit(1)
        if conres<>'tls':
            print "Warning: unable to estabilish secure connection - TLS failed!"
        authres=conn.auth(user,password)
        if not authres:
            print "Unable to authorize on %s - check login/password."%server
            sys.exit(1)
        if authres<>'sasl':
            print "Warning: unable to perform SASL auth os %s. Old authentication method used!"%server
        conn.RegisterHandler('message',messageCB)
        conn.RegisterHandler('presence', presenceCB)
        conn.sendInitPresence()
        ##conn.send(xmpp.protocol.Message('sanjay.verma@anktech.co.in','This is a automatic message'))

        print "Bot started."
        GoOn(conn)

start_bot()


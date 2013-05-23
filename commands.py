import urllib
import time
import datetime
from datetime import datetime
from xgoogle.search import GoogleSearch, SearchError
from argparse import ArgumentParser
from xml.dom import minidom
import random
import MySQLdb
import time,os
import string
import json
try:
    from urllib.request import urlopen
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlopen, urlencode
from assembla import *

########################### user handlers start ##################################
commands = {}
my_commands = {}

my_commands['HELP']="Available commands: %s"
def helpHandler(user,command,args,mess):
    lst=commands.keys()
    lst.remove("sendslave")
    lst.sort()
    return "HELP",', '.join(lst)

my_commands['EMPTY']="%s"

my_commands['hi']='Responce 1: %s'
def hiHandler(user,command,args,mess):
    return "Hello Master, How can i help you."

my_commands['hello']='Responce 1: %s'
def helloHandler(user,command,args,mess):
    return "Hello Master, How can i help you."

my_commands['sendslave']='Responce 1: %s'
def sendslaveHandler(user,command,args,mess):
    try:
        params = args.split(" ")
        if len(params) < 2: 
            return "Please Provide two parameters"
        else:
            user = params[0]
            messages = ""
            for text in params:
                if text == user:
                    pass
                else:
                    messages += " " + text
            conn.send(xmpp.protocol.Message(user,messages))
            return "Message successfully sent"
    except:
        return "Some Error Occured"

my_commands['livecricket']='Responce 1: %s'
def livecricketHandler(user,command,args,mess):    
    API_URL = "http://livechat.rediff.com/sports/score/score.txt"
    xml = urlopen(API_URL).read()
    
    return xml


my_commands['mayank']='Responce 1: %s'
def mayankHandler(user,command,args,mess):
    return "He is my father :)"

my_commands['search']='Responce 1: %s'
def searchHandler(user,command,args,mess):
    try:
      if len(args)<2:
        return "Please Provide your search Query"
      else:
          gs = GoogleSearch(args)
          gs.results_per_page = 10
          gs.page = 1
          results = gs.get_results()
          if len(results) > 0:
              for res in results:
                return res.title.encode("utf8") + "\n" + res.desc.encode("utf8") + "\n" + res.url.encode("utf8")
          else:
            return "No Search Result Found for your query."
    except SearchError, e:
      return "Search failed: %s" % e

my_commands['time']='Responce 1: %s'
def timeHandler(user,command,args,mess):
    return datetime.now()

my_commands['cricket']='Responce 1: %s'
def cricketHandler(user,command,args,mess):    
    try:
        API_URL = "http://static.cricinfo.com/rss/livescores.xml"
        xml = urlopen(API_URL).read()
        doc = minidom.parseString(xml)
        iternews = iter(doc.documentElement.getElementsByTagName("item"))
        newsText = ""
        for news in iternews:
            newsText += news.getElementsByTagName("title")[0].firstChild.nodeValue + "\n"
            newsText += "##############################################\n"

        return newsText
    except:
        return "Sorry some error occured"

my_commands['news']='Responce 1: %s'
def newsHandler(user,command,args,mess):
    try:
        if len(args)<2:
            API_URL = "http://news.google.in/news/feeds?output=rss&num=10"
        else:
            API_URL = "https://news.google.com/news/feeds?q="+urllib.quote_plus(args)+"&output=rss"

        xml = urlopen(API_URL).read()
        doc = minidom.parseString(xml)
        iternews = iter(doc.documentElement.getElementsByTagName("item"))
        newsText = ""
        for news in iternews:
            newsText += news.getElementsByTagName("title")[0].firstChild.nodeValue + "\n"
            newsText += news.getElementsByTagName("link")[0].firstChild.nodeValue + "\n"
            newsText += "##############################################\n"
        #https://news.google.com/news/feeds?q=india&output=rss
        #print doc.documentElement.getElementsByTagName("item")[0].firstChild.nodeValue
        return newsText
    except:
        return "Sorry some error occured"

my_commands['movies']='Responce 1: %s'
def moviesHandler(user,command,args,mess):
    try:
        if len(args)<2:
            return "Please Provide city name to find the movies in your city"
        else:
            API_URL = "http://www.google.com/ig/api?movies="+args

        xml = urlopen(API_URL).read()
        doc = minidom.parseString(xml)
        iternews = iter(doc.documentElement.getElementsByTagName('movie'))
        newsText = ""
        for news in iternews:
            newsText += news.getElementsByTagName('title')[0].getAttribute('data') + "--"
            newsText += news.getElementsByTagName("genre")[0].getAttribute('data') + "\n"
            newsText += "########################\n"
        return newsText
    except:
        return "Sorry some error occured"

my_commands['assembla_registration']='Responce 1: %s'
def assembla_registrationHandler(user,command,args,mess):
    if len(args.split(" "))<2:
        return "Please Enter your key and secret key: example assembla_registration <key> <secret>"\
            " Please take care that your key and secret both are not including spaces or line break..."\
            "You can find your key and secret @ Assembla -> Edit profile -> API application and sessions"
    else:
        key = args.split(" ")[0]
        secret = args.split(" ")[1]
        who=mess.getFrom()
        username = str(who).split("/")[0]

        if is_valid_user(key, secret) is not False and check_for_duplicate(key, secret) is False:
            if register_new_user(username,key,secret):
                return "Congratulations now you are registered user."\
                    "Now you can use assembla commands from your gtalk"\
                    " .If you want to delete your keys you can use assembla unsubscibe command anytime."
            else:
                return "Some Database error occured"
        else:
            return "Either your keys are already used by someone else or Not valid keys.."\
                "Please Try Again"

my_commands['assembla']='Responce 1: %s'
def assemblaHandler(user,command,args,mess):
    who=mess.getFrom()
    username = str(who).split("/")[0]

    if check_if_keys_exists(username) is not False:
        arguments = args.split(" ")
        if len(arguments) > 0 and arguments[0] is not "":
            if arguments[0] == "my_spaces":
                return get_my_spaces(username)
            elif arguments[0] == "my_profile":
                return my_profile(username)
            elif arguments[0] == "unsubscribe":
                if delete_my_keys(username) is not False:
                    return "You are Successfully unsubscribed from assembla command"
                else:
                    return "Some Database error occured"

            elif len(arguments) > 1 and arguments[1] == "get_tickets":
                #return get_my_tickets(arguments[0], username)
                return "This command will be available soon. :)"
            else:
                return "Sorry "+ arguments[0] +" command is not supported."
        else:
            #show available commands
            return "Please try these commands: 'assembla my_spaces', 'assembla <Space_Name> get_tickets', 'assembla unsubscribe', 'assembla my_profile'..."
    else:
        return "Please Try assembla_registration command, you need to save your keys for once"\
            "After that you can use assembla commands directly."

my_commands['define']='Responce 1: %s'
def defineHandler(user,command,args,mess):
    if len(args)<2:
        return "Please Enter your word to search"
    else:
        try:
            API_URL = "http://services.aonaware.com/DictService/DictService.asmx/Define?word="
            url = API_URL + urllib.quote_plus(args)
            xml = urlopen(url).read()
            doc = minidom.parseString(xml)
            return doc.documentElement.getElementsByTagName("WordDefinition")[0].firstChild.nodeValue
        except:
            return "Sorry no meaning found for this query"
    
my_commands['slave']='Responce 1: %s'
def slaveHandler(user,command,args,mess):
    return "Yes Master!!!!"

my_commands['UTC']='Responce 1: %s'
def utcHandler(user,command,args,mess):
    return datetime.utcnow()

my_commands['google']='Responce 1: %s'
def googleHandler(user,command,args,mess):
    if len(args):
        return 'http://lmgtfy.com/?q='+urllib.quote_plus(args)
    else:
        return "please provide what you want to search for example: google example"

my_commands['password']='Responce 1: %s'
def passwordHandler(user,command,args,mess):
    return  ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(8))


########################### user handlers stop ###################################
############################ bot logic start #####################################
my_commands["UNKNOWN COMMAND"]='Sorry master, I do not know what you mean by "%s". Try "help"'
my_commands["UNKNOWN USER"]="I do not know you. Register first."


for i in globals().keys():
    if i[-7:]=='Handler' and i[:-7].lower()==i[:-7]: 
        commands[i[:-7]]=globals()[i]
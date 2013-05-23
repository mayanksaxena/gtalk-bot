import time
import time,os
import MySQLdb

LOGDIR='log/'
#CONF=(confjid,password)
CONF=('mayank.personal.bot@gmail.com','')

PROXY={}
def LOG(stanza,nick,text):
    ts=stanza.getTimestamp()
    if not ts:
        ts=stanza.setTimestamp()
        ts=stanza.getTimestamp()
    tp=time.mktime(time.strptime(ts,'%Y%m%dT%H:%M:%S'))
    if time.localtime()[-1]: tp+=3600
    tp=time.localtime(tp)
    fold=stanza.getFrom().getStripped().replace('@','%')+'_'+time.strftime("%Y.%m",tp)
    day=time.strftime("%d",tp)
    tm=time.strftime("%H:%M:%S",tp)
    try: os.mkdir(LOGDIR+fold)
    except: pass
    fName='%s%s/%s.%s.html'%(LOGDIR,fold,fold,day)
    try: open(fName)
    except:
        open(fName,'w').write("""<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xml:lang="ru-RU" lang="ru-RU" xmlns="http://www.w3.org/1999/xhtml">
    <head>
        <meta content="text/html; charset=utf-8" http-equiv="content-type" />
        <title>%s logs for %s.%s.</title>
    </head>
    <body>
<table border="1"><tr><th>time</th><th>who</th><th>text</th></tr>
"""%(CONF[0],fold,day))
    text='<pre>%s</pre>'%text
    open(fName,'a').write((u"<tr><td>%s</td><td>%s</td><td>%s</td></tr>\n"%(tm,nick,text)).encode('utf-8'))
    print (u"<tr><td>%s</td><td>%s</td><td>%s</td></tr>\n"%(tm,nick,text)).encode('koi8-r','replace')
#    print time.localtime(tp),nick,text

def presenceCB(conn,msg):
    try: 
        prs_type=msg.getType()
        who=msg.getFrom()
        name = str(who).split("/")
        username = name[0]
        source = name[1].split(".")[0]
        onlineUsers.append(username)
        time = str(datetime.now())
        try:
            cur.execute("""INSERT INTO userdetails(username,device,status,logtime) VALUES(%s,%s,%s,%s)""",(username,source,str(prs_type), time))
            db.commit()
        except:
            db.rollback()
    except:
        pass
        #conn.send(xmpp.protocol.Message('mayank.saxena@anktech.co.in',"Some Error Occured in presence log"))
        #conn.send(xmpp.protocol.Message('mayank.saxena@anktech.co.in',username+" "+source+" "+str(prs_type)))

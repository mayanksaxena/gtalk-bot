import urllib2
import json
import MySQLdb
from datetime import datetime

BASE_JSON_URL = 'https://api.assembla.com/v1/spaces/'
auth = []
db = MySQLdb.connect(host="localhost", user="root", passwd="", db="gtalkbot")
cur = db.cursor()  

def get_ticket(project_id, key, secret, ticket_type='my_active'):
	opener = urllib2.build_opener()
	opener.addheaders = [('X-Api-Key', key), ('X-Api-Secret', secret)]

	if ticket_type == 'my_active':
		get_url = my_active_tickets(project_id)
	else:
		get_url = my_followed_tickets(project_id)

	res = opener.open(BASE_JSON_URL+get_url)
	result = res.read()
	j = json.loads(result)
	return j



def my_followed_tickets(project_id):
    """
    To get json url for user's followed tickets
    """
    return project_id +'/tickets/my_followed.json'

def my_active_tickets(project_id):
    """
    To get json url for user's active tickets
    """
    return project_id+'/tickets/my_active.json'

def my_active_spaces(key, secret):
	opener = urllib2.build_opener()
	opener.addheaders = [('X-Api-Key', key), ('X-Api-Secret', secret)]
	res = opener.open("https://api.assembla.com/v1/spaces.json")
	result = res.read()
	j = json.loads(result)
	return j

def my_profile(username):
	keys = check_if_keys_exists(username)
	data = ''
	if keys is not False:
		my_profile = is_valid_user(keys[0],keys[1])
		data =  "Profile pic:-" + my_profile["picture"] + "\n#Login name-" + my_profile["login"] + "\n#Email ID:-"+ my_profile["email"]+"\n#"
	return data

def get_my_spaces(username):
	keys = check_if_keys_exists(username)
	data = ''
	if keys is not False:
		allspace = my_active_spaces(keys[0],keys[1])
		data = ""
        for i in allspace:
        	if i["name"] is not None:
        		data = data + i["name"].replace (" ", "_") +"\n#"+ '\n\n'
	return data

def get_my_tickets(pid, username):
	keys = check_if_keys_exists(username)
	data = ''
	if keys is not False:
		opener = urllib2.build_opener()
		opener.addheaders = [('X-Api-Key', keys[0]), ('X-Api-Secret', keys[1])]
		my_url = "https://api.assembla.com/v1/spaces/"+pid+"/tickets/my_active.json"
		print my_url
		res = opener.open(my_url)
		allspace = res.read()
		print allspace
		data = "In progress"
        for i in allspace:
        	print "-"*40
        	print i
        	print "-"*40
	return data

def is_valid_user(key, secret_key):
	try:
		opener = urllib2.build_opener()
		opener.addheaders = [('X-Api-Key', key), ('X-Api-Secret', secret_key)]
		res = opener.open("https://api.assembla.com/v1/user.json")
		result = res.read()
		auth.append(key)
		auth.append(secret_key)
		j = json.loads(result)
		return j
	except:
		pass

	return False
	

def check1():
	l = my_active_spaces()
	for i in l:
		if i["name"] is not None:
			print i["name"]
			print "-"*40

def register_new_user(uname, key, secret):
	time = str(datetime.now())
	try:
	    cur.execute("""INSERT INTO assembla VALUES(0,%s,%s,%s)""",(uname,key,secret))
	    db.commit()
	    return True
	except:
	    db.rollback()
	    return False

def check_for_duplicate(key,secret):
	try:
		cur.execute("""SELECT* FROM assembla WHERE assembla.key=%s AND assembla.secret=%s""",(key, secret))
		rows = cur.fetchall()
		if len(rows) > 0:
			return True
		else:
			return False
	except:
		return False

def delete_my_keys(uname):
	time = str(datetime.now())
	try:
	    cur.execute("""DELETE FROM assembla Where assembla.username=%s""",(uname))
	    db.commit()
	    return True
	except:
	    db.rollback()
	    return False

def check_if_keys_exists(uname):
	try:
		cur.execute("""SELECT* FROM assembla WHERE assembla.username=%s""",(uname))
		rows = cur.fetchall()
		if len(rows) > 0:
			return [rows[0][2], rows[0][3]]
		else:
			return False
	except:
		return False

#is_valid_user('f148869521ab8158f448', 'b39dd71890ba5082503532b02bb501433278ced9')
#register_new_user("mayank.saxena@anktech.co.in","f148869521ab8158f448", "b39dd71890ba5082503532b02bb501433278ced9")
#check_for_duplicate("f148869521ab8158f448", "b39dd71890ba5082503532b02bb501433278ced9")
#delete_my_keys("mayank.saxena@anktech.co.in")
#assembla subcommands
#print check_if_keys_exists("mayank.saxena@anktech.co.in")
def check():
	if check_if_keys_exists("mayank.saxena@anktech.co.in") is not False:
		#show available commands
		print "Awesome you are a valid user you can use our subcommands"
	else:
		key = raw_input("Please Insert your key from assembla")
		secret = raw_input("Please Insert yout sectey key from assembla")
		print key
		print secret
		if is_valid_user(key, secret) is not False and check_for_duplicate(key, secret) is False:
			print register_new_user("mayank.saxena@anktech.co.in",key, secret)
		else:
			print "Either your keys are already used by someone else or Not valid keys.."\
				"Please Try Again"

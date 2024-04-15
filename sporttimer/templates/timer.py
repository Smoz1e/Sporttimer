# -*- coding: utf-8 -*-
import logging
import time, string
from flask import Flask, redirect, url_for,session,request,render_template
from datetime import datetime, timedelta
import pyodbc
import requests
import sqlite3
import random
import bcrypt


logging.basicConfig(level=logging.INFO, filename="/var/www/log/sb_call.log",filemode="a",format="%(asctime)s %(levelname)s %(message)s")
sqlite3db_str='/var/www/db/sb_call.db'
UPLOAD_FOLDER = '/var/www/usrfiles/'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif','zip','msrcincident','7z','vnc','exe','rar'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ALLOWED_EXTENSIONS'] =ALLOWED_EXTENSIONS
app.secret_key = 'asdfgsgq34Q#T$tq344tgfa43rga423,@42341'
app.permanent_session_lifetime = timedelta(hours=20)

check_conn=0
try:
    conn = sqlite3.connect(sqlite3db_str)
    conn.close()
except sqlite3.DatabaseError as e:
    check_conn=-1
    now=str(datetime.now())
    logging.error(' Ошибка подключения базы данных SQLite3  %s' % e)

    print ('Ошибка подключения базы данных SQLite3  %s' % e)
finally:
    print("SQLite3 ")


if check_conn == 0:
    try:
        conn = sqlite3.connect(sqlite3db_str)
        cur = conn.cursor()
        sql = """CREATE TABLE IF NOT EXISTS call_events(
           id INTEGER  PRIMARY KEY AUTOINCREMENT,
           button_id INTEGER,
           event TEXT,
           device TEXT,
           status INTEGER,
           Updatetime TEXT);
        """
        cur.execute(sql)
        conn.commit()


    except sqlite3.DatabaseError as e:
        if conn:
            conn.rollback()
        now = str(datetime.now())
        logging.error(' Ошибка  базы данных SQLite3  %s' % e)
        print ('Error %s' % e)
    finally:
        print("Table [call_events] exist or created")
        cur.close()
        conn.close()
def timeformat(n):
	n = int(n)
	h = n // 60
	m = n % 60
	x = h % 10
	y = m % 10
	if x == 1:
		if m // 10 == 1:
			a = str(h) + ' час ' + str(m) + ' минут'
		elif y == 1:
			a = str(h) + ' час ' + str(m) + ' минута'
		elif y == 2 or y == 3 or y == 4:
			a = str(h) + ' час ' + str(m) + ' минуты'
		elif m == 0:
			a = str(h) + ' час'
		else:
			a = str(h) + ' час ' + str(m) + ' минут'
	elif x == 2 or x == 3 or x == 4:
		if m // 10 == 1:
			a = str(h) + ' часа ' + str(m) + ' минут'
		elif y == 1:
			a = str(h) + ' часа ' + str(m) + ' минута'
		elif y == 2 or y == 3 or y == 4:
			a = str(h) + ' часа ' + str(m) + ' минуты'
		elif m == 0:
			a = str(h) + ' часа'
		else:
			a = str(h) + ' часа ' + str(m) + ' минут'
	elif x == 0:
		if m // 10 == 1:
			a = str(m) + ' минут'
		elif y == 1:
			a = str(m) + ' минута'
		elif y == 2 or y == 3 or y == 4:
			a = str(m) + ' минуты'
		elif m == 0:
			a = str(-1)
		else:
			a = str(m) + ' минут'
	else:
		if m // 10 == 1:
			a = str(h) + ' часов ' + str(m) + ' минут'
		elif y == 1:
			a = str(h) + ' часов ' + str(m) + ' минута'
		elif y == 2 or y == 3 or y == 4:
			a = str(h) + ' часов ' + str(m) + ' минуты'
		elif m == 0:
			a = str(h) + ' часов'
		else:
			a = str(h) + ' часов ' + str(m) + ' минут'
	return a

def checklogin():
	session_s=''
	Email=''
	if 'F1cloud' in session:
		session_s=session['F1cloud']
	if 'F1cloud_email' in session:
		Email=session['F1cloud_email']
	UserName=''
	if (session!='') and (Email!=''):
		cnxn = pyodbc.connect(CONNECTION_STRING)
		cursor = cnxn.cursor()
		try:
			cursor.execute("SELECT [Name],[Rights] from [f1base].dbo.[ManagerList] where ([Email]=?)and(session=?)",Email,session_s)
			row1 = cursor.fetchone()

			if row1:
				UserName=row1[0]
			else :
				cursor.close()
				cnxn.close()
				return False
		except:
			e=0

		cursor.close()
		cnxn.close()
	else:
		return False
	return True
def get_rights(email):
	Rights=''
	cnxn = pyodbc.connect(CONNECTION_STRING)
	cursor = cnxn.cursor()
	try:
		cursor.execute("SELECT [Rights] from [F1base].[dbo].[ManagerList]  where ([Email]=?)", email)
		row = cursor.fetchone()
		if row:
			Rights = row[0]
	except pyodbc.DatabaseError as e:
		if cnxn:
			cnxn.rollback()
	##print ('Error %s',  e)

	cursor.close()
	cnxn.close()
	#print('Rights='+str(Rights))
	return Rights
def get_managerid_by_phone(phone):
	res=-1
	cnxn = pyodbc.connect(CONNECTION_STRING)
	cursor = cnxn.cursor()
	try:
		cursor.execute("SELECT [managerid] from [dbo].[tg_users]  where ([phone]=?)", phone)
		row = cursor.fetchone()
		if row:
			res = row[0]
	except pyodbc.DatabaseError as e:
		if cnxn:
			cnxn.rollback()
	##print ('Error %s',  e)

	cursor.close()
	cnxn.close()
	#print('Rights='+str(Rights))
	return res
def get_email_by_managerid(managerid):
	res=-1
	cnxn = pyodbc.connect(CONNECTION_STRING)
	cursor = cnxn.cursor()
	try:
		cursor.execute("SELECT [Email] from [dbo].[ManagerList]  where ([managerid]=?)", managerid)
		row = cursor.fetchone()
		if row:
			res = row[0]
	except pyodbc.DatabaseError as e:
		if cnxn:
			cnxn.rollback()
	##print ('Error %s',  e)
	finally:
		cursor.close()
		cnxn.close()
	return res
def check_tg_code(managerid,code):
	''' res =
	-1 - срок действия кода истек
	0 - код не верный
	1 - код верный


	'''
	res=0
	cnxn = pyodbc.connect(CONNECTION_STRING)
	cursor = cnxn.cursor()
	try:
		cursor.execute("SELECT [tg_code],[expired] from [dbo].[tg_checklogin]  where ([managerid]=?)", managerid)
		row = cursor.fetchone()
		if row:
			expired=row[1]
			if expired<datetime.now():
				res=-1
			else:
				if code == row[0]:
					res=1
	except pyodbc.DatabaseError as e:
		print ('Error %s',  e)
	finally:
		cursor.close()
		cnxn.close()
	#print('Rights='+str(Rights))
	return res


def register_event(button_id, event, device):
	check_conn = 0
	try:
		conn = sqlite3.connect(sqlite3db_str)
		conn.close()
	except sqlite3.DatabaseError as e:
		check_conn = -1
		now = str(datetime.now())

		print('Ошибка подключения базы данных SQLite3  %s' % e)
	finally:
		print("SQLite3 ")

	if check_conn == 0:
		try:
			conn = sqlite3.connect(sqlite3db_str)
			cur = conn.cursor()

			sql = '''
                update call_events set status=1 where button_id=?

            '''
			params = [button_id]
			cur.execute(sql, params)
			dt = datetime.now()
			updatetime = dt.strftime("%Y%m%d %H:%M:%S")

			params = [button_id, event, device, updatetime]
			sql = """insert into  call_events (
               button_id,
               event,
               device,
               Updatetime,
                status) values (?,?,?,?,0)
            """
			cur.execute(sql, params)
			conn.commit()
			cur.close()


		except sqlite3.DatabaseError as e:
			if conn:
				conn.rollback()
			now = str(datetime.now())
			print('Error %s' % e)
		finally:
			# print("Table [call_events] exist or created")

			conn.close()
def tg_send_code(managerid,code):

	cnxn = pyodbc.connect(CONNECTION_STRING)
	cursor = cnxn.cursor()
	res=True
	chatid=0
	tid=0
	expired = 	datetime.now() + timedelta(minutes = 5)

	print(expired)
	print(managerid)
	try:
		cursor.execute("SELECT [ManagerID] from [F1base].[dbo].[tg_users]  where [Managerid]=?", managerid)
		row = cursor.fetchone()
		print(row)
		if row:
			cursor.execute("SELECT [ManagerID] from [F1base].[dbo].[tg_checklogin]  where [Managerid]=?", managerid)
			row = cursor.fetchone()
			if row:
				print(row)
				params=[code,expired,managerid]
				cursor.execute("Update [dbo].[tg_checklogin] set [TG_Code]=?,[Expired]=?  where [Managerid]=?", params)
				cnxn.commit()

			else:
				print('new managerid inserted')
				params = [code, expired, managerid]
				cursor.execute("Insert into  [dbo].[tg_checklogin] ([TG_Code],[Expired], [Managerid]) values (?,?,?)", params)
				cnxn.commit()
	except pyodbc.DatabaseError as e:
		print("Error SQL %s",e)
		if cnxn:
			cnxn.rollback()
		res=False


	try:
		cursor.execute("SELECT [chatid],[tid] from [F1base].[dbo].[tg_users]  where [Managerid]=?", managerid)
		row = cursor.fetchone()
		if row:
			chatid = row[0]
			tid= row[1]

	except pyodbc.DatabaseError as e:
		print("Error SQL %S", e)
		if cnxn:
			cnxn.rollback()
		res=False
	if chatid!=0:
		status=tg_users_messagelog(tid,bot_name,'text','Для входа в корпоратиный портал используйте код: '+str(code),chatid,status=1)
	cursor.close()
	cnxn.close()
	return res
def reserv_change_status(ID, status, Manager_id, Prog_reserv_id):
	try:
		res=1
		conn = pyodbc.connect(CONNECTION_STRING)
		cur = conn.cursor()
		params = [ID]
		cur.execute('Select [id],[tid],[status] from dbo.[tg_reserv] where ([id]=?)', params)
		row = cur.fetchone()
		updatetime = datetime.now()
		if row:
			params = [status,updatetime,Manager_id,Prog_reserv_id,ID]
			cur.execute('Update  tg_reserv set status=?,Manager_answertime=?, Manager_id=?,Prog_reserv_id=? where (id=?)', params)
			conn.commit()
			cur.close()
	except pyodbc.DatabaseError as e:
		logging.error(' reserv_change_status(TID, status) Ошибка базы данных MSSQL  %s' % e)
		res=-1

		#print('registration_request_name SQL Error %s' % e)

	finally:

		if (conn):
			conn.close()

	return res
@app.route("/")
def main():



	return render_template('sb_call.html');


def get_events(id):
	check_conn=0
	try:
		conn = sqlite3.connect(sqlite3db_str)
		conn.close()
	except sqlite3.DatabaseError as e:
		check_conn = -1
		now = str(datetime.now())

		print('Ошибка подключения базы данных SQLite3  %s' % e)
	finally:
		print("SQLite3 ")

	res=[]
	if check_conn == 0:
		try:
			conn = sqlite3.connect(sqlite3db_str)
			cur = conn.cursor()

			params = [id]
			sql = """Select [id],[button_id],[event],[device],[updatetime] from call_events where (id>=?)and(status=0) 

	        """
			cur.execute(sql, params)
			row = cur.fetchone()
			while row:
				res_item={'id':row[0],'button_id':row[1],'event':row[2],'device':row[3],'updatetime':row[4]}
				res.append(res_item)
				print(row)
				row = cur.fetchone()
				#res=row
			cur.close()


		except sqlite3.DatabaseError as e:
			if conn:
				conn.rollback()
			now = str(datetime.now())
			print('Error %s' % e)
		finally:
			#print("Table [call_events] exist or created")
			conn.close()
	return res

@app.route('/sb_call_api', methods=['post','get'])
def sb_call_api():
	res= {'res':-1}
	global CONNECTION_STRING
	getmessages = request.form.get('getmessages', default='', type=str)
	req_json=request.get_json()
	#print(req_json)
	try:
		cmd=req_json['cmd']
	except:
		cmd=''
		res={'res':'Cmd not found'}


	if cmd=='sendevents':
		button_id=0
		event=''
		res = {'res': -1}
		try:
			button_id = req_json['button_id']
			event= req_json['event']
		except:
			res = {'res': -1}

		if (button_id>0)and(event!=''):
			register_event(button_id,event,'staff_station')
			res = {'res': 1}
	if cmd=='getevents':
		id=-1
		try:
			id = req_json['id']
		except:
			id = -1
			res = {'res': -1}
		events=get_events(id)
		res={'res':len(events),'events':events}



	return  res
@app.route('/login_api', methods=['post','get'])
def login_api():
	request_json=request.get_json() or {}
	phone=request_json['phone']
	phone=phone.replace('+','')
	phone = phone.replace(' ', '')
	phone = phone.replace('(', '')
	phone = phone.replace(')', '')
	phone = phone.replace('-', '')
	res={'status':'Ok','phone':phone}
	#print(phone)
	code=random.randrange(1000,9999)
	if phone!='':
		tg_send_code(get_managerid_by_phone(phone),code)


	return  res

@app.route('/login',methods=['post', 'get'])
def login():
	message_email = ''
	message_tg=''
	random_s=''
	Email = request.form.get('username', default = '', type = str)
	password = request.form.get('password', default = '', type = str)
	phone_code = request.form.get('phone_code', default = '', type = str)
	tg_phone = request.form.get('tg_phone', default = '', type = str)
	login_phone = request.form.get('login_phone', default = '', type = str)
	print('login_phone='+login_phone)
	##print "login "+Email+password
	if login_phone=="tg_login" and tg_phone !='':
		managerid=get_managerid_by_phone(tg_phone)
		if managerid!=-1:
			check=check_tg_code(managerid,phone_code)
			if check==-1:
				print('Код устарел')
				message_tg = "Код устарел"
				return render_template('login.html', message_email=message_email, message_tg=message_tg,tg_phone=tg_phone)
			elif check==0:
				print('Код не верный')
				message_tg="Код не верный"
				return render_template('login.html', message_email=message_email, message_tg=message_tg,tg_phone=tg_phone)
			elif check==1:
				print('Код принят')
				cnxn = pyodbc.connect(CONNECTION_STRING)
				cursor = cnxn.cursor()
				try:
					random_s = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(32)])
					##print 'Random str: '+random_s
					Email=get_email_by_managerid(managerid)
					cursor.execute("Update [f1base].dbo.[ManagerList] set [Session]=?  where ([Email]=?)", random_s,
								   Email)
					cursor.commit()
					session.permanent = True
					session['F1cloud'] = random_s
					session['F1cloud_email'] = Email
					return redirect(url_for('main'))
				except pyodbc.DatabaseError as e:
					if cnxn:
						cnxn.rollback()
				##print ('Error %s' % e)
				finally:
					cursor.close()
					cnxn.close()



	if Email!= '' and password != '':
		cnxn = pyodbc.connect(CONNECTION_STRING)
		cursor = cnxn.cursor()
		try:
			cursor.execute("SELECT [Email],[Name],[Pass] from [F1base].dbo.[ManagerList] where ([Email]=?)",Email)
			row1 = cursor.fetchone()
			if row1:
				print('Pass hash: ')
			if bcrypt.checkpw(password.encode(), row1[2].encode()):
				random_s = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(32)])
					##print 'Random str: '+random_s
				cursor.execute("Update [f1base].dbo.[ManagerList] set [Session]=?  where ([Email]=?)",random_s,Email)
				cursor.commit()
				session.permanent = True
				session['F1cloud']=random_s
				session['F1cloud_email']=Email
				return redirect(url_for('main'))

		except pyodbc.DatabaseError as e:
			if cnxn:
				cnxn.rollback()
			##print ('Error %s' % e)

		cursor.close()
		cnxn.close()
		message_email = "Не верное имя пользователя или пароль"
		return render_template('login.html', message_email=message_email,message_tg=message_tg)

	return render_template('login.html', message_email=message_email,tg_phone=tg_phone,message_tg=message_tg)
@app.route("/eventlog", methods=['POST','get'])
def eventlog():
	hrefseventlog=[]
	hrefs_item={}
	global sqlite3db_str
	conn = sqlite3.connect(sqlite3db_str)
	cur = conn.cursor()
	try:
		cur.execute("""Select * from Emails""")

		while True:
			row=cur.fetchone()
			if row:
				hrefs_item=dict(event_id=str(row[0]),email_addr=str(row[1]),
				msg=str(row[2]),
				host_ip=row[3],
				UID=row[4],
				updatetime=row[5],
				Recive_time=row[6])
				print( row)



				hrefseventlog.append(hrefs_item)
			else:
				break
	finally:

		cur.close()
		conn.close()








	return render_template('eventlog.html',hrefseventlog=hrefseventlog);


@app.route('/logout',methods=['post', 'get'])
def logout():
	message = ''
	session['F1cloud']=''
	session['F1cloud_email']=''
	return redirect(url_for('login'))
if __name__ == '__main__':
##	app.run(debug=True,port=80, host='192.168.105.124', ssl_context=('/var/www/ssl/cert1.key', '/var/www/ssl/privkey1.key'))
	app.run(debug=True,port=80, host='0.0.0.0')
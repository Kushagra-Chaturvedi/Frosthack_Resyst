import sqlite3 
import hashlib
conn = sqlite3.connect('data.db')


c = conn.cursor()
def create_usertable():
	c.execute('''CREATE TABLE IF NOT EXISTS userstable(
	 username text,
	 email_id text,
	 password text)''')


def add_userdata(username,email_id,password):
	c.execute('INSERT INTO userstable(username,email_id,password) VALUES (?,?,?)',(username,email_id,password))
	conn.commit()

def login_user(email_id,password):
	c.execute('SELECT * FROM userstable WHERE email_id = ? AND password = ?',(email_id,password))
	data = c.fetchall()
	return data
def check_pass(password):
	c.execute('SELECT * FROM userstable WHERE password = ?',(password,))
	data = c.fetchall()
	return data

def existing_user(email_id):
	c.execute('SELECT * FROM userstable WHERE email_id =?',(email_id,))
	data = c.fetchall()
	return data
def create_sp():
	c.execute('''CREATE TABLE IF NOT EXISTS sp_table(
	 email_id text,
	 oxy text,
	 plasma text,
	 rem text,
	 pin text,
	 city text,
	 state text,
	 phone int,
	 upi text
	 )''')
def add_service_provider(email_id, oxy, plasma, rem,pin,city,state, phone, upi):
	c.execute('''INSERT INTO	
		sp_table(email_id, oxy, plasma, rem, pin, city, state,phone,upi) VALUES (?,?,?,?,?,?,?,?,?)
		''',(email_id,oxy, plasma, rem,pin,city,state,phone,upi))
	conn.commit()

def find_donors(pin,needed):
	if needed=='Oxygen Cylinders':
		c.execute("""SELECT * FROM sp_table WHERE pin = ? and oxy=?""", (pin,needed))
		data = c.fetchall()
		if len(data)==0:
			return []
		return data
	elif needed=='Plasma':
		c.execute("SELECT * FROM sp_table WHERE pin = ? and plasma=?", (pin,needed))
		data = c.fetchall()
		return data
	elif needed=='Remdesivir Doses':
		c.execute("SELECT * FROM sp_table WHERE pin = ? and rem=?", (pin,needed))
		data = c.fetchall()
		return data
	else:
		c.execute("SELECT * FROM sp_table WHERE pin = ? ", (pin,))
		data = c.fetchall()
		return data
def refine_donors(email):
	c.execute("SELECT * FROM userstable WHERE email_id=?",(email,))
	data = c.fetchall()
	return data
def make_hashes(password):
	return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password,hashed_text):
	if make_hashes(password) == hashed_text:
		return hashed_text
	return False

#c.execute('drop table if exists userstable')
#c.execute('drop table if exists sp_table')



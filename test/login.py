import requests
import json

<<<<<<< Updated upstream
login_url = 'http://54.:5000/login'
=======
login_url = 'http://54.149.235.253:5000/login'
>>>>>>> Stashed changes
user_data = {'email': 'xzhu15@illinois.edu', 'password': '123'}

def login():
	r = requests.post(login_url, data=user_data)
	print r
	return json.loads(r.content)

def renew_token(token):
	headers = {'token': token}
	r = requests.get(login_url, headers=headers)
	return json.loads(r.content)

if __name__ == '__main__':
	result = login()
	token = result['token']
	print 'old token:', token

	result = renew_token(token)
	token = result['token']
	print 'new token:', token
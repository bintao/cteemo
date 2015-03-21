import requests
import json
from login_test import login

profile_url = 'http://54.149.235.253:5000/profile'
profile_data = {
	'username': 'test',
	'school': 'UIUC',
	'intro': 'test intro',
	'profile_icon': None
}

def edit_profile(token):
	headers = {'token': token} 
	r = requests.post(profile_url, headers=headers, data = profile_data)
	result = json.loads(r.content)
	assert result == profile_data

def load_profile(token):
	headers = {'token': token} 
	r = requests.get(profile_url, headers=headers)
	result = json.loads(r.content)
	assert result == profile_data

if __name__ == '__main__':
	login = login()
	token = login['token']

	edit_profile(token)
	load_profile(token)
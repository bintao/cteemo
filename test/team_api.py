import requests
import json
from datetime import datetime
login_url = 'http://54.149.235.253:5000/login'
user_data = {'email': 'bintao@cteemo.com', 'password': '1234'}
user2_data ={'email': 'zilin@cteemo.com', 'password': '123'}
password_url = 'http://54.149.235.253:5000/change_password'
create_team = 'http://54.149.235.253:5000/create_team/lol'
get_team = 'http://54.149.235.253:5000/my_team/lol'
login = requests.post(login_url, data=user_data)
login2 = requests.post(login_url, data=user2_data)
token = json.loads(login.content)['token']
token2 = json.loads(login2.content)['token']
join_data = {'teamName': 'test'}
search_team = 'http://54.149.235.253:5000/search_team/lol'
search_user = 'http://54.149.235.253:5000/search_profile'
profile = 'http://54.149.235.253:5000/profile'

userdata= {
'username':'alex', 
'school':'UIUC',
'intro':'22'
 }




team_data = {
	'teamName': 'Toddm',
	'teamIntro': 'hahakk',
	'isSchool': True,
	'school': 'UIUC'
     }

search_data  = {'school': 'UIUC'}

    
def upload(token,data):
    headers = {'token': token} 
    r = requests.post(profile, headers=headers,data=data)
    return r.json()
    
def get(token):
    headers = {'token': token} 
    r = requests.get(get_team, headers=headers)
    return r.json()


def create(token, data):
    headers = {'token': token} 
    r = requests.post(create_team, headers=headers,data=data)
    return r.json()

def delete(token):
    headers = {'token': token} 
    r = requests.delete(create_team, headers=headers)
    return r.json()
    
def leave(token):
    headers = {'token': token} 
    r = requests.delete(get_team, headers=headers)
    return r.json()
    
def search(token,data):
    headers = {'token': token} 
    r = requests.get(search_team, headers=headers,data=data)
    return json.loads(r.content)
    
def search_u(token,data):
    headers = {'token': token} 
    r = requests.get(search_user,headers=headers,data=data)
    return r.json()
    
def get_profile(token):
    headers = {'token': token} 
    r = requests.get(profile,headers=headers)
    return r.json()



print create(token2,team_data)
import requests
import json
from datetime import datetime
login_url = 'http://54.149.235.253:5000/login'
user_data = {'email': 'bintao@cteemo.com', 'password': '1234'}
user2_data ={'email': 'zilin@cteemo.com', 'password': '123'}
login = requests.post(login_url, data=user_data)
login2 = requests.post(login_url, data=user2_data)
token = json.loads(login.content)['token']
token2 = json.loads(login2.content)['token']

team = 'http://54.149.235.253:5000/team_post'

post = 'http://54.149.235.253:5000/player_post'

post_data = {'content':'I want to find someone to talk'}


def player_post(token,data):
    headers = {'token': token} 
    r = requests.post(post, headers=headers,data=data)
    return r.json()


def get(token):
    headers = {'token': token} 
    r = requests.get(post, headers=headers)
    return r.json()


def team_post(token,data):
    headers = {'token': token} 
    r = requests.post(team, headers=headers,data=data)
    return r.json()


def team_get(token):
    headers = {'token': token} 
    r = requests.get(team, headers=headers)
    return r.json()



print team_post(token2,post_data)

print team_get(token)

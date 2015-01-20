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
create_tournament = 'http://54.149.235.253:5000/create_tournament'
join_tournament = 'http://54.149.235.253:5000/join_tournament'
view_tournament = 'http://54.149.235.253:5000/view_tournament'
match = 'http://54.149.235.253:5000/report_result'
tournamentsearch = {'tournamentName':'UIUCvsMIT'}
ID={'tournamentID':38,'tournamentName':'UIUCvsMIT'}

tournament_data = {
    'tournamentName': 'UIUCvsMIT',
    'isSchool': True,
    'entry_fee': 5,
    'school': 'UIUC',
    'size': 4,
    'descriptions': 'test for what',
    'Total_Prize': 5 ,
    'teamSize':5,
    'map':"Summoner's Rift",
    'pick':'BLIND PICK',
    'rounds':[{'startTime': str(datetime.now()),'bestOfN' : 3 },
               {'startTime': str(datetime.now()),'bestOfN' : 3 }]
}

def tournament(token,data):
    headers = {'token': token, 'content-type': 'application/json; charset=utf8'} 
    r = requests.post(create_tournament, headers=headers,data=json.dumps(data))
    return r.json()

def my_tournament(token):
    headers = {'token': token} 
    r = requests.get(create_tournament, headers=headers)
    return r.json()

def search_tournament(token,data):
    headers = {'token': token} 
    r = requests.get(join_tournament, headers=headers,data=data)
    return r.json()

def join(token,data):
    headers = {'token': token} 
    r = requests.post(join_tournament, headers=headers,data=data)
    return r.json()


def view(token,data):
    headers = {'token': token} 
    r = requests.get(view_tournament,headers=headers,data=data)
    return r.json()

def getcode(token,data):
    headers = {'token': token} 
    r = requests.post(view_tournament,headers=headers,data=data)
    return r

def get_match(token):
    headers = {'token': token} 
    r = requests.post(match,headers=headers)
    return r

print join(token2,ID)
print get_match(token2)



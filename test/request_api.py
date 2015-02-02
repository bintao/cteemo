from team_api import *

     
invite_request = 'http://54.149.235.253:5000/invite_request/lol'

teammate_request = 'http://54.149.235.253:5000/manage_team/lol'

sent_request='http://54.149.235.253:5000/my_team/lol'

join_request = 'http://54.149.235.253:5000/join_request/lol'

profile = {'profileID':9}

teamName = {'teamName':'Todd'}

def team_request(token,data):
    headers = {'token': token} 
    r = requests.post(teammate_request, headers=headers,data=data)
    return r.json()

def view_request(token):
    headers = {'token': token}
    r = requests.get(invite_request, headers=headers)
    return r.json()

def accept(token,data):
    headers = {'token': token}
    r = requests.post(invite_request, headers=headers,data=data)
    return r.json()

def decline(token,data):
    headers = {'token': token}
    r = requests.delete(invite_request, headers=headers,data=data)
    return r.json()

def join(token,data):
    headers = {'token': token}
    r = requests.post(sent_request, headers=headers,data=data)
    return r.json()

def join_view(token):
    headers = {'token': token}
    r = requests.get(join_request, headers=headers)
    return r.json()

def join_accept(token,data):
    headers = {'token': token}
    r = requests.post(join_request, headers=headers,data=data)
    return r.json()

def join_decline(token,data):
    headers = {'token': token}
    r = requests.delete(join_request, headers=headers,data=data)
    return r.json()

print join_view(token2)
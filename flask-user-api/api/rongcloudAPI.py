from flask import request, abort
from flask.ext.restful import Resource, reqparse
from model.profile import Profile
from model.user import User
from util.userAuth import auth_required
from util.serialize import serialize, profile_search_serialize
from util.exception import InvalidUsage
from random import randint
import time
from mongoengine.queryset import Q
import boto
import os
import requests
import json
import hashlib


profileParser = reqparse.RequestParser()
profileParser.add_argument('username', type=str)
profileParser.add_argument('school', type=str)
profileParser.add_argument('intro', type=str)
profileParser.add_argument('lolID', type=str)
profileParser.add_argument('dotaID', type=str)
profileParser.add_argument('hstoneID', type=str)
profileParser.add_argument('profileID', type=int)
profileParser.add_argument('page', type=int)


class RongcloudAPI(Resource):
    @auth_required
    def get(self, user_id):
        # load profile 
        profile =  Profile.objects(user=user_id).first()
        if profile is None:
        	raise InvalidUsage("Wrong action",401)

        rong_json,headers = dict(),dict()
        rong_json['userId'] = profile.id
        rong_json['name'] = profile.username
        rong_json['portraitUri'] = profile.profile_icon

        headers['App-Key'] = 'bmdehs6pdve3s'
        headers['Nonce'] = str(randint(1,99))
        headers['Timestamp'] = str(time.time())
        headers['Signature'] = str(hashlib.sha1(headers['App-Key']+headers['Nonce']+headers['Timestamp']).hexdigest())
        getToken_url = 'https://api.cn.rong.io/user/getToken.json'

        r = requests.post(getToken_url, data=rong_json, headers=headers)
        data = r.json()
        print data

        if data['code'] != 200:
        	raise InvalidUsage('Rong Cloud error',data['code'])

        user = User.objects(id=user_id).first()
        user.rongToken = data['token']

        return {'token' : data['token']}

    

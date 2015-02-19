from flask import request, abort
from flask.ext.restful import Resource, reqparse
from model.profile import Profile
from model.user import User
from util.userAuth import auth_required
from util.serialize import serialize, profile_search_serialize
from util.exception import InvalidUsage
from mongoengine.queryset import Q
import boto
import os
import requests
import json


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
        	raise InvalidUsage(401,"Wrong action")

        rong_json = dict()
        rong_json['userId'] = profile.id
        rong_json['name'] = profile.username
        rong_json['portraitUri'] = profile.profile_icon
        getToken_url = 'https://api.cn.rong.io/user/getToken.json'

        r = requests.post(getToken_url, data=rong_json)
        data = r.json()

        if data['code'] != 200:
        	raise InvalidUsage(data['code'],'Rong Cloud error')

        user = User.objects(id=user_id).first()
        user.rongToken = data['token']

        return {'token' : data['token']}

    

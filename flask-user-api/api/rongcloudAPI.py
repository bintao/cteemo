from flask import request, abort
from flask.ext.restful import Resource, reqparse
from model.profile import Profile
from model.user import User
from util.userAuth import auth_required
from util.serialize import serialize, profile_search_serialize
from util.exception import InvalidUsage
import os
import json
import unittest
import logging
from server_sdk_python.rong import ApiClient

app_key = "bmdehs6pdve3s"
app_secret = "dDv1kKuKC01II"
os.environ.setdefault('rongcloud_app_key', app_key)
os.environ.setdefault('rongcloud_app_secret', app_secret)

logging.basicConfig(level=logging.INFO)

api = ApiClient()


def rongcloudToken(self, user_id):
    # load profile 
    profile =  Profile.objects(user=user_id).first()
    if profile is None:
    	raise InvalidUsage("Wrong action",401)

    token = api.call_api(
    action="/user/getToken",
    params={
        "userId": profile.id,
        "name":profile.username,
        "portraitUri":profile.profile_icon
        }
    )

    user = User.objects(id=user_id).first()
    user.rongToken = token
    return token


    

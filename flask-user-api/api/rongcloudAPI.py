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


def rongcloudToken(profile_id):
    # load profile 
    profile = Profile.objects(id=profile_id).first()
    if profile is None:
    	raise InvalidUsage("Wrong action",401)

    user = profile.user

    token = api.call_api(
    action="/user/getToken",
    params={
        "userId": profile_id,
        "name":profile.username,
        "portraitUri":profile.profile_icon
        }
    )

    user.rongToken = token['token']
    user.save()
    return token

def rongRefresh(profile_id):
    profile = Profile.objects(id=profile_id).first()
    if profile is None:
        raise InvalidUsage("Wrong action",401)

    user = profile.user

    self.call_api(
            action=self.ACTION_USER_REFRESH,
            params={
                "userId": profile_id,
                "name": profile.username,
                "portraitUri": profile.profile_icon
            }
        )

    

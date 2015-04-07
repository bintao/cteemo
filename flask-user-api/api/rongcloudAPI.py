from flask import request, abort
from flask.ext.restful import Resource, reqparse
from model.profile import Profile
from model.user import User
from model.lol_team import LOLTeam
from util.userAuth import auth_required
from util.serialize import serialize, profile_search_serialize
from util.exception import InvalidUsage
import os
import json
import unittest
import logging
from server_sdk_python.rong import ApiClient

app_key = "pkfcgjstfmcl8"
app_secret = "dwGJ4fYYGJ"
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
    if user.rongToken is None:
        return rongcloudToken(profile_id)
    api.call_api(
            action="/user/refresh",
            params={
                "userId": profile_id,
                "name": profile.username,
                "portraitUri": profile.profile_icon
            }
        )

def rongcloudCreateGroup(team_id):
    team = LOLTeam.objects(id=team_id).first()
    if team is None:
        raise InvalidUsage("Wrong action",401)

    profile = team.captain

    api.call_api(
            action="/group/create",
            params={
                "userId":profile.id,
                "groupId":team_id,
                "groupName":team.teamName
            }
        )

def rongcloudJoinGroup(profile_id,team_id,teamName):
    api.call_api(
            action="/group/join",
            params={
                "userId":profile_id,
                "groupId":team_id,
                "groupName":team.teamName
            }
        )

def rongcloudLeaveGroup(profile_id,team_id):
    api.call_api(
            action="/group/quit",
            params={
                "userId":profile_id,
                "groupId":team_id,
            }
        )

def rongcloudDismissGroup(profile_id,team_id):
    api.call_api(
            action="/group/dismiss",
            params={
                "userId":profile_id,
                "groupId":team_id,
            }
        )   

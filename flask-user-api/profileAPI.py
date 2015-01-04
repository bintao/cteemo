from flask import request, abort
from flask.ext.restful import Resource, reqparse
from model.redis import redis_store
from model.profile import Profile
from model.teaminfo import TeamInfo
import boto
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)


SECRET_KEY = 'flask is cool'

def verify_auth_token(token):
    s = Serializer(SECRET_KEY)
    try:
        email = s.loads(token)
    except SignatureExpired:
        return None    # valid token, but expired
    except BadSignature:
        return None    # invalid token
    print redis_store.get(email)
    if redis_store.get(email) == token:
        return email
    else:
        return None


profileParser = reqparse.RequestParser()
profileParser.add_argument('token', type=str)
profileParser.add_argument('school', type=str)
profileParser.add_argument('lol_id', type=str)
profileParser.add_argument('dota_id', type=str)
profileParser.add_argument('hh_stone_id', type=str)
profileParser.add_argument('user_intro', type=str)

class ProfileAPI(Resource):
    def get(self):
        args = profileParser.parse_args()
        token = args['token']

        # verify token 
        if token is None:
            abort(400)
        email = verify_auth_token(token) 
        if email is None:
            abort(400)

        # load profile 
        profile =  Profile.objects(user_email=email)
        if profile.first() is None:
            return {}

        profile = profile.first()
        result = {}
        for key in profile:
            if key != "id":
                result[key] = profile[key]
        return result


    def post(self):
        args = profileParser.parse_args()
        token = args['token']

        # verify token 
        if token is None:
            abort(400)
        email = verify_auth_token(token) 
        if email is None:
            abort(400)

        school = args['school']
        lol_id = args['lol_id']
        dota_id = args['dota_id']
        hh_stone_id = args['hh_stone_id']
        user_intro = args['user_intro']

        teaminfo = TeamInfo.objects(user_email=email).first()
        if teaminfo is None:
            teaminfo = TeamInfo(user_email=email,lol_id=lol_id,dota_id=dota_id,hh_stone_id=hh_stone_id)
        else:
            teaminfo.lol_id = lol_id
            teaminfo.dota_id = dota_id
            teaminfo.hh_stone_id = hh_stone_id
        teaminfo.save()

        profile = Profile.objects(user_email=email)
        if profile.first() is None:
            profile = Profile(user_email=email, school=school, user_intro=user_intro, teaminfo=teaminfo)
            profile.save()
        else:
            profile = profile[0]
            profile.user_intro = user_intro
            profile.save()
       
        result = {}
        for key in profile:
            if key != "id":
                result[key] = profile[key]
        return result

class ProfileIconAPI(Resource):
    def post(self, token):
        # verify token 
        if token is None:
            abort(400)
        email = verify_auth_token(token) 
        if email is None:
            abort(400)

        uploaded_file = request.files['upload']
        filename = "_".join([email, uploaded_file.filename])

        conn = boto.connect_s3('AKIAJAQHGWIZDOAEQ65A', 'FpmnFv/jte9ral/iXHtL8cDUnuKXAgAqp9aXVQMI')
        bucket = conn.get_bucket('profile-icon')
        key = bucket.new_key(filename)
        key.set_contents_from_file(uploaded_file)

        profile = Profile.objects(user_email=email)
        if profile.first() is None:
            profile = Profile(user_email=email, profile_icon='https://s3-us-west-2.amazonaws.com/profile-icon/%s' %filename)
            profile.save()
        else:
            profile = profile[0]                
            profile.profile_icon = 'https://s3-us-west-2.amazonaws.com/profile-icon/%s' %filename
            profile.save()

        result = {}
        for key in profile:
            if key != "id":
                result[key] = profile[key]
        return result
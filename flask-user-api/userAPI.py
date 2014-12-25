from flask import abort
from flask.ext.restful import Resource, reqparse
from mongoengine.errors import NotUniqueError, ValidationError
from model.user import User
from model.redis import redis_store
import requests 

userParser = reqparse.RequestParser()
userParser.add_argument('email', type=str)
userParser.add_argument('username', type=str)
userParser.add_argument('password', type=str)

class UserAPI(Resource):
    def post(self):
        args = userParser.parse_args()
        email = args['email']
        username = args['username']
        password = args['password']
        if email is None or username is None or password is None:
            abort(400)    # missing arguments
        user = User(email=email, username=username)
        user.hash_password(password)
        try:
            user.save()
        except ValidationError, e:
            return {'status': 'error', 'message': e.message}  
        except NotUniqueError, e:
            return {'status': 'error', 'message': e.message}
        token = user.generate_auth_token(expiration=360000)
        redis_store.set(user.email, token)
        return ({'status': 'success', 'token': token}, 201)


class LoginAPI(Resource):
    def post(self):
        args = userParser.parse_args()
        email = args['email']
        password = args['password']
        if email is None or password is None:
            abort(400)

        try:    
            user = User.objects(email=email)[0]
        except:
            return {'status': 'error', 'message': 'username does not exist'}

        if not user or not user.verify_password(password):
            abort(400)
        token = user.generate_auth_token(expiration=360000)
        redis_store.set(user.email, token)
        return {'token': token}


fbUserParser = reqparse.RequestParser()
fbUserParser.add_argument('fbid', type=str)
fbUserParser.add_argument('fbtoken', type=str)
fbUserParser.add_argument('fbemail', type=str)

class FBUserAPI(Resource):
    def post(self):
        args = fbUserParser.parse_args()
        fb_id = args['fbid']
        fb_token = args['fbtoken']
        fb_email = args['fbemail']
        if fb_id is None or fb_token is None or fb_email is None:
            abort(400)    # missing arguments
        
        fbuser_info = requests.get('https://graph.facebook.com/me?access_token=%s' %fb_token).json()
        if not fbuser_info.get('id') or fb_id != fbuser_info['id']:
            abort(406)
        
        username = fbuser_info['name'] 
        user = User(email=fb_email, username=username, fb_id=fb_id)

        try:
            user.save()
        except:
            return {'status': 'error', 'message': 'FBname has already existed'}
        token = user.generate_auth_token(expiration=360000)
        redis_store.set(user.email, token)
        return ({'status': 'success', 'token': token}, 201)


class FBLoginAPI(Resource):
    def post(self):
        args = fbUserParser.parse_args()
        fb_id = args['fbid']
        fb_token = args['fbtoken']   
        if fb_id is None or fb_token is None:
           abort(400)

        fbuser_info = requests.get('https://graph.facebook.com/me?access_token=%s' %fb_token).json()
        if not fbuser_info.get('id') or fb_id != fbuser_info['id']:
            abort(406)

        username = fbuser_info['name']

        try:
            user = User.objects(username=username)[0]
        except:
            fb_email = args['fbemail']
            user = User(email=fb_email ,username=username, fb_id=fbuser_info['id'])
            user.save()

        token = user.generate_auth_token(expiration=360000)
        redis_store.set(user.email, token)
        return {'token': token}


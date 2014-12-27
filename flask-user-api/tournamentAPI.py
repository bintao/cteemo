from dateutil.parser import *
from dateutil.tz import *
from datetime import datetime
from flask import request, abort
from flask.ext.restful import Resource, reqparse
from model.redis import redis_store
from model.tournament import Tournament
import boto
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)

SECRET_KEY = 'flask is cool'
# UIUC time is the standard
tzoffset = {"CST":0, "PST":7200, "MST":3600, "EST":-3600,"CDT":0,"PDT":7200,"MDT":3600,"EDT":-3600}

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

#def verify_school(school):


profileParser = reqparse.RequestParser()
profileParser.add_argument('token', type=str)
profileParser.add_argument('isSchool', type=int) # if 1 then it is a school tournament
profileParser.add_argument('school', type=str)
profileParser.add_argument('tournament_name', type=str)
profileParser.add_argument('start_time', type=str)
profileParser.add_argument('end_time', type=str)

class TournamentAPI(Resource):
    def get(self):
        args = profileParser.parse_args()
        token = args['token']
        # verify token 
        #if token is None or verify_auth_token(token) == None:
        #    abort(400)
        # load tournament and return a list of tournaments (dicts)
        ret = list()
        for tournaments in Tournament.objects:
            result = dict()
            for key in tournaments:
                if key != 'id':
                    result[key] = str(tournaments[key])
            ret.append(result)
        return ret

    def post(self):
        args = profileParser.parse_args()
        token = args['token']
        # verify token 
        #if token is None or verify_auth_token(token) == None:
        #    abort(400)
        # create a new tournament
        tournament_Name = args['tournament_name']
        try:
            start_Time = parse(args['start_time'],tzinfos=tzoffset)
        except AttributeError, e:
            return {'status': 'error', 'message': e.message}  
        except ValueError, e:
            return {'status': 'error', 'message': e.message}
        try:
            end_Time = parse(args['end_time'],tzinfos=tzoffset)
        except AttributeError, e:
            return {'status': 'error', 'message': e.message}  
        except ValueError, e:
            return {'status': 'error', 'message': e.message}
        try:
            assert str(end_Time.tzinfo) == str(start_Time.tzinfo)
        except:
            return {'status': 'error', 'message': 'time zone does not match'}
        time_zone = end_Time.tzinfo.tzname(0)
        tournament = Tournament(time_zone=time_zone,start_time=start_Time,end_time=end_Time,tournament_name=tournament_Name)
        if args['isSchool'] == 1:
            school = args['school']
            tournament.school = school
            if school is None:
                abort(400)
        tournament.save()
        result = {}
        for key in tournament:
            if key != "id":
                result[key] = str(tournament[key])
        return result

from datetime import datetime
from flask import request, abort
from flask.ext.restful import Resource, reqparse
from model.redis import redis_store
from model.team import Team
from model.profile import Profile
from model.user import User
import boto
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)

SECRET_KEY = 'flask is cool'

profileParser = reqparse.RequestParser()
profileParser.add_argument('token', type=str)
profileParser.add_argument('isSchool', type=int) # if 1 then it is a school team
profileParser.add_argument('school', type=str)
profileParser.add_argument('team_name', type=str)

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

class createTeamAPI(Resource):
    def get(self):
        pass
        
    def post(self):
        args = profileParser.parse_args()
        token = args['token']
        email = verify_auth_token(token)
        # verify token 
        if token is None or email == None:
            abort(400)
        # query user's profile
        isSchool = args['isSchool']
        team_name = args['team_name']
        profile = Profile.objects(user_email=email)
        profile = profile.first()
        if profile is not None:
            if profile.team is not None:
                return {'status': 'error', 'message': 'Already has a team'}
        else:
            profile = Profile(user_email=email,team=team_name)
            profile.save()
        team = Team.objects(team_name=team_name).first()
        if team is None:
            team = Team(isSchool=isSchool, team_name=team_name)
        else:
            team.team_name = team_name
            team.isSchool = isSchool
        if isSchool == 1:
                school = args['school']
                team.school = school
        team.create_time = datetime.now()
        team.owner_email = email
        team.owner = profile.username
        team.team_members[team.owner] = email
        try:
            team.save()
        except ValidationError, e:
            return {'status': 'error', 'message': e.message}  
        except NotUniqueError, e:
            return {'status': 'error', 'message': e.message}
        result = {}
        for key in team:
            if key != "id":
                result[key] = str(team[key])
        return result

    def delete(self):
        args = profileParser.parse_args()
        token = args['token']
        email = verify_auth_token(token)
        # verify token 
        if token is None or email is None:
            abort(400)
        # query user's profile
        profile = Profile.objects(user_email=email)
        profile = profile.first()
        if profile is None:
            abort(400)
        team = Team.objects(team_name=profile.team)
        team = team.first()
        if team is not None:
            if team.owner_email != email:
                abort(400)
            for keys in team.team_members:
                profile = Profile.objects(user_email=team_members[keys])
                profile = profile.first()
                profile.team = None
            team.delete()
        profile.team = None
        profile.save()
        return {'status': 'success'}

class joinTeamAPI(Resource):
    def get(self):
        return

    def post(self):
        args = profileParser.parse_args()
        token = args['token']
        email = verify_auth_token(token)
        # verify token 
        if token is None or email == None:
            abort(400)
        profile = Profile.objects(user_email=email)
        profile = profile.first()
        if profile.team is not None:
            return {'status':'Already has team'}
        #isSchool = args['isSchool']
        #school = args['school']
        team_name = args['team_name']
        team = Team.objects(team_name=team_name)
        # Team not found
        if team.first() is None:
            return {'status':'Team not found'}
        team = team.first()
        if len(team.team_members) > 7:
            return {'status':'Team is full'}
        profile.team = team.team_name
        profile.save()
        team.team_members[User.objects(email=email).first().username] = email
        team.save()
        return {'status':'success'}

    def delete(self):
        return

class TeamIconAPI(Resource):
    def post(self, team_name):
        args = profileParser.parse_args()
        token = args['token']
        email = verify_auth_token(token)
        # verify token 
        if token is None or email == None:
            abort(400)
        
        team = Team.objects(team_name=team_name)
        team = team.first()

        if team.owner_email != email:
            abort(400)

        uploaded_file = request.files['upload']
        filename = "_".join([team_name, uploaded_file.filename])

        conn = boto.connect_s3('AKIAI6Y5TYNOTCIHK63Q', 'mmIpQx6mX/oFjZC6snQ7anO0yTOhEbpqPf2pcr0E')
        bucket = conn.get_bucket('team-icon')
        key = bucket.new_key(filename)
        key.set_contents_from_file(uploaded_file)

        if team is None:
            team = Team(team_name=team_name, team_icon='https://s3-us-west-2.amazonaws.com/team-icon/%s' %filename)
        else:
            team.team_icon = 'https://s3-us-west-2.amazonaws.com/team-icon/%s' %filename
        
        team.save()

        result = {}
        for key in team:
            if key != "id":
                result[key] = str(team[key])
        return result
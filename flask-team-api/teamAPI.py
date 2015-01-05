from datetime import datetime
from flask import request, abort
from flask.ext.restful import Resource, reqparse
from mongoengine.errors import NotUniqueError, ValidationError
from auth import verify_auth_token
from serialize import serialize
from model.team import Team
from model.profile import Profile
from model.user import User
from model.teaminfo import TeamInfo
import boto

profileParser = reqparse.RequestParser()
profileParser.add_argument('token', type=str)
profileParser.add_argument('isSchool', type=str) # if 1 then it is a school team
profileParser.add_argument('school', type=str)
profileParser.add_argument('team_name', type=str)
profileParser.add_argument('team_intro', type=str)
profileParser.add_argument('username', type=str)
profileParser.add_argument('user_email', type=str)

class myTeamAPI(Resource):
    def get(self):
        args = profileParser.parse_args()
        token = args['token']
        email = verify_auth_token(token)
        # verify token 
        if token is None or email == None:
            abort(400)

        teaminfo = TeamInfo.objects(user_email=email)
        teaminfo = teaminfo.first()

        if teaminfo is None:
            return None

        return serialize(teaminfo.lol_team)

    def delete(self):
        args = profileParser.parse_args()
        token = args['token']
        email = verify_auth_token(token)
        # verify token 
        if token is None or email == None:
            abort(400)

        teaminfo = TeamInfo.objects(user_email=email)
        teaminfo = teaminfo.first()

        if teaminfo is None:
            abort(400)

        team = teaminfo.lol_team
        # No team joined should not have acess to this url
        if team is None:
            abort(400)
        # Only captain can kick
        if team.owner.user_email != email:
            abort(400)

        user_email = args['user_email']
        if team.owner.user_email == user_email:
            return {'error' : 'Please assign new captain'}

        profile = Profile.objects(user_email=user_email).first()
        
        team.update(pull__team_members=profile)
        
        team.save()

        return serialize

    def post(self):
        args = profileParser.parse_args()
        token = args['token']
        email = verify_auth_token(token)
        # verify token 
        if token is None or email == None:
            abort(400)

        profile = Profile.objects(user_email=email)
        profile = profile.first() # The first of our query

        team = Team.objects(team_name=profile.team) # get the team already joined
        team = team.first()

        if team is None:
            return None
        if len(team.team_members) > 6:
            return {'Team is full'}
        if team.owner_email != email:
            abort(400)

        email = args['user_email']
        profile = Profile.objects(user_email=email)
        profile = profile.first()
        if profile is None:
            return {'error' : 'User not found'}
        if profile.team is not None:
            return {'error' : 'Person already joined a team'}
        if team.team_members.has_key(profile.username):
            return {'error' : 'Change username please'}
        profile.team = team.team_name
        team.team_members[profile.username] = email
        try:
            profile.save()
            team.save()
        except ValidationError, e:
            return {'status': 'error', 'message': e.message}  
        except NotUniqueError, e:
            return {'status': 'error', 'message': e.message}

        result = dict()
        for key in team:
            if key != 'id' and key != 'team_members':
                result[key] = str(team[key])
        members,icons = list(),list()
        for key in team.team_members:
            members.append(key)
            icons.append(Profile.objects(user_email=team.team_members[key]).first().profile_icon)
        result['team_members'] = members
        result['icons'] = icons
        return result

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
        isSchool = (args['isSchool'] == 'true')
        team_name = args['team_name']
        team_intro = args['team_intro']

        profile = Profile.objects(user_email=email)
        profile = profile.first()
        teaminfo = TeamInfo.objects(user_email=email)
        teaminfo = teaminfo.first()
        
        team = Team.objects(team_name=team_name).first()
        if team is None:
            team = Team(isSchool=isSchool, team_name=team_name)
            if teaminfo is not None:
                if teaminfo.lol_team is not None:
                    return {'error' : 'Already has a team'}
                teaminfo.lol_team = team
            else:    
                teaminfo = TeamInfo(lol_team=team,user_email=email)
        else:
            return {'error':'Team name exists'}
        if isSchool == True:
                school = args['school']
                team.school = school
        team.team_intro = team_intro
        team.create_time = datetime.now()
        team.owner = profile
        team.team_members = [profile]
        team.total_games = 0
        team.won_games = 0
        team.total_prize = 0
        try:
            team.save()
            teaminfo.save()
        except ValidationError, e:
            return {'status': 'error', 'message': e.message}  
        except NotUniqueError, e:
            return {'status': 'error', 'message': e.message}
        return serialize(team)

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
                profile = Profile.objects(user_email=team.team_members[keys])
                profile = profile.first()
                profile.team = None
                profile.save()
        team.delete()
        return {'status': 'success'}

class joinTeamAPI(Resource):
    def get(self):
        args = profileParser.parse_args()
        token = args['token']
        email = verify_auth_token(token)
        # verify token 
        if token is None or email == None:
            abort(400)
        #get profile
        profile = Profile.objects(user_email=email)
        profile = profile.first()
        #get team
        team_name = args['team_name']
        team = Team.objects(team_name__icontains=team_name)
        if team is None:
            return {'status' : 'No team found'}
        # give users team name and team icon
        

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
        if len(team.team_members) > 6:
            return {'status':'Team is full'}
        if team.team_members.has_key(profile.username):
            return {'status':'Same username in one team is not allowed'}
        profile.team = team.team_name
        profile.save()
        team.team_members[profile.username] = email
        team.save()
        return {'status':'success'}

    def delete(self):
        args = profileParser.parse_args()
        token = args['token']
        email = verify_auth_token(token)
        # verify token 
        if token is None or email == None:
            abort(400)
        profile = Profile.objects(user_email=email)
        profile = profile.first()

        if profile.team is None:
            abort(400)

        team = Team.objects(team_name=profile.team)
        team = team.first()
        if team.owner_email == profile.user_email:
            return {'error' : 'Please assgin new captain'}
        profile.team = None
        profile.save()


        if team is not None:
            try:
                del team.team_members[profile.username]
            except:
                pass
            team.save()

        return {'status' : 'success'}

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

        conn = boto.connect_s3('AKIAJAQHGWIZDOAEQ65A', 'FpmnFv/jte9ral/iXHtL8cDUnuKXAgAqp9aXVQMI')
        bucket = conn.get_bucket('team-icon')
        key = bucket.new_key(filename)
        key.set_contents_from_file(uploaded_file)

        if team is None:
            team = Team(team_name=team_name, team_icon='https://s3-us-west-2.amazonaws.com/team-icon/%s' %filename)
        else:
            #if team.team_icon is not None:
            #    old_icon = team.team_icon.split('/')[4]
            #    bucket.delete_key(old_icon)  
            team.team_icon = 'https://s3-us-west-2.amazonaws.com/team-icon/%s' %filename
        
        team.save()

        result = {}
        for key in team:
            if key != "id":
                result[key] = str(team[key])
        return result
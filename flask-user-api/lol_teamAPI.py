from flask import request, abort
from flask.ext.restful import Resource, reqparse
from mongoengine.errors import NotUniqueError, ValidationError
from model.profile import Profile
from model.lol_team import LOLTeam
from userAuth import auth_required
from serialize import team_serialize
import boto


teamParser = reqparse.RequestParser()
teamParser.add_argument('teamIntro', type=str)
teamParser.add_argument('teamName', type=str)
teamParser.add_argument('userID', type=str) # This userID is the operand

class lolTeamAPI(Resource):
	@auth_required
	def post(self, user_id):
		profile = Profile.objects(user=user_id).first()
		if profile.LOLTeam is not None:
			return {'status' : 'Only one team per game allowed'}
		args = teamParser.parse_args()
		teamName = args['teamName']
		teamIntro = args['teamIntro']
		team = LOLTeam(teamName=teamName,teamIntro=teamIntro,captain=profile)
		try:
			team.save()
		except ValidationError, e:
			return {'status': 'error', 'message': e.message}  
		except NotUniqueError, e:
			return {'status': 'error', 'message': e.message}
		profile.LOLTeam = team
		profile.save()
		return team_serialize(team)

	@auth_required
	def get(self, user_id):
		profile = Profile.objects(user=user_id).first()
		if profile.LOLTeam is None:
			return {'status' : 'Not joined any team yet'}
		team = profile.LOLTeam
		return team_serialize(team)

	@auth_required
	def delete(self, user_id):
		profile = Profile.objects(user=user_id).first()
		if profile.LOLTeam is None:
			return {'status' : 'Not joined any team yet'}
		team = profile.LOLTeam
		if team.captain != profile:
			abort(400)
		# update members' profiles
		for member in team.members:
			member.LOLTeam = None
			member.save()

		profile.LOLTeam = None
		profile.save()
		team.delete()
		return {'status' : 'success'}
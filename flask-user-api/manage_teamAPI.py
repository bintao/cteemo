from flask import request, abort
from flask.ext.restful import Resource, reqparse
from mongoengine.errors import NotUniqueError, ValidationError
from model.profile import Profile
from model.lol_team import LOLTeam
from userAuth import auth_required
from serialize import team_serialize
import boto


teamParser = reqparse.RequestParser()
teamParser.add_argument('teamName', type=str)
teamParser.add_argument('userID', type=str) # This userID is the operand

class manage_TeamAPI(Resource):
	@auth_required
	def post(self, user_id):
		args = teamParser.parse_args()
		userID = args['userID']
		profile = Profile.objects(user=user_id).first()
		team = profile.LOLTeam
		# avoid illegal operation
		if team is None:
			abort(400)
		if team.captain != profile:
			abort(400)
		# query the player u want to invite
		profile = Profile.objects(user=userID).first()
		if profile is None:
			return {'status' : 'user not found'}
		try:
			assert len(team.members) < 6
			team.members.append(profile)
		except:
			return {'status' : 'team is full'}
		profile.LOLTeam = team
		team.save()
		profile.save()

		return team_serialize(team)

	@auth_required
	def delete(self, user_id):
		args = teamParser.parse_args()
		userID = args['userID']
		profile = Profile.objects(user=user_id).first()
		team = profile.LOLTeam
		# avoid illegal operation
		if team is None:
			abort(400)
		if team.captain != profile:
			abort(400)
		# query the player u want to kick
		try:
			member = Profile.objects(user=userID).first()
			member.LOLTeam = None
			team.update(pull__members=member,safe=True)
		except:
			return {'error' : 'member not found'}
		team.save()
		member.save()
		
		return {'status' : 'success'}
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
		teamName = args['teamName']
		userID = args['userID']
		profile = Profile.objects(user=user_id).first()
		team = LOLTeam.objects(teamName=teamName).first()
		# avoid illegal operation
		if team is None:
			abort(400)
		if team.captain != profile:
			abort(400)
		# query the player u want to invite
		profile = Profile.objects(user=userID).first()
		if profile is None:
			return {'status' : 'user not found'}
		if len(team.members) >= 6:
			return {'status' : 'team is full'}
		team.members.append(profile)
		profile.LOLTeam = team
		team.save()
		profile.save()

		return team_serialize(team)

	@auth_required
	def delete(self, user_id):
		args = teamParser.parse_args()
		teamName = args['teamName']
		userID = args['userID']
		profile = Profile.objects(user=user_id).first()
		team = LOLTeam.objects(teamName=teamName).first()
		# avoid illegal operation
		if team is None:
			abort(400)
		if team.captain != profile:
			abort(400)
		# query the player u want to kick
		for member in team.members:
			if member.user == userID:
				break
		if member.user != userID:
			return {'status' : 'user not found'}
		
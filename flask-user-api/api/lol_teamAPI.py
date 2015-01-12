from flask import request, abort
from flask.ext.restful import Resource, reqparse
from mongoengine.errors import NotUniqueError, ValidationError
from model.profile import Profile
from model.lol_team import LOLTeam
from util.userAuth import auth_required
from util.serialize import team_serialize, team_search_serialize
import boto
import os

teamParser = reqparse.RequestParser()
teamParser.add_argument('teamIntro', type=str)
teamParser.add_argument('teamName', type=str)
teamParser.add_argument('profileID', type=str) # This profileID is the operand
teamParser.add_argument('isSchool', type=bool) # use boolean
teamParser.add_argument('school', type=str)
teamParser.add_argument('page', type=int)

class LolTeamAPI(Resource):
	@auth_required
	def post(self, user_id):
		profile = Profile.objects(user=user_id).first()
		if profile.LOLTeam is not None:
			return {'status' : 'Only one team per game allowed'}
		args = teamParser.parse_args()
		teamName = args['teamName']
		teamIntro = args['teamIntro']
		isSchool = args['isSchool']
		school = args['school']
		team = LOLTeam(teamName=teamName,teamIntro=teamIntro,captain=profile,isSchool=isSchool)
		if isSchool is True:
			team.school = school
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
	def delete(self, user_id):
		profile = Profile.objects(user=user_id).first()
		if profile.LOLTeam is None:
			return {'status' : 'Not joined any team yet'}
		team = profile.LOLTeam
		if team.captain != profile:
			abort(401)
		# update members' profiles
		for member in team.members:
			member.LOLTeam = None
			member.save()

		profile.LOLTeam = None
		profile.save()
		team.delete()
		return {'status' : 'success'}

class MylolTeamAPI(Resource):
	@auth_required
	def get(self, user_id):
		profile = Profile.objects(user=user_id).first()
		if profile.LOLTeam is None:
			return {'status' : 'Not joined any team yet'}
		team = profile.LOLTeam
		return team_serialize(team)

	@auth_required
	def post(self, user_id):
		args = teamParser.parse_args()
		profile = Profile.objects(user=user_id).first()
		if profile.LOLTeam is not None:
			return {'status' : 'Already joined a team'}

		teamName = args['teamName']
		team = LOLTeam.objects(teamName=teamName).first()
		if team is None:
			return {'status' : 'team not found'}
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
		profile = Profile.objects(user=user_id).first()
		if profile.LOLTeam is None:
			abort(400)

		team = profile.LOLTeam
		try:
			team.update(pull__members=profile,safe=True)
		except:
			return {'status' : 'captain is not allowed to quit'}
		profile.LOLTeam = None
		profile.save()
		team.save()

		return {'status' : 'success'}

class ManagelolTeamAPI(Resource):
	@auth_required
	def post(self, user_id):
		args = teamParser.parse_args()
		profileID = args['profileID']
		profile = Profile.objects(user=user_id).first()
		team = profile.LOLTeam
		# avoid illegal operation
		if team is None:
			abort(400)
		if team.captain != profile:
			abort(401)
		# query the player u want to invite
		profile = Profile.objects(id=profileID).first()
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
		profileID = args['profileID']
		profile = Profile.objects(user=user_id).first()
		team = profile.LOLTeam
		# avoid illegal operation
		if team is None:
			abort(400)
		if team.captain != profile:
			abort(401)
		# query the player u want to kick
		try:
			member = Profile.objects(id=profileID).first()
			member.LOLTeam = None
			team.update(pull__members=member,safe=True)
		except:
			return {'error' : 'member not found'}
		team.save()
		member.save()
		
		return {'status' : 'success'}

class LolTeamIconAPI(Resource):
	@auth_required
	def post(self, user_id):
		profile = Profile.objects(user=user_id).first()
		team = profile.LOLTeam
		# prevent bad request
		if team.captain != profile:
			abort(401)
		uploaded_file = request.files['upload']
		filename = "_".join([user_id, uploaded_file.filename])
		conn = boto.connect_s3('AKIAJAQHGWIZDOAEQ65A', 'FpmnFv/jte9ral/iXHtL8cDUnuKXAgAqp9aXVQMI')
		bucket = conn.get_bucket('team-icon')
		key = bucket.new_key(filename)
		key.set_contents_from_file(uploaded_file)
		team.teamIcon = 'https://s3-us-west-2.amazonaws.com/team-icon/%s' %filename
		team.save()
		return team_serialize(team)
        
class SearchlolTeamAPI(Resource):
	@auth_required
	def get(self, user_id):
		args = teamParser.parse_args()
		teamName = args['teamName']
		school = args['school']
		page = args['page']
		if teamName is None and school is None:
			abort(400)
		teams = LOLTeam.objects.only('teamName','school','captain','teamIcon')
		if teamName is not None:
			teams = teams.filter(teamName__icontains=teamName)
		if school is not None:
			teams = teams.filter(school=school)
		return team_search_serialize(teams)

class ViewlolTeamAPI(Resource):
	def get(self, teamID):
		team = LOLTeam.objects(id=teamID).first()
		if team is None:
			abort(400)

		return team_serialize(team)

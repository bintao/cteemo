#
# Copyright (c) 2015 by Xiaofo Yu.  All Rights Reserved.
#
from flask import request, abort
from flask.ext.restful import Resource, reqparse
from mongoengine.errors import NotUniqueError, ValidationError
from model.profile import Profile
from model.lol_team import LOLTeam
from model.request import Request
from util.userAuth import auth_required
from util.serialize import team_serialize, team_search_serialize, requests_list_serialize
from util.exception import InvalidUsage
import boto
import os

teamParser = reqparse.RequestParser()
teamParser.add_argument('teamIntro', type=str)
teamParser.add_argument('teamName', type=str)
teamParser.add_argument('profileID', type=int) # This profileID is the operand
teamParser.add_argument('isSchool', type=bool) # use boolean
teamParser.add_argument('school', type=str)
teamParser.add_argument('page', type=int)

class LolTeamAPI(Resource):
	def options(self):
		pass
		
	@auth_required
	def post(self, user_id):
		profile = Profile.objects(user=user_id).first()
		if profile.LOLTeam is not None:
			raise InvalidUsage('Only one team per game allowed')
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
			raise InvalidUsage(e.message)  
		except NotUniqueError, e:
			raise InvalidUsage(e.message)
		profile.LOLTeam = team
		profile.save()
		return team_serialize(team)

	@auth_required
	def delete(self, user_id):
		profile = Profile.objects(user=user_id).first()
		if profile.LOLTeam is None:
			raise InvalidUsage('Not joined any team yet')
		team = profile.LOLTeam
		if team.captain != profile:
			raise InvalidUsage('Unauthorized',401)
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
			raise InvalidUsage('Not joined any team yet')
		team = profile.LOLTeam
		return team_serialize(team)

	@auth_required
	def post(self, user_id):
		args = teamParser.parse_args()
		profile = Profile.objects(user=user_id).first()
		if profile.LOLTeam is not None:
			raise InvalidUsage('Already joined a team')

		teamName = args['teamName']
		team = LOLTeam.objects(teamName=teamName).first()

		if team is None:
			raise InvalidUsage('Team not found',404)

		captain = team.captain
		request = Request.objects(user=captain.user,type='join').only('requests_list').first()
		if request is None:
			request = Request(user=captain.user,type='join')
			request.save()
		request.update(add_to_set__requests_list=profile)

		return {'status' : 'success'}

	@auth_required
	def delete(self, user_id):
		profile = Profile.objects(user=user_id).first()
		if profile.LOLTeam is None:
			raise InvalidUsage('Not joined any team yet')

		team = profile.LOLTeam
		if team.captain == profile:
			raise InvalidUsage('Captain is not allowed to quit')
	
		team.update(pull__members=profile)

		profile.LOLTeam = None
		profile.save()
		team.save()

		return {'status' : 'success'}

class ManagelolTeamAPI(Resource):
	@auth_required
	def post(self, user_id):
		args = teamParser.parse_args()
		profileID = args['profileID']
		teamIntro = args['teamIntro']
	
		profile = Profile.objects(user=user_id).first()
		team = profile.LOLTeam
		if profileID is None and teamIntro is not None:
			team.teamIntro = teamIntro
			team.save()
			return {'status' : 'success'}
		# avoid illegal operation
		if team is None:
			abort(400)
		if team.captain != profile:
			raise InvalidUsage('Unauthorized',401)
		# query the player u want to invite
		profile = Profile.objects(id=profileID).first()
		if profile is None:
			raise InvalidUsage('Member not found',404)
		try:
			assert len(team.members) < 6
		except:
			raise InvalidUsage('Team is full',403)
		request = Request.objects(user=profile.user,type='invite').only('requests_list').first()
		if request is None:
			request = Request(user=profile.user,type='invite')
			request.save()
		request.update(add_to_set__requests_list=team.captain)

		return {'status' : 'success'}

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
			raise InvalidUsage('Unauthorized',401)
		# query the player u want to kick
		member = Profile.objects(id=profileID).first()
		if member == profile:
			raise InvalidUsage('Cannot kick yourself')

		team.update(pull__members=member)
		
		member.LOLTeam = None
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
			raise InvalidUsage('Unauthorized',401)
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
			raise InvalidUsage('No argument provided')
		teams = LOLTeam.objects.only('teamName','school','captain','teamIcon')
		if teamName is not None:
			teams = teams.filter(teamName__icontains=teamName)
		if school is not None:
			teams = teams.filter(school=school)
		if page is None:
			page = 0
		return team_search_serialize(teams[10*page:10*(page+1)])

class ViewlolTeamAPI(Resource):
	def get(self, teamID):
		team = LOLTeam.objects(id=teamID).first()
		if team is None:
			raise InvalidUsage('Team not found',404)

		return team_serialize(team)

class InviteTeamRequestAPI(Resource):
	@auth_required
	def get(self, user_id):
		request = Request.objects(user=user_id,type='invite').only('requests_list').first()
		if request is None:
			return {}

		return requests_list_serialize(request.requests_list)

	@auth_required
	def post(self, user_id):
		args = teamParser.parse_args()
		profileID = args['profileID']

		profile = Profile.objects(id=profileID).first()
		request = Request.objects(user=user_id,type='invite').only('requests_list').first()
		if request is None or profile is None:
			raise InvalidUsage('Request is illegal')

		team = profile.LOLTeam

		success = request.update(pull__requests_list=profile)
		if success is 0 or team is None or team.captain != profile:
			raise InvalidUsage('Request is illegal') 

		profile = Profile.objects(user=user_id).first()
		try:
			assert len(team.members) < 6
			team.members.append(profile)
		except:
			raise InvalidUsage('Team is full', 403)
		profile.LOLTeam = team

		team.save()
		profile.save()

		return team_serialize(team)

	@auth_required
	def delete(self, user_id):
		args = teamParser.parse_args()
		profileID = args['profileID']

		request = Request.objects(user=user_id, type='invite').only('requests_list').first()
		if request is None:
			raise InvalidUsage('Request does not exist')

		request.update(pull__requests_list=profileID)
		return {'status' : 'success'}

class JoinTeamRequestAPI(Resource):
	@auth_required
	def get(self, user_id):
		request = Request.objects(user=user_id,type='join').only('requests_list').first()
		if request is None:
			return {}

		return requests_list_serialize(request.requests_list)

	@auth_required
	def post(self, user_id):
		args = teamParser.parse_args()
		profileID = args['profileID']

		request = Request.objects(user=user_id, type='join').only('requests_list').first()
		if request is None:
			raise InvalidUsage('Request does not exist')

		captain = Profile.objects(user=user_id).first()
		team = captain.LOLTeam
		if team is None:
			raise InvalidUsage('Request is illegal')

		if team.captain != captain:
			raise InvalidUsage('Unauthorized',401)
		# query the player u want to invite
		profile = Profile.objects(id=profileID).first()
		success = request.update(pull__requests_list=profile)
		if success is 0:
			raise InvalidUsage('Request not found')
			
		if profile is None:
			raise InvalidUsage('Member not found',404)
		try:
			assert len(team.members) < 6
			team.members.append(profile)
		except:
			raise InvalidUsage('Team is full',403)
		profile.LOLTeam = team
		team.save()
		profile.save()

		return team_serialize(team)

	@auth_required
	def delete(self, user_id):
		args = teamParser.parse_args()
		profileID = args['profileID']

		request = Request.objects(user=user_id, type='join').only('requests_list').first()
		if request is None:
			raise InvalidUsage('Request does not exist')

		request.update(pull__requests_list=profileID)
		return {'status' : 'success'}
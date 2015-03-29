from __future__ import division
from flask import request, abort
from flask.ext.restful import Resource, reqparse
from mongoengine.errors import NotUniqueError, ValidationError
from mongoengine import Q
from model.profile import Profile
from model.team import Team
from model.tournament import Tournament
from model.rule import Rule
from model.round import Round
from model.match_history import MatchHistory
from model.challonge import Challonge
from util.userAuth import auth_required
from util.serialize import tournament_serialize, tournament_search_serialize, match_serialize
from util.exception import InvalidUsage
from functions.game import update
from lol.code_generator import lolTournamentCode
from challonge import api
from api.rongcloudAPI import rongcloudCreateGroup,rongcloudJoinGroup,rongcloudLeaveGroup,rongcloudDismissGroup
import math
import boto
import challonge

challonge.set_credentials("bintao", "OzVqaaqFdjiuTGPbbeQfvpgHxnIcquz6yh5LSwep")

profileParser = reqparse.RequestParser()
profileParser.add_argument('tournamentName', type=str)
profileParser.add_argument('tournamentUrl', type=str)
profileParser.add_argument('tournamentType', type=str)
profileParser.add_argument('tournamentId', type=int)
profileParser.add_argument('participantId', type=int)
profileParser.add_argument('matchId', type=int)

class ChallongeAPI(Resource):
	@auth_required
	def post(self, user_id):
		args = profileParser.parse_args()
		tournamentName = args['tournamentName']
		tournamentUrl = args['tournamentUrl']
		tournamentType = args['tournamentType']

		tournament = Challonge(tournamentName=tournamentName)
		profile = Profile.objects(user=user_id).first()

		if profile is None:
			raise InvalidUsage("No profile found")

		try:
			tournament.save()
		except:
			raise InvalidUsage("Tournament creation failed")

		tournament.profile = profile

		challonge = challonge.tournaments.create(tournamentName,tournamentUrl,tournamentType)
		tournament.id = challonge["id"]
		rongcloudCreateGroup(challonge["id"])

		return {'status': 'success'}

	@auth_required
	def get(self, user_id):
		args = profileParser.parse_args()
		tournamentId = args['tournamentId']

		return challonge.tournaments.show(tournamentId)

class ChallongeJoinAPI(Resource):
	@auth_required
	def post(self, user_id):
		args = profileParser.parse_args()
		tournamentId = args['tournamentId']

		profile = Profile.objects(user=user_id).first()
		if profile.LOLTeam is None:
			raise InvalidUsage()

		team = profile.LOLTeam
		if team.captain is not profile:
			raise InvalidUsage()

		challonge.participants.create(tournamentId,team.teamName)
		#rongcloudJoinGroup()
		return {'status' : 'success'}

	@auth_required
	def get(self, user_id):
		args = profileParser.parse_args()
		tournamentId = args['tournamentId']
		participantId = args['participantId']

		return challonge.matches.show(tournamentId,participantId)

class ChallongeResultAPI(Resource):
	@auth_required
	def get(self, user_id):
		args = profileParser.parse_args()
		tournamentId = args['tournamentId']
		tournamentName = args['tournamentName']
		matchId = args['matchId']
		code = lolTournamentCode(tournamentName,matchId,matchId,matchId,team_size)
		try:
			return { "tournament_code" : code.generate("Summoner's Rift","TOURNAMENT DRAFT",'ALL') }
		except:
			raise InvalidUsage('Tournament is not valid')

	@auth_required
	def post(self, user_id):
		args = profileParser.parse_args()
		profileParser.add_argument('tournamentId', type=int)
		profileParser.add_argument('participantId', type=int)
		profileParser.add_argument('matchId', type=int)

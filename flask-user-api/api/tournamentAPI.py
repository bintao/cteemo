from __future__ import division
from flask import request, abort
from flask.ext.restful import Resource, reqparse
from mongoengine.errors import NotUniqueError, ValidationError
from fractions import Fraction
from model.profile import Profile
from model.team import Team
from model.tournament import Tournament
from model.rule import Rule
from model.round import Round
from model.match_history import MatchHistory
from util.userAuth import auth_required
from util.serialize import tournament_serialize
import math

tournamentParser = reqparse.RequestParser()
tournamentParser.add_argument('tournamentName', type=str)
tournamentParser.add_argument('isSchool', type=str)
tournamentParser.add_argument('school', type=str)
tournamentParser.add_argument('descriptions', type=str)
tournamentParser.add_argument('entryFee', type=int)
tournamentParser.add_argument('size', type=int)
tournamentParser.add_argument('tournamentID', type=str)
tournamentParser.add_argument('totalPrize', type=int)
#tournamentParser.add_argument('groupStage', type=int)
tournamentParser.add_argument('teamSize', type=int)
tournamentParser.add_argument('elimination', type=int)
tournamentParser.add_argument('map', type=str)
tournamentParser.add_argument('pick', type=str)

class CreateTournamentAPI(Resource):
	@auth_required
	def post(self, user_id):
		args = tournamentParser.parse_args()
		tournamentName = args['tournamentName']
		isSchool = (args['isSchool'] == 'true')
		school = args['school']
		descriptions = args['descriptions']
		entryFee = args['entryFee']
		size = args['size']
		rounds = request.json['rounds']
		teamSize = args['teamSize']
		#group_stage = args['group_stage']
		map = args['map']
		pick = args['pick']
		roundNumber = int(math.log(size,2))
		totalPrize = args['totalPrize']
		profile = Profile.objects(user=user_id).first()

		if roundNumber != math.log(size,2):
			return {'status' : 'error', 'message' : 'size not acceptable'}

		tournament = Tournament(tournamentName=tournamentName,isSchool=isSchool,descriptions=descriptions,entryFee=entryFee,size=size,school=school,creator=profile,totalPrize=totalPrize)

		for i in range(roundNumber):
			round = Round(roundName=str(Fraction(2*(i+1)/size))+'Final', startTime=rounds[i]['startTime'], bestOfN=rounds[i]['bestOfN'])
			round.save()
			tournament.rounds.append(round)

		try:
			tournament.save()
		except ValidationError,e:
			return {'status' : 'error', 'message' : e.message}
		except NotUniqueError,e:
			return {'status' : 'error', 'message' : e.message}
		rule = Rule(team_size=teamSize, map=map, pick=pick, tournament=tournament)
		rule.save()

		return tournament_serialize(tournament)

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
tournamentParser.add_argument('entry_fee', type=int)
tournamentParser.add_argument('size', type=int)
tournamentParser.add_argument('tournamentID', type=str)
tournamentParser.add_argument('Total_Prize', type=int)
tournamentParser.add_argument('group_stage', type=int)
tournamentParser.add_argument('team_size', type=int)
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
		entry_fee = args['entry_fee']
		size = args['size']
		rounds = request.json['rounds']
		team_size = args['team_size']
		#group_stage = args['group_stage']
		map = args['map']
		pick = args['pick']
		roundNumber = int(math.log(size,2))
		Total_Prize = args['Total_Prize']
		profile = Profile.objects(user=user_id).first()

		if roundNumber != math.log(size,2):
			return {'status' : 'error', 'message' : 'size not acceptable'}

		tournament = Tournament(tournamentName=tournamentName,isSchool=isSchool,descriptions=descriptions,entry_fee=entry_fee,size=size,school=school,creator=profile,Total_Prize=Total_Prize)

		for i in range(roundNumber):
			round = Round(roundName=str(Fraction(2*(i+1)/size))+'Final', startTime=rounds[i]['startTime'], bestOfN=rounds[i]['bestOfN'])
			round.save()
			tournament.update(push__rounds=round,safe=True)

		try:
			tournament.save()
		except ValidationError,e:
			return {'status' : 'error', 'message' : e.message}
		except NotUniqueError,e:
			return {'status' : 'error', 'message' : e.message}
		rule = Rule(team_size=team_size, map=map, pick=pick, tournament=tournament)
		rule.save()

		return tournament_serialize(tournament)

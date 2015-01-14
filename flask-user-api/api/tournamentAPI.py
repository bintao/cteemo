#
# Copyright (c) 2015 by Xiaofo Yu.  All Rights Reserved.
#
from __future__ import division
from flask import request, abort
from flask.ext.restful import Resource, reqparse
from mongoengine.errors import NotUniqueError, ValidationError
from mongoengine import Q
from fractions import Fraction
from model.profile import Profile
from model.team import Team
from model.tournament import Tournament
from model.rule import Rule
from model.round import Round
from model.match_history import MatchHistory
from util.userAuth import auth_required
from util.serialize import tournament_serialize, tournament_search_serialize, match_serialize
from util.exception import InvalidUsage
from functions.game import update
import math

tournamentParser = reqparse.RequestParser()
tournamentParser.add_argument('tournamentName', type=str)
tournamentParser.add_argument('isSchool', type=bool)
tournamentParser.add_argument('school', type=str)
tournamentParser.add_argument('descriptions', type=str)
tournamentParser.add_argument('entryFee', type=int)
tournamentParser.add_argument('size', type=int)
tournamentParser.add_argument('tournamentID', type=int)
tournamentParser.add_argument('totalPrize', type=int)
#tournamentParser.add_argument('groupStage', type=int)
tournamentParser.add_argument('teamSize', type=int)
tournamentParser.add_argument('elimination', type=int)
tournamentParser.add_argument('map', type=str)
tournamentParser.add_argument('pick', type=str)
tournamentParser.add_argument('page', type=int)

class CreateTournamentAPI(Resource):
	def options(self):
		pass

	@auth_required
	def get(self, user_id):
		args = tournamentParser.parse_args()
		page = args['page']
		if page is None:
			page = 0

		profile = Profile.objects(user=user_id).first()
		tournaments = Tournament.objects(creator=profile).only('id','creator','tournamentName','createTime','isEnded','rounds')

		return tournament_search_serialize(tournaments[5*page:5*(page+1)])

	@auth_required
	def post(self, user_id):
		args = tournamentParser.parse_args()
		tournamentName = args['tournamentName']
		isSchool = args['isSchool']
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
			round = Round(roundName=str(Fraction(2*(i+1)/size))+' Final', startTime=rounds[i]['startTime'], bestOfN=rounds[i]['bestOfN'])
			round.save()
			tournament.rounds.append(round)
		for i in range(roundNumber-1):
			tournament.rounds[i].next = tournament.rounds[i+1]
		tournament.rounds[roundNumber-1].next = None


		try:
			tournament.save()
		except ValidationError,e:
			raise InvalidUsage(e.message)
		except NotUniqueError,e:
			raise InvalidUsage(e.message)
		rule = Rule(team_size=teamSize, map=map, pick=pick, tournament=tournament)
		rule.save()

		return tournament_serialize(tournament)

	@auth_required
	def delete(self, user_id):
		args = tournamentParser.parse_args()
		tournamentID = args['tournamentID']
		if tournamentID is None:
			raise InvalidUsage('Provide tournament id please')

		profile = Profile.objects(user=user_id).first()

		tournament = Tournament.objects(id=tournamentID).first()
		if tournament is None:
			raise InvalidUsage('Tournament not found',404)
		if tournament.creator != profile:
			raise InvalidUsage('Unauthorized',401)
		# More deletions need to be added
		rule = Rule.objects(tournament=tournament).first()
		if rule is not None:
			rule.delete()
		for round in tournament.rounds:
			round.delete()

		tournament.delete()
		return {'status':'success'}

class JoinTournamentAPI(Resource):
	def options(self):
		pass

	@auth_required
	def get(self, user_id):
		args = tournamentParser.parse_args()
		tournamentName = args['tournamentName']
		page = args['page']

		if tournamentName is None:
			tournamentName = ''
		if page is None:
			page = 0

		tournaments = Tournament.objects(tournamentName__icontains=tournamentName).only('id','creator','isEnded','createTime','rounds','isFull')

		tournaments = tournaments.filter(isEnded=False).order_by('-createTime')[10*page:10*(page+1)]

		return tournament_search_serialize(tournaments)
	# Join tournament
	@auth_required
	def post(self, user_id):
		args = tournamentParser.parse_args()
		tournamentID = args['tournamentID']

		tournament = Tournament.objects(id=tournamentID).first()
		if tournament is None:
			raise InvalidUsage('Tournament not found',404)
		if tournament.isEnded is True or tournament.isFull is True:
			raise InvalidUsage('Tournament full or has ended',403)

		profile = Profile.objects(user=user_id).first()
		team = profile.LOLTeam
		if team is None or team.captain != profile:
			raise InvalidUsage('Only captain can join tournament',401)
		if team.inGame is True:
			raise InvalidUsage('One team can only join one tournament at the same time',403)
		# join the first round
		round = tournament.rounds[0]
		round.checkInNumber += 1
		if round.checkInNumber == tournament.size:
			tournament.isFull = True
		tournament.save()

		if len(round.readyTeam) is 0:
			round.update(add_to_set__readyTeam=team)
		else:
			opponent = round.readyTeam[0]
			round.update(pull__readyTeam=opponent)
			match = MatchHistory(tournament=tournament,tournamentName=tournament.tournamentName,round=round,teams=[opponent,team])
			match.save()
			team.update(add_to_set__matchHistory=match)
			opponent.update(add_to_set__matchHistory=match)
			round.update(add_to_set__matches=match)

		return {'status' : 'success'}

matchParser = reqparse.RequestParser()
matchParser.add_argument('matchID', type=int)
matchParser.add_argument('win', type=bool)

class TournamentResultAPI(Resource):
	def options(self):
		pass

	@auth_required
	def get(self, user_id):
		profile = Profile.objects(user=user_id).first()
		team = profile.LOLTeam
		if team is None:
			raise InvalidUsage('Team not found',404)
		if team.captain != profile:
			raise InvalidUsage('Unauthorized',401)
		if team.inGame is False:
			raise InvalidUsage('Not in a tournament')

		match = team.matchHistory[-1]

		return match_serialize(match)

	@auth_required
	def post(self, user_id):
		profile = Profile.objects(user=user_id).first()
		team = profile.LOLTeam
		if team is None:
			raise InvalidUsage('Team not found',404)
		if team.captain != profile:
			raise InvalidUsage('Unauthorized',401)
		if team.inGame is False:
			raise InvalidUsage('Not in a tournament')

		args = matchParser.parse_args()
		matchID = args['matchID']
		win = args['win']

		match = MatchHistory.objects(id=matchID).first()
		if team == match.teams[0]:
			index = 0
		else:
			index = 1
		if win is True:
			match.scores[index] += 0.5
		else:
			match.scores[index-1] += 0.5

		round = match.round
		result = sum(match.scores)
		if result == round.bestOfN:
			if int(match.scores[0]) != match.scores[0]:
				return {'status' : 'Dispute needs screen shots verifying'}
			if match.scores[0] > match.scores[1]:
				win_team = match.teams[0]
				lose_team = match.teams[1]
			else:
				win_team = match.teams[1]
				lose_team = match.teams[0]

			lose_team.inGame = False
			lose_team.save()
			round = round.next
			if round is None:
				win_team.inGame = False
				win_team.save()
				return {'status' : 'Tournament Ended'}
			update(win_team,round)

		return {'status' : 'success', 'message' : 'Please get tournament code for the next game'}
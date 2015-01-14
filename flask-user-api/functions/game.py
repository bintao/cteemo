from __future__ import division
from flask import request, abort
from flask.ext.restful import Resource, reqparse
from mongoengine.errors import NotUniqueError, ValidationError
from model.profile import Profile
from model.team import Team
from model.tournament import Tournament
from model.rule import Rule
from model.round import Round
from model.match_history import MatchHistory
from util.userAuth import auth_required
from util.serialize import tournament_serialize, tournament_search_serialize, match_serialize
from util.exception import InvalidUsage
import math

def update(team,round):
	round.checkInNumber += 1
	tournament = round.tournament

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

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
from lol.code_generator import lolTournamentCode
import math
import boto
import challonge

challonge.set_credentials("your_challonge_username", "your_api_key")
from flask import request, abort
from flask.ext.restful import Resource, reqparse
from mongoengine.errors import NotUniqueError, ValidationError
from model.profile import Profile
from model.team import Team
from model.tournament import Tournament
from userAuth import auth_required
from serialize import tournament_serialize
import boto

tournamentParser = reqparse.RequestParser()
tournamentParser.add_argument('tournamentName', type=str)
tournamentParser.add_argument('isSchool', type=str)
tournamentParser.add_argument('school', type=str)
tournamentParser.add_argument('descriptions', type=str)
tournamentParser.add_argument('entry_fee', type=int)
tournamentParser.add_argument('size', type=int)
tournamentParser.add_argument('tournamentID', type=str)
tournamentParser.add_argument('Total_Prize', type=int)

class CreateTournamentAPI(Resource):
	@auth_required
	def post(self, user_id):
		args = tournamentParser.parse_args()
		tournamentName = args['tournamentName']
		isSchool = (args['isSchool'] == 'True')
		school = args['school']
		descriptions = args['descriptions']
		entry_fee = args['entry_fee']
		size = args['size']
		Total_Prize = args['Total_Prize']
		profile = Profile.objects(user=user_id).first()

		tournament = Tournament(tournamentName=tournamentName,isSchool=isSchool,descriptions=descriptions,entry_fee=entry_fee,size=size,school=school,creator=profile,Total_Prize=Total_Prize)

		try:
			tournament.save()
		except ValidationError,e:
			return {'status' : 'error', 'message' : e.message}
		except NotUniqueError,e:
			return {'status' : 'error', 'message' : e.message}

		return tournament_serialize(tournament)

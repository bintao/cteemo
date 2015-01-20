from flask import abort
from flask.ext.restful import Resource, reqparse
from model.player_post import PlayerPost
from model.team_post import TeamPost
from model.profile import Profile
from util.userAuth import auth_required
from util.serialize import posts_list_serialize
from util.exception import InvalidUsage

postParser = reqparse.RequestParser()
postParser.add_argument('content', type=str)
postParser.add_argument('page', type=int)


class PlayerPostAPI(Resource):

	@auth_required
	def get(self, user_id):
		args = postParser.parse_args()
		page = args['page']
		if page is None:
			page = 0

		posts = PlayerPost.objects().order_by('-date')[10 * page: 10 * (page + 1)]
		if posts is None:
			raise InvalidUsage('No post found',404)

		return posts_list_serialize(posts)

	@auth_required
	def post(self, user_id):
		args = postParser.parse_args()
		content = args['content']

		profile = Profile.objects(user=user_id).first()
		post = PlayerPost(user_profile=profile, content=content)
		post.save()

		return {'status': 'success'}

class TeamPostAPI(Resource):
	def options(self):
		pass

	@auth_required
	def get(self, user_id):
		args = postParser.parse_args()
		page = args['page']
		if page is None:
			page = 0

		posts = TeamPost.objects.order_by('-date')[10 * page: 10* (page + 1)]
		if posts is None:
			raise InvalidUsage('No post found',404)

		return posts_list_serialize(posts)

	@auth_required
	def post(self, user_id):
		args = postParser.parse_args()
		content = args['content']

		profile = Profile.objects(user=user_id).first()
		team = profile.LOLTeam

		if team is None:
			raise InvalidUsage('No team')

		if team.captain != profile:
			raise InvalidUsage('Unauthorized',401)

		post = TeamPost(user_profile=profile, team=team)
		post.save()

		return {'status' : 'success'}

from flask import Flask, request, abort
from flask.ext.restful import Resource, Api
from flask_mail import Mail
from model import db, bcrypt, redis_store
from api.userAPI import UserAPI, LoginAPI, FBUserAPI, FBLoginAPI, ActivateAPI
from api.profileAPI import ProfileAPI, ProfileIconAPI, FindProfileAPI, ViewProfileAPI
from api.lol_teamAPI import LolTeamAPI, MylolTeamAPI, ManagelolTeamAPI, LolTeamIconAPI, SearchlolTeamAPI, ViewlolTeamAPI
from api.friendsAPI import FriendsListAPI, FriendsRequestAPI
from api.passwordAPI import ChangePasswordAPI, ForgetPasswordAPI
from api.tournamentAPI import CreateTournamentAPI

app = Flask(__name__)
app.config.from_object('config') 

db.init_app(app)
bcrypt.init_app(app)
redis_store.init_app(app)
mail = Mail(app)

api = Api(app)

api.add_resource(UserAPI, '/create_user')
api.add_resource(LoginAPI, '/login')
api.add_resource(FBUserAPI, '/fb_create_user')
api.add_resource(FBLoginAPI, '/fb_login')
api.add_resource(ActivateAPI, '/activate_account')

api.add_resource(ChangePasswordAPI, '/change_password')
api.add_resource(ForgetPasswordAPI, '/forget_password')

api.add_resource(ProfileAPI, '/profile')
api.add_resource(ProfileIconAPI, '/upload_profile_icon')
api.add_resource(FindProfileAPI, '/search_profile')
api.add_resource(ViewProfileAPI, '/view_profile/<int:profileID>')

api.add_resource(FriendsListAPI, '/friends_list')
api.add_resource(FriendsRequestAPI, '/friends_request')

api.add_resource(LolTeamAPI, '/create_team/lol')
api.add_resource(MylolTeamAPI, '/my_team/lol')
api.add_resource(ManagelolTeamAPI, '/manage_team/lol')
api.add_resource(LolTeamIconAPI, '/upload_team_icon/lol')
api.add_resource(SearchlolTeamAPI, '/search_team/lol')
api.add_resource(ViewlolTeamAPI, '/view_team/lol/<int:teamID>')

api.add_resource(CreateTournamentAPI, '/create_tournament')

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')




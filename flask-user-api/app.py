from flask import Flask, request, abort
from flask.ext.restful import Resource, Api
from model import db, bcrypt, redis_store
from userAPI import UserAPI, LoginAPI, FBUserAPI, FBLoginAPI
from profileAPI import ProfileAPI, ProfileIconAPI
from lol_teamAPI import lolTeamAPI
from manage_teamAPI import manage_TeamAPI

app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {
    'db': 'testdb',
    'host': '54.149.235.253',
    'port': 27017,
    'username': 'dbuser',
    'password': 'cteemo2015'
}

app.config['REDIS_URL'] = "redis://:cteemo2015@54.149.235.253:6379/1"
app.config['SECRET_KEY'] = 'flask is cool' 

db.init_app(app)
bcrypt.init_app(app)
redis_store.init_app(app)

api = Api(app)

api.add_resource(UserAPI, '/create_user')
api.add_resource(LoginAPI, '/login')
api.add_resource(FBUserAPI, '/fb_create_user')
api.add_resource(FBLoginAPI, '/fb_login')

api.add_resource(ProfileAPI, '/profile')
api.add_resource(ProfileIconAPI, '/upload_profile_icon')

api.add_resource(lolTeamAPI, '/create_team/lol')
api.add_resource(manage_TeamAPI, '/manage_team')

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')




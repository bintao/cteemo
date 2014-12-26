from flask import Flask, request, abort
from flask.ext.restful import Resource, Api
from model.user import db, bcrypt
from model.redis import redis_store
from userAPI import UserAPI, LoginAPI, FBUserAPI, FBLoginAPI
from todoAPI import TodoAPI
from profileAPI import ProfileAPI, ProfileIconAPI

app = Flask(__name__)
#The following code should be modified on server
app.config['MONGODB_SETTINGS'] = {
    'db': 'testdb',
    'host': '54.149.235.253',
    'port': 27017,
    'username': 'dbuser',
    'password': 'cteemo2015'
}
app.config['REDIS_URL'] = "redis://:cteemo2015@54.149.235.253:6379/0"

db.init_app(app)
bcrypt.init_app(app)
redis_store.init_app(app)

api = Api(app)

api.add_resource(UserAPI, '/create_user')
api.add_resource(LoginAPI, '/login')
api.add_resource(FBUserAPI, '/fb_create_user')
api.add_resource(FBLoginAPI, '/fb_login')
api.add_resource(TodoAPI, '/todos')
api.add_resource(ProfileAPI, '/profile')
api.add_resource(ProfileIconAPI, '/upload_profile_icon/<string:token>')

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')




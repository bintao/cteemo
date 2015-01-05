from flask import Flask, request, abort
from flask.ext.restful import Resource, Api
from flask.ext.mongoengine import MongoEngine, MongoEngineSessionInterface
from flask.ext.bcrypt import Bcrypt
from model.user import db, bcrypt
from model.redis import redis_store
from teamAPI import createTeamAPI, joinTeamAPI, TeamIconAPI, myTeamAPI
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)

app = Flask(__name__)
#The following code should be modified on server
app.config['MONGODB_SETTINGS'] = {
    'db': 'testdb',
    'host': '54.149.235.253',
    'port': 27017,
    'username': 'dbuser',
    'password': 'cteemo2015'
}
app.config['REDIS_URL'] = "redis://:cteemo2015@54.149.235.253:6379/1"

db.init_app(app)
bcrypt.init_app(app)
redis_store.init_app(app)
app.session_interface = MongoEngineSessionInterface(db)

api = Api(app)

api.add_resource(createTeamAPI, '/create_team')
api.add_resource(joinTeamAPI, '/join_team')
api.add_resource(TeamIconAPI, '/upload_team_icon/<string:team_name>')
api.add_resource(myTeamAPI, '/my_team')

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')



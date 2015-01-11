from model import db
from datetime import datetime

class Team(db.Document):
	id = db.SequenceField(primary_key=True)
	createTime = db.DateTimeField(default=datetime.now())
	teamBalance = db.FloatField(default=0)
	teamName = db.StringField(required=True,unique=True)
	teamIntro = db.StringField(default='Captain left nothing here', max_length=200)
	captain = db.ReferenceField('Profile')
	isSchool = db.BooleanField()
	school = db.StringField()
	teamIcon = db.URLField()
	gameWon = db.IntField(default=0)
	gamePlayed = db.IntField(default=0)
	meta = {'allow_inheritance' : True,
			'abstract' : True,
			}
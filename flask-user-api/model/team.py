from model import db
from datetime import datetime

class Team(db.Document):
	createTime = db.DateTimeField(default=datetime.now())
	teamBalance = db.FloatField(default=0)
	teamName = db.StringField(required=True,unique=True)
	teamIntro = db.StringField(default='Captain left nothing here', max_length=200)
	captain = db.ReferenceField('Profile')
	meta = {'allow_inheritance' : True,
			}
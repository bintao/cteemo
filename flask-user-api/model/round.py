from model import db

class Round(db.Document):
	roundName = db.StringField(required=True)
	startTime = db.DateTimeField(required=True)
	bestOfN = db.IntField(default=3,max_value=7)
	readyTeam = db.ListField(db.ReferenceField('Team'))
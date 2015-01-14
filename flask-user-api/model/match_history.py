from model import db
from datetime import datetime

class MatchHistory(db.Document):
	matchTime = db.DateTimeField(default=datetime.now())
	scores = db.ListField()
	teams = db.ListField(db.ReferenceField('LOLTeam'))
	tournamentName = db.StringField()
	tournament = db.ReferenceField('Tournament')
	round = db.ReferenceField('Round')
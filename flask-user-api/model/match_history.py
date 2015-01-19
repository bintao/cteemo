from model import db
from datetime import datetime

class MatchHistory(db.Document):
	id = db.SequenceField(primary_key=True)
	matchTime = db.DateTimeField(default=datetime.now())
	scores = db.ListField(default=[0,0])
	teams = db.ListField(db.ReferenceField('LOLTeam'))
	tournamentName = db.StringField()
	tournament = db.ReferenceField('Tournament')
	round = db.ReferenceField('Round')
	screen_shots = db.ListField(db.URLField())
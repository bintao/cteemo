from model import db

class MatchHistory(db.Document):
	scores = db.ListField()
	teams = db.ListField(db.ReferenceField('Team'))
	tournamentName = db.StringField()
	tournament = db.ReferenceField('Tournament')
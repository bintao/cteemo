from model import db
from model.team import Team 

class HSTONETeam(Team):
	members = db.ListField(db.ReferenceField('Profile'),max_length=5)
	matchHistory = db.ListField(db.ReferenceField('MatchHistory'))
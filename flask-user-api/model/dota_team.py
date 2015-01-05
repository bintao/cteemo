from model import db
from model.team import Team 

class DOTATeam(Team):
	members = db.ListField(db.ReferenceField('Profile'),max_length=7)
	matchHistory = db.ListField(db.ReferenceField('MatchHistory'))
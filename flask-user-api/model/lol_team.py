from model import db
from model.team import Team 

class LOLTeam(Team):
	members = db.ListField(db.ReferenceField('Profile'))
	matchHistory = db.ListField(db.ReferenceField('MatchHistory'))
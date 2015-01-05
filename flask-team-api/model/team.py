from user import db
from datetime import datetime

class Team(db.Document):
	create_time = db.DateTimeField(default=datetime.now())
	school = db.StringField()
	owner = db.ReferenceField('Profile')
	team_members = db.ListField(db.ReferenceField('Profile'))
	team_name = db.StringField(unique=True)
	team_icon = db.URLField()
	total_prize = db.FloatField()
	team_intro = db.StringField() # brief intro of the team 
	total_games = db.IntField()
	won_games = db.IntField()
	isSchool = db.BooleanField()
	#match history
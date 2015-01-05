from user import db
from datetime import datetime

class TeamInfo(db.Document):
	lol_team = db.ReferenceField('Team')
	#dota_team = db.ReferenceField()
	#hh_team = db.ReferenceField()
	#profile = db.ReferenceField('Profile')
	user_email = db.EmailField(unique=True)
	lol_id = db.StringField()
	dota_id = db.StringField()
	hh_stone_id = db.StringField()
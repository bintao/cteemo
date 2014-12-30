from user import db

class Team(db.Document):
	create_time = db.DateTimeField()
	school = db.StringField()
	owner = db.StringField()
	owner_email = db.EmailField()
	team_members = db.DictField()
	team_name = db.StringField(unique=True)
	team_icon = db.URLField()
	total_prize = db.FloatField()
	#match history
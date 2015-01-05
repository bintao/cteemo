from user import db

class Tournament(db.Document):
	start_time = db.DateTimeField()
	end_time = db.DateTimeField()
	school = db.StringField()
	tournament_name = db.StringField()
	time_zone = db.StringField()
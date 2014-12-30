from user import db

class Profile(db.Document):
	user_email = db.EmailField(unique=True)
	username = db.StringField()
	profile_icon = db.URLField()
	school = db.StringField()
	lol_id = db.StringField()
	dota_id = db.StringField()
	team = db.StringField()
	total_prize = db.FloatField()
	user_intro = db.StringField()
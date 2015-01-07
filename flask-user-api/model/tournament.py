from model import db

class Tournament(db.Document):
	creator = db.ReferenceField('Profile')
	entry_fee = db.FloatField()
	tournamentName = db.StringField(required=True)
	isSchool = db.BooleanField()
	school = db.StringField()
	tournamentIcon = db.URLField()
	descriptions = db.StringField(max_length=500)
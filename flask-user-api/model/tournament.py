from model import db

class Tournament(db.Document):
	creator = db.ReferenceField('Profile')
	entry_fee = db.IntField(default=0)
	tournamentName = db.StringField(required=True)
	isSchool = db.BooleanField()
	school = db.StringField()
	size = db.IntField(required=True)
	Total_Prize = db.IntField(default=0)
	descriptions = db.StringField(max_length=500)
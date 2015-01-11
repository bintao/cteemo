from model import db

class Tournament(db.Document):
	id = db.SequenceField(primary_key=True)
	creator = db.ReferenceField('Profile')
	entry_fee = db.IntField(default=0)
	tournamentName = db.StringField(required=True)
	isSchool = db.BooleanField(default=False)
	school = db.StringField()
	size = db.IntField(required=True)
	Total_Prize = db.IntField(default=0)
	descriptions = db.StringField(max_length=500)
	rounds = db.ListField(db.ReferenceField('Round'))
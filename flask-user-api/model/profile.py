from model import db

class Profile(db.Document):
	user = db.ReferenceField('User')
	username = db.StringField()
	profile_icon = db.URLField()
	school = db.StringField()
	intro = db.StringField(default='Player left nothing here', max_length=200)
	lolID = db.StringField()
	dotaID = db.StringField()
	hstoneID = db.StringField()
	LOLTeam = db.ReferenceField('LOLTeam')
	DOTATeam = db.ReferenceField('DOTATeam')
	HSTONETeam = db.ReferenceField('HSTONETeam')
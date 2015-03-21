from model import db

class Profile(db.Document):
	id = db.SequenceField(primary_key=True)
	user = db.ReferenceField('User')
	username = db.StringField(default='cteemoUser')
	profile_icon = db.URLField(default=	
'https://s3-us-west-2.amazonaws.com/profile-icon/123%40gmail.com_images.jpg')
	school = db.StringField()
	intro = db.StringField(default='Player left nothing here', max_length=200)
	lolID = db.StringField()
	dotaID = db.StringField()
	hstoneID = db.StringField()
	LOLTeam = db.ReferenceField('LOLTeam')
	DOTATeam = db.ReferenceField('DOTATeam')
	HSTONETeam = db.ReferenceField('HSTONETeam')
	
	gender = db.StringField()
	riotID = db.StringField()
	lollevel = db.IntField()
	lolIcon = db.StringField()
	lolRank = db.StringField()


	def checkInfo(self, username, school):
		if self.username != username or self.school != school:
			return False
		return True
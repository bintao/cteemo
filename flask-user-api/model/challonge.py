from model import db
from datetime import datetime

class Challonge(db.Document):
	id = db.SequenceField(primary_key=True)
	tournamentName = db.StringField(required=True)
	creator = db.ReferenceField('Profile')
	
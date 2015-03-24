from model import db
from datetime import datetime

class Challonge(db.Document):
	id = db.SequenceField(primary_key=True)
	name = db.StringField(required=True)
	tournament_type = db.StringField(default="single elimination")
	
from model import db
from datetime import datetime


class Post(db.Document):
	date = db.DateTimeField(default=datetime.now())
	content = db.StringField()
	meta = {'allow_inheritance' : True,
			'abstract' : True,
			}
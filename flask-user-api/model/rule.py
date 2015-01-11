from model import db

class Rule(db.Document):
	group_stage = db.BooleanField(default=False)
	team_size = db.IntField(max_value=5,min_value=1,required=True)
	eliminiation = db.IntField(default=1) # 1 stands for single-elimination 2 stands for double eliminiation
	map = db.StringField(default="Summoner's Rift")
	pick = db.StringField(default="TOURNAMENT DRAFT")
	tournament = db.ReferenceField('Tournament')
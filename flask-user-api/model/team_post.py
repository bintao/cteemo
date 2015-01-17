from model import db
from model.post import Post

class TeamPost(Post):
	team = db.ReferenceField('LOLTeam')
	user_profile = db.ReferenceField('Profile')
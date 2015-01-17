from model import db
from model.post import Post

class PlayerPost(Post):
    user_profile = db.ReferenceField('Profile')
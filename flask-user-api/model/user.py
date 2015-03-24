from flask import current_app
from model import db, bcrypt
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)

class User(db.Document):
    email = db.EmailField(unique=True)
    password_hash = db.StringField()
    fb_id = db.IntField()
    rongToken = db.StringField()
    is_activated = db.BooleanField(default=False)
    
    def hash_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password)

    def verify_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    def generate_auth_token(self):
        s = Serializer(current_app.config.get('SECRET_KEY'),expires_in=0)
        return s.dumps(str(self.id))




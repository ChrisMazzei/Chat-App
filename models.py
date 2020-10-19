# models.py
import flask_sqlalchemy
from app import db


class Chatlog(db.Model):
    __tablename__ = 'chatlog'
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(120))
    
    def __init__(self, a):
        self.message = a

    def __repr__(self):
        return '<Chat message: %s>' % self.message 


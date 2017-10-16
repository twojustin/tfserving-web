from flask_sqlalchemy import SQLAlchemy
import random

db = SQLAlchemy()

class TrainedModel(db.Model):
    __tablename__ = 'trained_models'

    id = db.Column(db.Integer, primary_key=True)
    hash_id = db.Column(db.String())
    name = db.Column(db.String())

    def __init__(self, name):
        self.hash_id = random.getrandbits(32)
        self.name = name

    def __repr__(self):
        return '<Model {}>'.format(self.id)

    @property
    def serialize(self):
        return {
            'id': self.hash_id,
            'name': self.name
        }

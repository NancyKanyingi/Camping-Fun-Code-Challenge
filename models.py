from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from Server.extensions import db
# Create db instance here

class Camper(db.Model):
    __tablename__ = 'campers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    age = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"<Camper {self.name}>"

    signups = db.relationship('Signup', back_populates='camper', cascade='all, delete-orphan')
    activities = db.relationship('Activity', secondary='signups', back_populates='campers')

    def to_dict(self, include_signups=False):
        base = {"id": self.id, "name": self.name, "age": self.age}
        if include_signups:
            base["signups"] = [s.to_dict(include_nested_activity=True) for s in self.signups]
        return base

    @validates('name')
    def validate_name(self, key, value):
        if not value or not value.strip():
            raise ValueError('name is required')
        return value.strip()

    @validates('age')
    def validate_age(self, key, value):
        try:
            value_int = int(value)
        except Exception:
            raise ValueError('age must be an integer')
        if value_int < 8 or value_int > 18:
            raise ValueError('age must be between 8 and 18')
        return value_int


class Activity(db.Model):
    __tablename__ = 'activities'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    difficulty = db.Column(db.Integer, nullable=False)

    signups = db.relationship('Signup', back_populates='activity', cascade='all, delete-orphan')
    campers = db.relationship('Camper', secondary='signups', back_populates='activities')

    def to_dict(self):
        return {"id": self.id, "name": self.name, "difficulty": self.difficulty}

    @validates('name')
    def validate_name(self, key, value):
        if not value or not value.strip():
            raise ValueError('name is required')
        return value.strip()

    @validates('difficulty')
    def validate_difficulty(self, key, value):
        try:
            d = int(value)
        except Exception:
            raise ValueError('difficulty must be an integer')
        if d < 0:
            raise ValueError('difficulty must be >= 0')
        return d


class Signup(db.Model):
    __tablename__ = 'signups'

    id = db.Column(db.Integer, primary_key=True)
    camper_id = db.Column(db.Integer, db.ForeignKey('campers.id'), nullable=False)
    activity_id = db.Column(db.Integer, db.ForeignKey('activities.id'), nullable=False)
    time = db.Column(db.Integer, nullable=False)

    camper = db.relationship('Camper', back_populates='signups')
    activity = db.relationship('Activity', back_populates='signups')

    def to_dict(self, include_nested_activity=False):
        base = {"id": self.id, "time": self.time}
        if include_nested_activity:
            base["activity"] = self.activity.to_dict()
        return base

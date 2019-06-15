from werkzeug.security import generate_password_hash, check_password_hash

from app.routes import db
from datetime import datetime


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    trails = db.relationship('Trail', backref='author', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __str__(self):
        return f'Issue #{self.id}: {self.name}'

    def __repr__(self):
        return f'Issue #{self.id}: {self.name}'


class Trail(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    photos = db.relationship('Photo', backref='trail', lazy='dynamic')

    def __repr__(self):
        return f'<Trail {self.body}>'


class Photo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(140))
    # date = db.Column(db.String(140))  #  TODO: решить, как работать с датой и временем
    lat = db.Column(db.Float)
    lng = db.Column(db.Float)
    timestamp = db.Column(db.DateTime)
    trail_id = db.Column(db.Integer, db.ForeignKey('trail.id'))

    def __repr__(self):
        return f'<Photo {self.body}>'

from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from app import db, login

from datetime import datetime


class User(UserMixin, db.Model):
    # __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    trails = db.relationship('Trail', backref='author', lazy='dynamic')

    def __repr__(self):
        return f'{self.id}: {self.username}'

    def __str__(self):
        return f'{self.id}: {self.username}'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Trail(db.Model):
    # __tablename__ = 'trails'
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    private = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    photos = db.relationship('Photo', backref='trail', lazy='dynamic')

    def __repr__(self):
        return f'Trail {self.photos}'


class Photo(db.Model):
    # __tablename__ = 'photos'
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(36))
    filename = db.Column(db.String(40))
    original_filename = db.Column(db.String(50))
    thumbnail = db.Column(db.String(50))
    # rotation = db.Column(db.Integer)
    comment = db.Column(db.String(140))
    datetime = db.Column(db.String(20))  # TODO: решить, как работать с датой и временем
    lat = db.Column(db.Float)
    lng = db.Column(db.Float)
    timestamp = db.Column(db.DateTime)
    deleted = db.Column(db.Boolean, default=False)
    trail_id = db.Column(db.Integer, db.ForeignKey('trail.id'))

    def __repr__(self):
        return f'Photo {self.file}'


@login.user_loader
def load_user(id):
    return User.query.get(int(id))

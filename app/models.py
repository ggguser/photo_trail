from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, current_user

from app import db, login

from datetime import datetime


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    trails = db.relationship('Trail', backref='author', lazy='dynamic')
    photos = db.relationship('Photo', backref='author', lazy='dynamic')
    countries = db.relationship('Country', backref='imported_by', lazy='dynamic')

    def __repr__(self):
        return f'{self.username}'

    def __str__(self):
        return f'{self.username}'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def countries_visited(self):
        countries_visited = []
        for trail in self.trails:
            for photo in trail.photos:
                countries_visited.append(photo.country)
        return len(set(countries_visited))

    def countries_visited_iso(self):
        countries_visited = []
        for trail in self.trails:
            for photo in trail.photos:
                countries_visited.append(photo.country.iso)
        return set(countries_visited)

    def areas_visited(self):
        areas_visited = []
        for trail in self.trails:
            for photo in trail.photos:
                areas_visited.append(photo.area)
        return len(set(areas_visited))


class Trail(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    private = db.Column(db.Boolean, default=False)
    deleted = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    photos = db.relationship('Photo', backref='trail', lazy='dynamic')

    # def __repr__(self):
    #     return f'Trail {self.photos}'


class Photo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(36))
    original_filename = db.Column(db.String(50))
    # rotation = db.Column(db.Integer)  # TODO: если пользователь хочет повернуть не так как в EXIF
    comment = db.Column(db.String(140))
    error = db.Column(db.String(140), default=None)
    unsupported_country = db.Column(db.String(50), default=None)
    # country_iso = db.Column(db.String(4), default=None)
    country_id = db.Column(db.Integer, db.ForeignKey('country.id'), default=None)
    area_id = db.Column(db.Integer, db.ForeignKey('area.id'), default=None)
    # area_iso = db.Column(db.String(8), default=None)
    # country = db.Column(db.String(140))
    # area = db.Column(db.String(140), default=None)
    # city = db.Column(db.String(140))  # TODO: пока только с регионами работаем
    datetime = db.Column(db.String(20))
    lng = db.Column(db.Float, default=None)
    lat = db.Column(db.Float, default=None)
    # timestamp = db.Column(db.DateTime)
    deleted = db.Column(db.Boolean, default=False)  # TODO: возможно лучше timestamp, чтобы удалять старые
    trail_id = db.Column(db.Integer, db.ForeignKey('trail.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    private = db.Column(db.Boolean, default=False)

    def thumbnail(self):
        return str(self.uuid + '_thumbnail.jpg')

    def filename(self):
        return str(self.uuid + '.jpg')

    # def __repr__(self):
    #     return f'Photo {self.filename()}'


class Country(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(140))
    iso = db.Column(db.String(10))
    areas = db.relationship('Area', backref='country', lazy='dynamic')
    areas_count = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    photos = db.relationship('Photo', backref='country', lazy='dynamic')

    def __repr__(self):
        return f'{self.name}'

    def __str__(self):
        return f'{self.name}'


class Area(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(140))
    iso = db.Column(db.String(10))
    country_id = db.Column(db.Integer, db.ForeignKey('country.id'))
    photos = db.relationship('Photo', backref='area', lazy='dynamic')

    def __repr__(self):
        return f'{self.name}'

    def __str__(self):
        return f'{self.name}'

    def photos_count(self):  # FIXME: Не уверен, что это эффективно
        photos = []
        for photo in self.photos:
            if not photo.deleted and not photo.private:
                photos.append(photo)
        return len(photos)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))



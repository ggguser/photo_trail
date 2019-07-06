from werkzeug.urls import url_parse
from werkzeug.utils import secure_filename

from datetime import datetime

from app import app, db
from app.forms import LoginForm, RegistrationForm, PhotoUploadForm, PhotoEditForm, TrailUploadForm, PhotoDeleteForm
from app.exif import get_exif_data, get_exif_location, create_thumbnail, get_exif_datetime
from app.geocoder import get_area_name, get_json_from_yandex, check_country, get_country_name
from app.models import User, Trail, Photo

import os
from uuid import uuid4

from flask import render_template, request, url_for, redirect, flash
from flask_login import current_user, login_user, logout_user, login_required

from app.exif import get_exif_orientation

# from phototrail import app

photos = []


@app.route('/')
@app.route('/index')
def index():
    trails = Trail.query.all()
    return render_template('index.html', title='Главная', trails=trails)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Не подходит пароль или логин, а может и оба')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Поздравляем с регистрацией!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Registration', form=form)


# @app.route('/upload', methods=['POST'])
# @login_required
# def upload():
#     photos = []

#     if 'photo' not in request.files:
#         redirect(url_for('index'))
#
#     photo = request.files['photo']
#     photo_name = str(uuid.uuid4())
#     photos.append(photo_name)
#     trails.append(photos)
#     path = os.path.join(app.config['IMAGE_DIR'], photo_name)  # TODO: это можно переместить в config?
#     photo.save(path)  # TODO: загрузка нескольких файлов сразу
#     return redirect(url_for('create'))


@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():

    global photos

    form = PhotoUploadForm()
    save = TrailUploadForm()
    delete = PhotoDeleteForm()
    photo = Photo()

    if form.upload.data and form.validate():
        size = (400, 400)

        photo.uuid = str(uuid4())
        photo.filename = secure_filename(photo.uuid + '.jpg')
        photo.thumbnail = secure_filename(photo.uuid + '_thumbnail.jpg')
        photo_path = os.path.join(app.config['IMAGE_DIR'], photo.filename)
        thumbnail_path = os.path.join(app.config['IMAGE_DIR'], photo.thumbnail)
        form.photo.data.save(photo_path)

        photo.original_filename = form.photo.data.filename[:50]

        exif_data = get_exif_data(photo_path)
        photo.datetime = get_exif_datetime(exif_data)
        photo.lat, photo.lng = get_exif_location(exif_data)

        if not photo.lat or not photo.lng:
            photo.error = 'no_coordinates'

        else:
            geocoder_info = get_json_from_yandex(f'{photo.lng},{photo.lat}')
            photo.country = get_country_name(geocoder_info)
            photo.area = get_area_name(geocoder_info)

            if not check_country(photo.country):
                photo.error = 'unsupported_country'

        rotation = get_exif_orientation(exif_data)
        create_thumbnail(photo_path, thumbnail_path, size, rotation)

        photos.append(photo)

        return render_template('photo_upload.html', form=form, photos=photos, save=save, delete=delete)

    if save.submit.data and save.validate():

        trail = Trail(comment=save.comment.data,
                      private=save.private.data,
                      author=current_user,
                      timestamp=datetime.utcnow())
        db.session.add(trail)
        db.session.commit()

        for photo in photos:
            photo.trail_id = trail.id
            db.session.add(photo)
            db.session.commit()

        photos = []

        return redirect(url_for('index'))

    return render_template('photo_upload.html', form=form, photos=photos, save=save, delete=delete)


@app.route('/<photo_id>/delete', methods=['POST'])
@login_required
def delete_photo(photo_id):

    global photos
    result = []
    for photo in photos:
        if photo.uuid == photo_id:
            photo.deleted = True
#  Если не хотим добавлять в БД фотографии, удалённые на стадии загрузки
        else:
            result.append(photo)
        photos = result

    return redirect(url_for('upload'))


    # @app.route('/user/<photo_id>/remove', methods=['POST'])
    # def delete_photo(photo_id):
    #     global photos
    #     if delete.validate_on_submit():
    #         result = []
    #         for photo in photos:
    #             if photo.uuid != photo_id:
    #                 result.append(photo)
    #         photos = result
    #     return render_template('photo_upload.html', form=form, photos=photos, save=save, edit=edit, delete=delete)



    # if save.validate_on_submit():
    #
    #     trail.user_id = current_user




@app.route('/user/<photo_id>/edit', methods=['GET', 'POST'])
@login_required
def photo_edit(photo_id):
    edit = PhotoEditForm()
    return render_template('photo_edit.html')




@app.route('/save', methods=['GET', 'POST'])
@login_required
def save_trail():
    save = TrailUploadForm()
    trail = Trail()
    if save.validate_on_submit():
        pass


# @app.route('/user/<photo_id>/remove', methods=['POST'])
# @login_required
# def delete_photo(photo_id):


    # result = []
    # for photo in photos:
    #     if photo.uuid != photo_id:
    #         result.append(photo)
    # photos = result

    # photos = list(filter(lambda photos: photos.uuid != photo_id), photos)
    # photo_form = PhotoEditForm()

    # return render_template('user.html')

    # return render_template('photo_upload.html', form=form, photos=photos, save=save, edit=edit)
    # return render_template('_photo_edit.html', photo=photo, edit=edit)

    # render_template('photo_upload.html', form=form, photos=[], save=save, edit=edit)

    # return redirect(url_for('create'))


@app.route('/user/<username>')
@login_required
def user(username):
    photos = []
    user = User.query.filter_by(username=username).first_or_404()
    trails = Trail.query.filter_by(user_id=user.id)
    # Photo.query.filter_by(trail_id=trails.id)

    # Post.query.join(
    #     followers, (followers.c.followed_id == Post.user_id)).filter(
    #     followers.c.follower_id == self.id).order_by(
    #     Post.timestamp.desc())
    return render_template('user.html', user=user, trails=trails, photos=photos)


# @app.route('/create')
# @login_required
# def create():
#     form = UploadForm()
#     return render_template('create.html', username=current_user, form=form)


# if __name__ == '__main__':
#     app.run(port=9873, debug=True)

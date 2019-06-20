from werkzeug.urls import url_parse
from werkzeug.utils import secure_filename

from app import db
from app.forms import LoginForm, RegistrationForm, UploadForm
from app.models import User

import os
import uuid

from flask import render_template, request, url_for, redirect, flash
from flask_login import current_user, login_user, logout_user, login_required

from phototrail import app

photos = []
trails = [photos]


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Главная', trails=trails)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
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
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Registration', form=form)


# @app.route('/upload', methods=['POST'])
# @login_required
# def upload():
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


@app.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    form = UploadForm()

    if form.validate_on_submit():
        filename = secure_filename(form.file.data.filename)
        path = os.path.join(app.config['IMAGE_DIR'], filename)
        form.file.data.save(path)
        return redirect(url_for('create'))

    return render_template('create.html', form=form)


@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    trails = [
        {'author': user, 'comment': 'Test trail #1'},
        {'author': user, 'comment': 'Test trail #2'}
    ]
    return render_template('user.html', user=user, trails=trails)


# @app.route('/create')
# @login_required
# def create():
#     form = UploadForm()
#     return render_template('create.html', username=current_user, form=form)


if __name__ == '__main__':
    # db.init_app(app)
    # db.create_all()

    app.run(port=9874, debug=True)
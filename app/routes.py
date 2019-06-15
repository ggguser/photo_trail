from app import app, db
from app.forms import LoginForm
from app.models import User

import os
import uuid

from flask import render_template, request, url_for, redirect, flash
from flask_login import current_user, login_user

photos = []


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', photos=photos)


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
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)


@app.route('/upload', methods=['POST'])
def upload():
    if 'photo' not in request.files:
        redirect(url_for('index'))

    photo = request.files['photo']
    photo_name = str(uuid.uuid4()) + '.jpg'
    photos.append(photo_name)
    path = os.path.join(app.config['IMAGE_DIR'], photo_name)  # TODO: это можно переместить в config?
    photo.save(path)
    return redirect(url_for('index'))


if __name__ == '__main__':

    db.init_app(app)
    db.create_all()

    app.run(port=9874, debug=True)
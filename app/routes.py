import os
import uuid

from flask import Flask, render_template, request, url_for, redirect, flash

from app.forms import LoginForm

app = Flask(__name__)
app.config['IMAGE_DIR'] = os.path.join('static', 'photos')
app.config['SECRET_KEY'] = 'this_is_secret'
photos = []


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', photos=photos)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash(f'Login requested for user {form.username.data}, remember_me={form.remember_me.data}')
        return redirect('/index')
    return render_template('login.html', title='Sign In', form=form)


@app.route('/upload', methods=['POST'])
def upload():
    if 'photo' not in request.files:
        redirect(url_for('index'))

    photo = request.files['photo']
    photo_name = str(uuid.uuid4()) + '.jpg'
    photos.append(photo_name)
    path = os.path.join(app.config['IMAGE_DIR'], photo_name)
    photo.save(path)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(port=9874, debug=True)
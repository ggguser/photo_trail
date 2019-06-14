import os
import uuid

from flask import Flask, render_template, request, url_for, redirect

app = Flask(__name__)
app.config['IMAGE_DIR'] = os.path.join('static', 'photos')
photos = []


@app.route('/')
def index():
    return render_template('index.html', photos=photos)


@app.route('/upload', methods=['POST'])
def upload():
    if 'photo' not in request.files:
        redirect(url_for('index'))

    photo = request.files['photo']
    photo_name = str(uuid.uuid4())
    photos.append(photo_name)
    path = os.path.join(app.config['IMAGE_DIR'], photo_name)
    photo.save(path)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(port=9874, debug=True)
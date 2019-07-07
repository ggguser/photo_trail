from flask_wtf import FlaskForm, widgets
from flask_wtf.file import FileRequired, FileAllowed
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, FileField, MultipleFileField
from wtforms.validators import DataRequired, EqualTo, Email, ValidationError, Length

from app.models import User


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired()])
    email = StringField('Почта', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password2 = PasswordField('Ещё раз пароль', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Зарегистрироваться')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Это имя уже кем-то занято, попробуйте другое')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('На этот адрес уже зарегистрировался кто-то другой')


class PhotoEditForm(FlaskForm):
    area = StringField('Username', validators=[DataRequired()])
    comment = TextAreaField('Описание', validators=[Length(min=0, max=140)])
    delete = SubmitField('Удалить')
    save = SubmitField('Submit')


class PhotoUploadForm(FlaskForm):
    photo = FileField(validators=[FileRequired(message='Забыли фото приложить!'),
                                  FileAllowed(['jpg', 'jpeg'], 'Подойдут только jpeg файлы')])
    upload = SubmitField('Загрузить')


class PhotoDeleteForm(FlaskForm):
    delete = SubmitField('X')


class TrailUploadForm(FlaskForm):
    private = BooleanField('Сделать фотографии приватным')
    comment = TextAreaField('Описание', validators=[Length(min=0, max=140)])
    submit = SubmitField('Сохранить эти фотографии')


class AddCountryForm(FlaskForm):
    name = StringField('Страна', validators=[DataRequired(message='Нужно указать название страны')])
    submit = SubmitField('Добавить страну')


class ImportAreasForm(FlaskForm):
    file = FileField(validators=[FileRequired(message='Нужно вложить файл!'),
                                 FileAllowed(['csv'], 'Импортировать можно только csv')])
    upload = SubmitField('Импортировать')

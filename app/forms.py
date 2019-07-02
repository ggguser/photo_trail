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
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Это имя уже кем-то занято, попробуйте другое')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('На этот адрес уже зарегистрировался кто-то другой')


class PhotoUploadForm(FlaskForm):
    submit = SubmitField('Загрузить')
    photo = FileField(validators=[FileRequired(),
                                  FileAllowed(['jpg', 'jpeg'], 'Подойдут только jpeg файлы')])


class PhotoEditForm(FlaskForm):
    area = StringField('Username', validators=[DataRequired()])
    comment = TextAreaField('About me', validators=[Length(min=0, max=140)])
    delete = SubmitField('del')
    save = SubmitField('Submit')


class PhotoDeleteForm(FlaskForm):
    delete = SubmitField('Delete')


class TrailUploadForm(FlaskForm):
    private = BooleanField('Сделать фотографии приватным')
    comment = TextAreaField('Описание')
    save = SubmitField('Сохранить эти фотографии')

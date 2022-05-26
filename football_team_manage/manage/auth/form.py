from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, HiddenField
from wtforms.validators import Length, Email, EqualTo, Regexp, ValidationError, DataRequired
from wtforms.widgets import PasswordInput

from football_team_manage.models.models import User


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=50), Regexp(regex=r'^(?![\s.]+$)[a-zA-Z0-9sq\s.]*$')])
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=50)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = StringField('Password', validators=[DataRequired()], widget=PasswordInput(hide_value=False))
    confirm_password = StringField('Confirm Password', widget=PasswordInput(hide_value=False),
                                   validators=[DataRequired(), EqualTo('password')])
    phone = StringField('Phone', validators=[DataRequired(), Length(max=11), Regexp(regex=r'^[0-9]{11}')])
    submit = SubmitField('Sign in')

    def validate_username(self, username):
        user = User.query.filter_by(user_name=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=50), Regexp(regex=r'^(?![\s.]+$)[a-zA-Z0-9sq\s.]*$')])
    password = StringField('Password', validators=[DataRequired()], widget=PasswordInput(hide_value=False))
    remember = BooleanField('Remember me')
    submit = SubmitField('Sign in')





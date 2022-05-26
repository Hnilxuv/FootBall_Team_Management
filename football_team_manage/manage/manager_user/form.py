from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import Length, Email, Regexp, DataRequired, ValidationError, EqualTo
from wtforms.widgets import PasswordInput
from football_team_manage.models.models import Roles, User


class UpdateUserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=50)])
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=50)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone', validators=[DataRequired(), Length(max=11), Regexp(regex=r'^[0-9]{11}')])
    role_name = SelectField('Role Name', choices=[roles.name for roles in Roles.query.all()])
    status = SelectField('Status', choices=[True, False])
    submit = SubmitField('Update')


class InsertationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=50), Regexp(regex=r'^(?![\s.]+$)[a-zA-Z0-9sq\s.]*$')])
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=50)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = StringField('Password', validators=[DataRequired()], widget=PasswordInput(hide_value=False))
    confirm_password = StringField('Confirm Password', widget=PasswordInput(hide_value=False),
                                   validators=[DataRequired(), EqualTo('password')])
    phone = StringField('Phone', validators=[DataRequired(), Length(max=11), Regexp(regex=r'^[0-9]{11}')])
    submit = SubmitField('Insert')

    def validate_username(self, username):
        user = User.query.filter_by(user_name=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')

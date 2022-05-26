from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, HiddenField
from wtforms.validators import Length, Email, EqualTo, Regexp, ValidationError, DataRequired
from wtforms.widgets import PasswordInput

from football_team_manage.models.models import User


class UpdateAccountForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=50)])
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=50)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone', validators=[DataRequired(), Length(max=11), Regexp(regex=r'^[0-9]{11}')])
    role_name = StringField('Role Name', render_kw={'readonly': True})
    submit = SubmitField('Update')


class ChangePasswordForm(FlaskForm):
    old_password = StringField('Old Password', validators=[DataRequired()], widget=PasswordInput(hide_value=False))
    new_password = StringField('New Password', validators=[DataRequired()], widget=PasswordInput(hide_value=False))
    new_confirm_password = StringField('New Confirm Password', widget=PasswordInput(hide_value=False),
                                       validators=[DataRequired(), EqualTo('new_password')])
    submit = SubmitField('Change Password')

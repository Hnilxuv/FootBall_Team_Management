from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, SelectField, IntegerField
from wtforms.validators import Length, Email, EqualTo, Regexp, ValidationError, DataRequired
from wtforms.widgets import PasswordInput

from football_team_manage.models.models import User, Roles, Player, LeagueJoin, Position


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=50),
                                                   Regexp(regex=r'^(?![\s.]+$)[a-zA-Z0-9sq\s.]*$')])
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=50)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = StringField('Password', validators=[DataRequired()], widget=PasswordInput(hide_value=False))
    confirm_password = StringField('Confirm Password', widget=PasswordInput(hide_value=False),
                                   validators=[DataRequired(), EqualTo('password')])
    phone = StringField('Phone', validators=[DataRequired(), Length(max=11), Regexp(regex=r'^[0-9]{11}')])
    submit = SubmitField('Sign up')

    def validate_username(self, username):
        user = User.query.filter_by(user_name=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=50),
                                                   Regexp(regex=r'^(?![\s.]+$)[a-zA-Z0-9sq\s.]*$')])
    password = StringField('Password', validators=[DataRequired()], widget=PasswordInput(hide_value=False))
    remember = BooleanField('Remember me')
    submit = SubmitField('Sign in')


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


class UpdateUserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=50)])
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=50)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone', validators=[DataRequired(), Length(max=11), Regexp(regex=r'^[0-9]{11}')])
    role_name = SelectField('Role Name', choices=[roles.name for roles in Roles.query.all()])
    status = SelectField('Status', choices=[('True', 'Enable'), ('False', 'Disable')])
    submit = SubmitField('Update')


class InsertionUserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=50),
                                                   Regexp(regex=r'^(?![\s.]+$)[a-zA-Z0-9sq\s.]*$')])
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


class EditionForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=50)])
    submit = SubmitField('Update')


class InsertionRolesForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=50)])
    submit = SubmitField('Insert')

    def validate_name(self, name):
        user = Roles.query.filter_by(name=name.data).first()
        if user:
            raise ValidationError('That name is taken. Please choose a different one.')


class InsertionLeagueForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=50)])
    submit = SubmitField('Insert')

    def validate_name(self, name):
        user = LeagueJoin.query.filter_by(name=name.data).first()
        if user:
            raise ValidationError('That name is taken. Please choose a different one.')


class InsertionPositionForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=50)])
    submit = SubmitField('Insert')

    def validate_name(self, name):
        user = Position.query.filter_by(name=name.data).first()
        if user:
            raise ValidationError('That name is taken. Please choose a different one.')


class InsertionPlayerForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=50)])
    shirt_number = StringField('Shirt Number', validators=[DataRequired(), Length(max=50), Regexp(regex=r'^[0-9]{1,}')])
    age = StringField('Age', validators=[DataRequired(), Length(max=50), Regexp(regex=r'^[0-9]{1,}')])
    position_name = SelectField('Position', choices=[position.name for position in Position.query.all()])
    submit = SubmitField('Insert')

    def validate_name(self, name):
        user = Player.query.filter_by(name=name.data).first()
        if user:
            raise ValidationError('That name is taken. Please choose a different one.')


class EditionPlayerForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=50)])
    shirt_number = StringField('Shirt Number', validators=[DataRequired(), Length(max=50), Regexp(regex=r'^[0-9]{1,}')])
    age = StringField('Age', validators=[DataRequired(), Length(max=50), Regexp(regex=r'^[0-9]{1,}')])
    # join_time = StringField('Join Time', render_kw={'readonly': True})
    position_name = SelectField('Position', choices=[position.name for position in Position.query.all()])
    submit = SubmitField('Update')


class EditionUserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=50)])
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=50)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone', validators=[DataRequired(), Length(max=11), Regexp(regex=r'^[0-9]{11}')])
    role_name = StringField('Role Name', render_kw={'readonly': True})
    status = SelectField('Status', choices=[('True', 'Enable'), ('False', 'Disable')])
    submit = SubmitField('Update')
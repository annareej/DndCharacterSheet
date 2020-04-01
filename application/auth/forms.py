from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, validators

class LoginForm(FlaskForm):
	username = StringField("Username")
	password = PasswordField("Password")

	class Meta:
		csrf = False

class UserForm(FlaskForm):
	name = StringField("Name", [validators.InputRequired()])
	username = StringField("Username", [validators.InputRequired()])
	password = PasswordField("Password", [validators.Length(min=8), validators.EqualTo('password2', message="Passwords must match!")])
	password2 = PasswordField("Confirm password")

	class Meta:
		csrf = False
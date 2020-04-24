from flask import render_template, request, redirect, url_for
from flask_login import login_user, logout_user

from application import app, db, bcrypt
from application.auth.models import User
from application.auth.forms import LoginForm, UserForm, PasswordForm

@app.route("/auth/userform", methods=["GET"])
def user_form():
	return render_template("auth/newuser.html", form = UserForm())

@app.route("/auth/change", methods=["GET"])
def changepwd_form():
	return render_template("auth/changepwd.html", form = PasswordForm())

@app.route("/auth/signup", methods=["POST"])
def user_create():
	form = UserForm(request.form)

	if not form.validate():
		return render_template("auth/newuser.html", form = form)

	name = (form.name.data)
	username = (form.userform.username.data)
	password = (form.userform.password.data)

	user = User.query.filter_by(username=username).first()

	if not user:
		user = User(name, username, password)

		db.session().add(user)
		db.session().commit()

		login_user(user)
		return redirect(url_for("index")) 

	else:
		return render_template("auth/newuser.html", form = form, error = "User already exists")

@app.route("/auth/changepwd", methods=["POST"])
def user_change_password():
	form = PasswordForm(request.form)
	user = User.query.filter_by(username=form.username.data).first()
	
	if not form.validate():
		return render_template("auth/changepwd.html", form = form)

	if not user:
		return render_template("auth/changepwd.html", form = form, error = "No such user")
	else:
		user.change_password(form.password.data)
		db.session().add(user)
		db.session().commit()

		login_user(user)
		return redirect(url_for("index"))	

@app.route("/auth/login", methods = ["GET", "POST"])
def auth_login():
	if request.method == "GET":
		return render_template("auth/loginform.html", form = LoginForm())

	form = LoginForm(request.form)

	found_user = User.query.filter_by(username=form.username.data).first()
	if found_user and bcrypt.check_password_hash(found_user.password, form.password.data):
		login_user(found_user)
		return redirect(url_for("index"))
	else:
		return render_template("auth/loginform.html", form = form, error = "No such username or password")

@app.route("/auth/logout")
def auth_logout():
	logout_user()
	return redirect(url_for("index"))

from flask import render_template, request, redirect, url_for
from flask_login import login_user, logout_user

from application import app, db
from application.auth.models import User
from application.auth.forms import LoginForm
from application.auth.forms import UserForm

@app.route("/auth/userform", methods=["GET"])
def user_form():
	return render_template("auth/newuser.html", form = UserForm())

@app.route("/auth/newuser", methods=["POST"])
def user_create():
	form = UserForm(request.form)
	
	if not form.validate():
		return render_template("auth/newuser.html", form = form)
	
	name = (form.name.data)
	username = (form.username.data)
	password = (form.password.data)

	user = User.query.filter_by(username=form.username.data).first()
	
	if not user:
		user = User(name, username, password)

		db.session().add(user)
		db.session().commit()

		login_user(user)
		return redirect(url_for("index")) 
	
	else:
		return render_template("auth/newuser.html", form = form, error = "User already exists")

@app.route("/auth/login", methods = ["GET", "POST"])
def auth_login():
	if request.method == "GET":
		return render_template("auth/loginform.html", form = LoginForm())

	form = LoginForm(request.form)

	user = User.query.filter_by(username=form.username.data, password=form.password.data).first()
	if not user:
		return render_template("auth/loginform.html", form = form, error = "No such username or password")

	login_user(user)
	return redirect(url_for("index"))

@app.route("/auth/logout")
def auth_logout():
	logout_user()
	return redirect(url_for("index"))

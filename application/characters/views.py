from application import app, db
from flask import redirect, render_template, request, url_for
from application.characters.models import Character

@app.route("/characters/", methods=["GET"])
def characters_index():
	return render_template("characters/list.html", characters = Character.query.all())

@app.route("/characters/new/")
def character_form():
	return render_template("characters/new.html")

@app.route("/characters/<char_id>/", methods=["GET"])
def character_view(char_id):
	return render_template("characters/sheet.html", character = Character.query.get(char_id))

@app.route("/characters/", methods=["POST"])
def character_create():
	name = request.form.get("name")
	str = int(request.form.get("str"))
	dex = int(request.form.get("dex"))
	con = int(request.form.get("con"))
	intel = int(request.form.get("int"))
	wis = int(request.form.get("wis"))
	cha = int(request.form.get("cha"))

	c = Character(name, str, dex, con, intel, wis, cha)

	db.session().add(c)
	db.session().commit()

	return redirect(url_for("characters_index"))

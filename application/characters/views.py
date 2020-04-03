from flask import redirect, render_template, request, url_for
from flask_login import login_required, current_user

from application import app, db
from application.characters.models import Character
from application.characters.forms import CharacterForm

from application.sheet.models import CharacterSheet

from application.races.models import Race

@app.route("/characters/", methods=["GET"])
@login_required
def characters_index():
	return render_template("characters/list.html", characters = Character.query.filter_by(account_id=current_user.id))

@app.route("/characters/new/")
@login_required
def character_form():
	return render_template("characters/new.html", form = CharacterForm())

@app.route("/characters/<char_id>/", methods=["GET"])
@login_required
def character_view(char_id):
	return render_template("sheets/sheet.html", sheet = CharacterSheet(char_id))

@app.route("/characters/<char_id>/", methods=["POST"])
@login_required
def character_level_up(char_id):

	character = Character.query.get(char_id)
	if character.level < 20:
		character.level += 1
		db.session().commit()

	return redirect(request.url)

@app.route("/characters/remove/<char_id>/", methods=["POST"])
@login_required
def character_remove(char_id):
	character = Character.query.get(char_id)
	db.session().delete(character)
	db.session().commit()
	return redirect(url_for("characters_index"))

@app.route("/characters/render", methods=["POST"])
def render_form():
	form = CharacterForm(request.form)
	race = form.race.data

	return render_template("characters/new.html", form = form, race = race)

@app.route("/characters/", methods=["POST"])
@login_required
def character_create():
	form = CharacterForm(request.form)
	race = form.race.data

	if not form.validate():
		return render_template("characters/new.html", form = form)

	name = form.name.data
	str = int(form.strength.data)
	dex = int(form.dexterity.data)
	con = int(form.constitution.data)
	intel = int(form.intelligence.data)
	wis = int(form.wisdom.data)
	cha = int(form.charisma.data)

	c = Character(name, str, dex, con, intel, wis, cha)

	c.race = race.id
	c.account_id = current_user.id

	db.session().add(c)
	db.session().commit()

	return redirect(url_for("characters_index"))

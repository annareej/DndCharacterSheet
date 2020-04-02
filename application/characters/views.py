from flask import redirect, render_template, request, url_for
from flask_login import login_required, current_user

from application import app, db
from application.characters.models import Character
from application.characters.forms import CharacterForm

@app.route("/characters/", methods=["GET"])
@login_required
def characters_index():
	return render_template("characters/list.html", characters = Character.query.filter_by(account_id=current_user.id))

@app.route("/characters/new/")
@login_required
def character_form():
	return render_template("characters/new.html", form = CharacterForm())

@app.route("/characters/<char_id>/", methods=["GET"])
def character_view(char_id):
	return render_template("characters/sheet.html", character = Character.query.get(char_id))

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
	Character.query.filter_by(id=char_id).delete()
	db.session().commit()
	return redirect(url_for("characters_index"))

@app.route("/characters/", methods=["POST"])
@login_required
def character_create():
	form = CharacterForm(request.form)

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

	c.account_id = current_user.id

	db.session().add(c)
	db.session().commit()

	return redirect(url_for("characters_index"))

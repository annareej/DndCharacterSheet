from flask import redirect, render_template, request, url_for, g
from flask_login import login_required, current_user

from application import app, db
from application.characters.models import Character
from application.characters.forms import CharacterForm, LevelUpForm

from application.staticmethods import StaticMethods

from application.classes.models import CharacterClass
from application.races.models import Race

from application.sheet.models import CharacterSheet
from application.armor.models import Armor
from application.armor.forms import ArmorForm

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
	return render_template("sheets/sheet.html", sheet = CharacterSheet(char_id), form = LevelUpForm(), armorform = ArmorForm())

@app.route("/characters/levelup/<char_id>/", methods=["POST"])
@login_required
def character_level_up(char_id):
	form = LevelUpForm(request.form)
	character = Character.query.get(char_id)
	race = Race.query.get(character.race_id)
	conmod = character.constitution + race.constitution
	
	if character.level < 20:
		hp = int(form.hpfield.data) + StaticMethods.getModifier(conmod)
		character.level += 1
		character.maxhp += hp
		db.session().add(character)
		db.session().commit()

	return redirect(url_for("character_view", char_id=char_id, form=LevelUpForm(), armorform=ArmorForm()))

@app.route("/characters/remove/<char_id>/", methods=["POST"])
@login_required
def character_remove(char_id):
	character = Character.query.get(char_id)
	db.session().delete(character)
	db.session().commit()
	return redirect(url_for("characters_index"))

@app.route("/characters/armor/<char_id>/", methods=["POST"])
@login_required
def character_add_armor(char_id):
	form = ArmorForm(request.form)
	armor = form.armor.data
	character = Character.query.get(char_id)
	if not armor:
		character.add_armor(None)
	else:
		character.add_armor(armor.id)
	db.session().commit()

	return redirect(url_for("character_view", char_id=char_id, form=LevelUpForm(), armorform=ArmorForm()))

@app.route("/characters/", methods=["POST"])
@login_required
def character_create():
	form = CharacterForm(request.form)
	race = form.race.data
	class_id = form.class_id.data

	if not form.validate():
		return render_template("characters/new.html", form = form)

	name = form.name.data

	str = int(form.strength.data)
	dex = int(form.dexterity.data)
	con = int(form.constitution.data)
	intel = int(form.intelligence.data)
	wis = int(form.wisdom.data)
	cha = int(form.charisma.data)

	hp = class_id.hitdice + StaticMethods.getModifier(con)

	c = Character(name, hp, str, dex, con, intel, wis, cha)

	c.race_id = race.id
	c.class_id = class_id.id
	c.account_id = current_user.id

	db.session().add(c)
	db.session().commit()

	return redirect(url_for("characters_index"))

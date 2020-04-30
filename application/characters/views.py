from flask import redirect, render_template, request, url_for, g
from flask_login import login_required, current_user

from application import app, db
from application.characters.models import Character, CharacterWeapons
from application.characters.forms import CharacterForm, LevelUpForm

from application.staticmethods import StaticMethods

from application.classes.models import CharacterClass
from application.races.models import Race

from application.sheet.models import CharacterSheet
from application.armor.models import Armor
from application.armor.forms import ArmorForm

from application.weapons.forms import EquipWeaponForm

@app.route("/characters/", methods=["GET"])
@login_required
def characters_index():
	return render_template("characters/list.html", characters = Character.get_user_characters(account_id=current_user.id))

@app.route("/characters/new/")
@login_required
def character_form():
	return render_template("characters/new.html", form = CharacterForm())

@app.route("/characters/edit/<char_id>/", methods=["GET"])
def character_edit_form(char_id):
	character = Character.query.get(char_id)
	form = CharacterForm(race=character.race_id, class_id=character.class_id)

	form.name.data = character.name
	form.race.data = character.race_id
	form.class_id.data = character.class_id
	form.strength.data = character.strength
	form.dexterity.data = character.dexterity
	form.constitution.data = character.constitution
	form.intelligence.data = character.intelligence
	form.wisdom.data = character.wisdom
	form.charisma.data = character.charisma

	return render_template("characters/edit.html", form = form, character = character)

@app.route("/characters/<char_id>/", methods=["GET"])
@login_required
def character_view(char_id):
	character = Character.query.get(char_id)
	charClass = CharacterClass.query.get(character.class_id)
	form = LevelUpForm(maxhp=charClass.hitdice)
	form.maxhp = charClass.hitdice
	return render_template("sheets/sheet.html", sheet = CharacterSheet(char_id), form = form, armorform = ArmorForm(), editform=CharacterForm(), weaponform=EquipWeaponForm())

@app.route("/characters/levelup/<char_id>/", methods=["POST"])
@login_required
def character_level_up(char_id):
	form = LevelUpForm(request.form)
	character = Character.query.get(char_id)
	race = Race.query.get(character.race_id)
	charclass = CharacterClass.query.get(character.class_id)
	form.max = charclass.hitdice
	if not form.validate():
		return render_template("sheets/sheet.html", sheet=CharacterSheet(char_id), form = form, armorform=ArmorForm(), editform=CharacterForm())
	
	constitution = character.constitution + race.constitution
	conmod = StaticMethods.getModifier(constitution)

	if character.level < 20:
		hp = int(form.hpfield.data) + conmod
		if hp <= 0:
			hp = 1
		character.level_up(hp)
		db.session().commit()

	return redirect(url_for("character_view", char_id=char_id))

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

	return redirect(url_for("character_view", char_id=char_id))

@app.route("/characters/weapon/<char_id>/", methods=["POST"])
def character_equip_weapon(char_id):
	form = EquipWeaponForm(request.form)
	weapon = form.weapon.data
	character = Character.query.get(char_id)

	character.weapons.append(weapon)
	db.session().commit()

	return redirect(url_for("character_view", char_id = char_id))

@app.route("/characters/deleteweapon/<char_id>/<weapon_id>/", methods=["POST"])
def character_unequip_weapon(char_id,weapon_id):
	character_weapon = CharacterWeapons.query.get(weapon_id)
	db.session().delete(character_weapon)
	db.session().commit()

	return redirect(url_for("character_view", char_id=char_id))

@app.route("/characters/", methods=["POST"])
@login_required
def character_create():
	form = CharacterForm(request.form)
	race_id = form.race.data
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

	hp = class_id.hitdice + StaticMethods.getModifier(con + race_id.constitution)

	c = Character(name, hp, str, dex, con, intel, wis, cha)

	c.race_id = race_id.id
	c.class_id = class_id.id
	c.account_id = current_user.id

	db.session().add(c)
	db.session().commit()

	return redirect(url_for("characters_index"))

@app.route("/characters/edit/<char_id>/", methods=["POST"])
def character_edit(char_id):
	
	character = Character.query.get(char_id)	
	form = CharacterForm(request.form)

	if not form.validate():
		return render_template("characters/edit.html", form=form, character=character)

	race_id = form.race.data
	class_id = form.class_id.data

	name = form.name.data

	str = int(form.strength.data)
	dex = int(form.dexterity.data)
	con = int(form.constitution.data)
	intel = int(form.intelligence.data)
	wis = int(form.wisdom.data)
	cha = int(form.charisma.data)

	if character.class_id != class_id.id or character.race_id != race_id.id:
		hp = class_id.hitdice + StaticMethods.getModifier(con + race_id.constitution)
	else :
		hp = character.maxhp

	character.edit_character(name, str, dex, con, intel, wis, cha, class_id.id, race_id.id, hp)
	
	db.session().commit()

	return redirect(url_for("character_view", char_id=char_id))
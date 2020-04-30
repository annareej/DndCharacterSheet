from flask import flash,redirect, render_template, request, url_for
from flask_login import login_required, current_user

from application import app, db
from application.weapons.models import Weapon
from application.weapons.forms import CreateWeaponForm

from application.characters.models import CharacterWeapons

@app.route("/weapons/", methods=["GET"])
@login_required
def weapons_index():
	return render_template("weapons/list.html", weapons=Weapon.get_weapons_list(current_user.id), user_weapons=Weapon.get_user_weapons(current_user.id))

@app.route("/weapons/new/", methods=["GET"])
@login_required
def create_weapon_form():
    return render_template("weapons/new.html", form=CreateWeaponForm())

@app.route("/weapons/<weapon_id>/", methods=["GET"])
@login_required
def weapon_view(weapon_id):
    weapon = Weapon.query.get(weapon_id)
    return render_template("weapons/view.html", weapon=weapon)

@app.route("/weapons/edit/<weapon_id>/", methods=["GET"])
@login_required
def weapon_edit_form(weapon_id):
    weapon = Weapon.query.get(weapon_id)
    if weapon.created_by == current_user.id:
        form = CreateWeaponForm()
        
        form.name.data = weapon.name
        form.weapontype.data = weapon.type
        form.damagedice.data = weapon.damagedice
        form.diceamount.data = weapon.diceamount
        form.damagetype.data = weapon.damagetype
        form.magical.data = weapon.magical
        form.finesse.data = weapon.finesse
        
        return render_template('weapons/edit.html', form=form, weapon=weapon)

    return redirect(url_for('weapons_index'))

@app.route("/weapons/create", methods=["POST"])
@login_required
def weapon_create():
    form = CreateWeaponForm(request.form)
    
    name = form.name.data
    weapontype = form.weapontype.data
    damagedice = form.damagedice.data
    diceamount = form.diceamount.data
    damagetype = form.damagetype.data
    magical = form.magical.data
    
    if magical:
        bonus = form.bonus.data
    else:
        bonus = 0

    finesse = form.finesse.data
    public = form.public.data
Weapon()
    weapon = Weapon(name, damagedice, diceamount, damagetype, finesse, magical, bonus, weapontype, public)
    weapon.created_by = current_user.id

    db.session().add(weapon)
    db.session().commit()

    return redirect(url_for('weapons_index'))

@app.route("/weapons/editsave/<weapon_id>/", methods=["POST"])
@login_required
def weapon_edit(weapon_id):
    weapon = Weapon.query.get(weapon_id)
    form = CreateWeaponForm(request.form)

    weapon.name = form.name.data
    weapon.damagedice = form.damagedice.data
    weapon.diceamount = form.diceamount.data
    weapon.damagetype = form.damagetype.data
    weapon.magical = form.magical.data
    
    if weapon.magical:
        weapon.bonus = form.bonus.data
    else:
        weapon.bonus = 0
    
    weapon.finesse = form.finesse.data
    weapon.public = form.public.data
    db.session().commit()

    return redirect(url_for('weapon_view', weapon_id=weapon_id))

@app.route("/weapons/delete/<weapon_id>/", methods=["POST"])
@login_required
def weapon_remove(weapon_id):
    weapon = Weapon.query.get(weapon_id)
    character_weapons = CharacterWeapons.query.filter_by(weapon_id=weapon.id).all()
    for association in character_weapons:
        db.session().delete(association)

    db.session().delete(weapon)
    db.session().commit()

    return redirect(url_for("weapons_index"))
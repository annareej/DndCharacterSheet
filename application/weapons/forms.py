from application.weapons.models import Weapon
from application import app, db
from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import BooleanField, IntegerField, SelectField, StringField, validators
from wtforms.ext.sqlalchemy.fields import QuerySelectField

from sqlalchemy import or_

def weapon_choices():
    return db.session().query(Weapon).filter(or_(Weapon.public==True, Weapon.created_by==current_user.id)).all()

class EquipWeaponForm(FlaskForm):
    weapon = QuerySelectField('Weapon', query_factory=weapon_choices, allow_blank=False, get_label='name')

    class Meta:
        csrf = False

class CreateWeaponForm(FlaskForm):
    name = StringField("Weapon name", [validators.DataRequired(), validators.Length(max=144)])
    damagedice = SelectField("Select damage dice type",choices=[(4, 'd4'), (6, 'd6'), (8, 'd8'), (10,'d10'), (12,'d12')])
    diceamount = IntegerField("Dice amount", [validators.DataRequired(), validators.NumberRange(min=1, max=4)])
    damagetype = SelectField("Select damage type", choices=[('slashing', 'slashing'), ('bludgeoning','bludgeoning'),('piercing','piercing')])
    weapontype = SelectField("Select weapon type", choices=[(1,"Simple weapon"),(2,"Martial weapon")])
    finesse = BooleanField("Finesse")
    magical = BooleanField("Magic weapon")
    bonus = SelectField("Select enchantment", choices=[(0,'+ 0'), (1,'+ 1'), (2,'+ 2'), (3,'+ 3')])
    public = BooleanField("Make weapon public for others?")

    class Meta:
        csrf = False
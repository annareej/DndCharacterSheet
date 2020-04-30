from application.weapons.models import Weapon

from flask_wtf import FlaskForm
from wtforms import IntegerField, SelectField, StringField, validators
from wtforms.ext.sqlalchemy.fields import QuerySelectField

def weapon_choices():
    return Weapon.query.filter_by(public=True).all()

class EquipWeaponForm(FlaskForm):
    weapon = QuerySelectField('Weapon', query_factory=weapon_choices, allow_blank=False, get_label='name')

    class Meta:
        csrf = False
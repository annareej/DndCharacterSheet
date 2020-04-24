from application.armor.models import Armor

from flask_wtf import FlaskForm
from wtforms import IntegerField, SelectField, StringField, validators
from wtforms.ext.sqlalchemy.fields import QuerySelectField

def armor_choices():
    return Armor.query

class ArmorForm(FlaskForm):
    armor = QuerySelectField('Armor', query_factory=armor_choices, allow_blank=True, get_label='name')

    class Meta:
        csrf = False
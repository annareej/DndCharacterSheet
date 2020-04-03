from flask_wtf import FlaskForm
from wtforms import IntegerField, SelectField, StringField, validators
from wtforms.ext.sqlalchemy.fields import QuerySelectField

from application.races.models import Race

def race_choices():
	return Race.query

class CharacterForm(FlaskForm):
	name = StringField("Character name", [validators.InputRequired(), validators.Length(max=144)])
	strength = IntegerField("Strength", [validators.NumberRange(min=3, max=18)])
	dexterity = IntegerField("Dexterity", [validators.NumberRange(min=3, max=18)])
	constitution = IntegerField("Constitution", [validators.NumberRange(min=3, max=18)])
	intelligence = IntegerField("Intelligence", [validators.NumberRange(min=3, max=18)])
	wisdom = IntegerField("Wisdom", [validators.NumberRange(min=3, max=18)])
	charisma = IntegerField("Charisma", [validators.NumberRange(min=3, max=18)])

	race = QuerySelectField('Character race', query_factory=race_choices, allow_blank=False, get_label='name')
	
	class Meta:
		csrf = False
	

from flask import g
from flask_wtf import FlaskForm
from wtforms import IntegerField, SelectField, StringField, validators
from wtforms.ext.sqlalchemy.fields import QuerySelectField

from application import app
from application.races.models import Race
from application.classes.models import CharacterClass

def race_choices():
	return Race.query

def class_choices():
	return CharacterClass.query

def get_hit_die(class_id):
	charClass = CharacterClass.query.get(class_id)
	return charClass.hitdice

class CharacterForm(FlaskForm):
	name = StringField("Character name", [validators.DataRequired(), validators.Length(max=144)])
	strength = IntegerField("Strength", [validators.NumberRange(min=3, max=18)])
	dexterity = IntegerField("Dexterity", [validators.NumberRange(min=3, max=18)])
	constitution = IntegerField("Constitution", [validators.NumberRange(min=3, max=18)])
	intelligence = IntegerField("Intelligence", [validators.NumberRange(min=3, max=18)])
	wisdom = IntegerField("Wisdom", [validators.NumberRange(min=3, max=18)])
	charisma = IntegerField("Charisma", [validators.NumberRange(min=3, max=18)])

	race = QuerySelectField('Character race', query_factory=race_choices, allow_blank=False, get_label='name')
	class_id = QuerySelectField('Character class', query_factory=class_choices, allow_blank=False, get_label='name')

	
	class Meta:
		csrf = False
	
class LevelUpForm(FlaskForm):
	hpfield = IntegerField("Add hit points to maximum", [validators.DataRequired(), validators.NumberRange(min=1)])

	class Meta:
		csrf = False

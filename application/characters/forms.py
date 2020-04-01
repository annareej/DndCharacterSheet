from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, validators

class CharacterForm(FlaskForm):
	name = StringField("Character name", [validators.InputRequired()])
	strength = IntegerField("Strength", [validators.NumberRange(min=3, max=18)])
	dexterity = IntegerField("Dexterity", [validators.NumberRange(min=3, max=18)])
	constitution = IntegerField("Constitution", [validators.NumberRange(min=3, max=18)])
	intelligence = IntegerField("Intelligence", [validators.NumberRange(min=3, max=18)])
	wisdom = IntegerField("Wisdom", [validators.NumberRange(min=3, max=18)])
	charisma = IntegerField("Charisma", [validators.NumberRange(min=3, max=18)])

	class Meta:
		csrf = False

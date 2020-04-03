from application.characters.models import Character
from application.races.models import Race

class CharacterSheet:
	def __init__(sheet, char_id):
		character = Character.query.get(char_id)
		race = Race.query.get(character.race)
		sheet.char_id = character.id
		sheet.charname = character.name
		sheet.level = character.level
		sheet.racename = race.name
		sheet.speed = race.speed
		sheet.strength = character.strength + race.strength
		sheet.dexterity = character.dexterity + race.dexterity
		sheet.constitution = character.constitution + race.constitution
		sheet.intelligence = character.intelligence + race.intelligence
		sheet.wisdom = character.wisdom + race.wisdom
		sheet.charisma = character.charisma + race.charisma

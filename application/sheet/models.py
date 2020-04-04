from application.characters.models import Character
from application.races.models import Race

class CharacterSheet:
	def __init__(self, char_id):
		character = Character.query.get(char_id)
		race = Race.query.get(character.race)
		
		self.char_id = character.id
		self.charname = character.name
		self.level = character.level
		self.racename = race.name
		self.speed = race.speed

		strength = character.strength + race.strength
		self.strength = strength
		self.strmodifier = self.getModifier(strength)

		dexterity = character.dexterity + race.dexterity
		self.dexterity = dexterity
		self.dexmodifier = self.getModifier(dexterity)

		constitution = character.constitution + race.constitution
		self.constitution = constitution
		self.conmodifier = self.getModifier(constitution)

		intelligence = character.intelligence + race.intelligence
		self.intelligence = intelligence
		self.intmodifier = self.getModifier(intelligence)

		wisdom = character.wisdom + race.wisdom
		self.wisdom = wisdom
		self.wismodifier = self.getModifier(wisdom)

		charisma = character.charisma + race.charisma
		self.charisma = charisma
		self.chamodifier = self.getModifier(charisma)

		self.ac = 10 + self.dexmodifier

	def getModifier(self, score):
		modifier = -5
		if score == 2 or score == 3:
			modifier = -4
		elif score == 4 or score == 5:
			modifier = -3
		elif score == 6 or score == 7:
			modifier = -2
		elif score == 8 or score == 9:
			modifier = -1
		elif score == 10 or score == 11:
			modifier = 0
		elif score == 12 or score == 13:
			modifier = 1
		elif score == 14 or score == 15:
			modifier = 2
		elif score == 16 or score == 17:
			modifier = 3
		elif score == 18 or score == 19:
			modifier = 4
		elif score == 20:
			modifier = 5
			
		return modifier

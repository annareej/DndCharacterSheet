from application.characters.models import Character
from application.races.models import Race
from application.classes.models import CharacterClass
from application.armor.models import Armor
from application.staticmethods import StaticMethods

class CharacterSheet:
	def __init__(self, char_id):
		character = Character.query.get(char_id)
		race = Race.query.get(character.race_id)
		charclass = CharacterClass.query.get(character.class_id)
		
		self.character = character
		self.race = race
		self.charclass = charclass 
		self.profbonus = StaticMethods.getProficiencyBonus(character.level)
		
		strength = character.strength + race.strength
		self.strength = strength
		self.strmodifier = StaticMethods.getModifier(strength)

		dexterity = character.dexterity + race.dexterity
		self.dexterity = dexterity
		self.dexmodifier = StaticMethods.getModifier(dexterity)

		constitution = character.constitution + race.constitution
		self.constitution = constitution
		self.conmodifier = StaticMethods.getModifier(constitution)

		intelligence = character.intelligence + race.intelligence
		self.intelligence = intelligence
		self.intmodifier = StaticMethods.getModifier(intelligence)

		wisdom = character.wisdom + race.wisdom
		self.wisdom = wisdom
		self.wismodifier = StaticMethods.getModifier(wisdom)

		charisma = character.charisma + race.charisma
		self.charisma = charisma
		self.chamodifier = StaticMethods.getModifier(charisma)

		armor = Armor.query.get(character.armor_id)
		if not armor:
			armor_name = "None"
		else:
			armor_name = armor.name

		self.ac = character.get_armor_class()
		self.armor = armor_name

		self.hitdie = charclass.hitdice

		self.weapons = character.get_character_weapons()

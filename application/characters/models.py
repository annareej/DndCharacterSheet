from application import db
from application.models import Base

from application.classes.models import CharacterClass
from application.armor.models import Armor,ArmorType
from application.races.models import Race

from application.staticmethods import StaticMethods
from sqlalchemy.sql import text

class CharacterWeapons(Base):
	__tablename__ = 'character_weapons'
	character_id = db.Column(db.String(144), db.ForeignKey('character.id'), nullable=False)
	weapon_id = db.Column(db.String(144), db.ForeignKey('weapon.id'), nullable=False)

	character = db.relationship('Character', backref=db.backref('weapon_characters', cascade='all, delete-orphan'))
	weapon = db.relationship('Weapon', backref=db.backref('character_weapons', cascade='all, delete-orphan'))

class Character(Base):
	name = db.Column(db.String(144), nullable=False)
	level = db.Column(db.Integer, nullable=False)
	maxhp = db.Column(db.Integer, nullable=False)
	
	strength = db.Column(db.Integer, nullable=False)
	dexterity = db.Column(db.Integer, nullable=False)
	constitution = db.Column(db.Integer, nullable=False)
	intelligence = db.Column(db.Integer, nullable=False)
	wisdom = db.Column(db.Integer, nullable=False)
	charisma = db.Column(db.Integer, nullable=False)

	race_id = db.Column(db.Integer, db.ForeignKey("race.id"), nullable=False)
	class_id = db.Column(db.Integer, db.ForeignKey("class.id"), nullable=False)

	armor_id = db.Column(db.Integer, db.ForeignKey("armor.id"))

	account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)

	weapons = db.relationship("Weapon", secondary="character_weapons")

	def __init__(self, name, hp, str, dex, con, intel, wis, cha):
		self.name = name
		self.level = 1
		self.maxhp = hp
		self.strength = str
		self.dexterity = dex
		self.constitution = con
		self.intelligence = intel
		self.wisdom = wis
		self.charisma = cha

	def add_armor(self, armor_id):
		self.armor_id = armor_id
	
	def level_up(self, hp):
		self.level += 1
		self.maxhp += hp

	def edit_character(self, name, str, dex, con, int, wis, cha, class_id, race_id, hp):
		self.name = name
		
		self.strength = str
		self.dexterity = dex
		self.constitution = con
		self.intelligence = int
		self.wisdom = wis
		self.charisma = cha
		
		if class_id != self.class_id or race_id != self.race_id:
			self.level = 1
		
		self.class_id = class_id
		self.race_id = race_id
		
		self.maxhp = hp

	def get_character_weapons(self):
		stmt = text("SELECT cw.id, w.name, w.damagedice, w.diceamount, w.damagetype, w.finesse, w.magical, w.bonus, c.strength, c.dexterity, c.level, race.strength, race.dexterity "
					"FROM weapon w "
						"JOIN character_weapons cw ON cw.weapon_id = w.id "
						"JOIN character c ON cw.character_id = c.id "
						"JOIN race ON c.race_id = race.id "
					"WHERE c.id = :character_id").params(character_id = self.id)

		res = db.engine.execute(stmt)

		response = []
		for row in res:
			weapon_name = row[1]
			damage = str(row[3]) + "d" + str(row[2])
			finesse = row[5]
			magical = row[6]
			bonus = int(row[7])
			level = int(row[10])
			profbonus = StaticMethods.getProficiencyBonus(level)
			dexterity = int(row[9]) + int(row[12])
			strength = int(row[8]) + int(row[11])
			if(finesse):
				if(dexterity > strength):
					atkmodifier = StaticMethods.getModifier(dexterity) + profbonus + bonus
					damagebonus = StaticMethods.getModifier(dexterity) + bonus
				else:
					atkmodifier = StaticMethods.getModifier(strength) + profbonus + bonus
					damagebonus = StaticMethods.getModifier(strength) + bonus					
			else:
				atkmodifier = StaticMethods.getModifier(strength) + profbonus + bonus
				damagebonus = StaticMethods.getModifier(strength) + bonus
			
			damagetype = ""
			if(magical):
				damagetype = "magical "
			damagetype += row[4]

			damagerow = damage 
			if(damagebonus > -1):
				damagerow += " + " + str(damagebonus)
			else:
				negative, bonus = str(damagebonus)
				damagerow += " - " + bonus 
			
			damagerow += " " + damagetype

			response.append({
				"association_id": row[0],
				"weapon_name": weapon_name,
				"atk_bonus": atkmodifier,
				"damage": damagerow
			})
		
		return response

	def get_armor_class(self):
		armor = Armor.query.get(self.armor_id)
		race = Race.query.get(self.race_id)
		dexmod = StaticMethods.getModifier(self.dexterity + race.dexterity)
		ac = 10 + dexmod
		
		if not armor:
			charClass = CharacterClass.query.get(self.class_id)
			if charClass.name == "Barbarian":
				ac += StaticMethods.getModifier(self.constitution + race.constitution)
			elif charClass.name == "Monk":
				ac += StaticMethods.getModifier(self.wisdom + race.wisdom)
		else:
			ac = armor.ac
			if armor.type == ArmorType.LIGHT.value:
				ac += dexmod
			elif armor.type == ArmorType.MEDIUM.value:
				if dexmod > 2:
					ac += 2
				else:
					ac += dexmod
		return ac
	
	@staticmethod
	def get_user_characters(account_id):
		stmt = text(
			"SELECT c.id, c.name, race.name, class.name, c.level "
			"FROM character c "
				"LEFT JOIN race ON c.race_id = race.id "
				"LEFT JOIN class ON c.class_id = class.id "
			"WHERE c.account_id = :account_id;"
		).params(account_id=account_id)
		res = db.engine.execute(stmt)

		response = []
		for row in res:
			response.append({ "character_id":row[0],"character_name":row[1], "race_name": row[2], "class_name": row[3], "level": row[4] })

		return response

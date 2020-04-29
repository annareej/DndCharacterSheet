from application import db
from application.models import Base

from sqlalchemy.sql import text

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

from application import db
from application.models import Base

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
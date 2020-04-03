from application import db
from application.models import Base

class Race(Base):
	__tablename__ = 'Race'

	name = db.Column(db.String(144), nullable=False)
	speed = db.Column(db.Integer, nullable=False)
	strength = db.Column(db.Integer, nullable=False)
	dexterity = db.Column(db.Integer, nullable=False)
	constitution = db.Column(db.Integer, nullable=False)
	intelligence = db.Column(db.Integer, nullable=False)
	wisdom = db.Column(db.Integer, nullable=False)
	charisma = db.Column(db.Integer, nullable=False)
	type = db.Column(db.Integer, nullable=False)

	def __init__(self, name, speed, str, con, intel, wis, cha, type):
		self.name = name
		self.speed = speed,
		self.strength = str
		self.dexterity = dex
		self.constitution = con
		self.intelligence = intel
		self.wisdom = wis
		self.charisma = cha
		self.type = type

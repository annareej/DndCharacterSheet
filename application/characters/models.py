from application import db
from application.models import Base

from sqlalchemy import text

class Character(Base):
	name = db.Column(db.String(144), nullable=False)
	level = db.Column(db.Integer, nullable=False)
	strength = db.Column(db.Integer, nullable=False)
	dexterity = db.Column(db.Integer, nullable=False)
	constitution = db.Column(db.Integer, nullable=False)
	intelligence = db.Column(db.Integer, nullable=False)
	wisdom = db.Column(db.Integer, nullable=False)
	charisma = db.Column(db.Integer, nullable=False)

	race = db.Column(db.Integer, db.ForeignKey("Race.id"), nullable=False)

	account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)

	def __init__(self, name, str, dex, con, intel, wis, cha):
		self.name = name
		self.level = 1
		self.strength = str
		self.dexterity = dex
		self.constitution = con
		self.intelligence = intel
		self.wisdom = wis
		self.charisma = cha

	@staticmethod
	def get_character_sheet(char_id):
		stmt = text("SELECT c.name AS cname, r.name AS rname, r.speed," 
					"c.strength + r.strength AS str,"
					"c.dexterity + r.dexterity AS dex,"
					"c.constitution + r.constitution AS con,"
					"c.intelligence + r.intelligence AS intel,"
					"c.wisdom + r.wisdom AS wis,"
					"c.charisma + r.charisma AS cha" 
					" FROM character c"
					" LEFT JOIN Race r ON r.id = c.race"
					" WHERE c.id =" + char_id + ";")
		res = db.engine.execute(stmt)
		sheet = {}
		for row in res:
			sheet.append({"charname":row['cname'], "racename":row['rname']})

		print(sheet)
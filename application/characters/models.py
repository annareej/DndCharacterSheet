from application import db

class Character(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
	date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
	onupdate=db.func.current_timestamp())

	name = db.Column(db.String(144), nullable=False)
	level = db.Column(db.Integer, nullable=False)
	strength = db.Column(db.Integer, nullable=False)
	dexterity = db.Column(db.Integer, nullable=False)
	constitution = db.Column(db.Integer, nullable=False)
	intelligence = db.Column(db.Integer, nullable=False)
	wisdom = db.Column(db.Integer, nullable=False)
	charisma = db.Column(db.Integer, nullable=False)

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

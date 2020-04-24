from application import db, bcrypt
from application.models import Base

class User(Base):

	__tablename__ = "account"

	name = db.Column(db.String(144), nullable=False)
	username = db.Column(db.String(144), nullable=False)
	password = db.Column(db.String(144), nullable=False)

	characters = db.relationship("Character", backref='account', lazy=True)

	def __init__(self, name, username, password):
		self.name = name
		self.username = username
		self.password = bcrypt.generate_password_hash(password).decode('UTF-8')

	def get_id(self):
		return self.id

	def is_active(self):
		return True

	def is_anonymous(self):
		return False

	def is_authenticated(self):
		return True

	def change_password(self, password):
		self.password = bcrypt.generate_password_hash(password).decode('UTF-8')

from application import app, db
from application.models import Base
from enum import Enum

class ArmorType(Enum):
    LIGHT = 1
    MEDIUM = 2
    HEAVY = 3

class Armor(Base):

    __tablename__ = 'armor'

    name = db.Column(db.String(144), nullable=False)
    ac = db.Column(db.Integer, nullable=False)
    dexmod = db.Column(db.Boolean, nullable=False)
    type = db.Column(db.Integer, nullable=False)

    def __init__(self, name, ac, dexmod, type):
        self.name = name
        self.ac = ac
        self.dexmod = dexmod
        self.type = type
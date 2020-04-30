from application import app, db
from application.models import Base
from enum import Enum

class DamageType(Enum):
    bludgeoning = "bludgeoning"
    piercing = "piercing"
    slashing = "slashing"

class WeaponType(Enum):
    SIMPLE = 1
    SIMPLERANGED = 2
    MARTIAL = 3
    MARTIALRANGED = 4

class Weapon(Base):

    __tablename__ = 'weapon'

    name = db.Column(db.String(144), nullable=False)
    damagedice = db.Column(db.Integer, nullable=False)
    diceamount = db.Column(db.Integer, nullable=False)
    damagetype = db.Column(db.String(144), nullable=False)
    finesse = db.Column(db.Boolean, nullable=False)
    magical = db.Column(db.Boolean, nullable=False)
    bonus = db.Column(db.Integer, nullable=False)
    type = db.Column(db.Integer, nullable=False)

    created_by = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=True)
    public = db.Column(db.Boolean, nullable=False)

    def __init__(self, name, damagedice, diceamount, damagetype, finesse, magical, bonus, type, public):
        self.name = name
        self.damagedice = damagedice
        self.diceamount = diceamount
        self.damagetype = damagetype
        self.finesse = finesse
        self.magical = magical
        self.bonus = bonus
        self.type = type
        self.public = public

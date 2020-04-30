from application import app, db
from application.models import Base
from enum import Enum
from sqlalchemy.sql import text

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

    characters = db.relationship("Character", secondary="character_weapons")

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

    @staticmethod
    def get_weapons_list(user_id):
        stmt = text(
            "SELECT weapon.id, weapon.name, COUNT(character_weapons.character_id) "
            "FROM weapon "
                "LEFT JOIN character_weapons ON character_weapons.weapon_id = weapon.id "
            "WHERE weapon.public = 1 AND (weapon.created_by IS NOT NULL AND NOT weapon.created_by = :user_id) "
            "GROUP BY weapon.id;"
        ).params(user_id = user_id)
        res = db.engine.execute(stmt)
        
        response = []
        for row in res:
            response.append({
                "weapon_id":row[0], 
                "weapon_name":row[1],
                "character_count":row[2] 
            })
            
        return response
    
    @staticmethod
    def get_user_weapons(user_id):
        stmt = text(
            "SELECT weapon.id, weapon.name, COUNT(character_weapons.character_id) "
            "FROM weapon "
                "LEFT JOIN character_weapons ON character_weapons.weapon_id = weapon.id "
            "WHERE weapon.created_by = :user_id "
            "GROUP BY weapon.id;"
        ).params(user_id=user_id)

        res = db.engine.execute(stmt)

        response = []
        for row in res:
            response.append({
                "weapon_id":row[0],
                "weapon_name":row[1],
                "character_count":row[2]
            })

        return response

from application import db
from application.models import Base

class CharacterClass(Base):
    
    __tablename__ = 'class'

    name = db.Column(db.String(144), nullable=False)
    hitdice = db.Column(db.Integer, nullable=False)

    def __init__(self, name, hitdice):
        self.name = name
        self.hitdice = hitdice
        
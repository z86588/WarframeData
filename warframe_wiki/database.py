from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, JSON, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from .settings import DATABASE_URL

Base = declarative_base()

class BaseModel(Base):
    __abstract__ = True
    
    id = Column(String, primary_key=True)
    name_en = Column(String)
    name_zh = Column(String)
    name_alias = Column(String)
    description_en = Column(String)
    description_zh = Column(String)
    image_url = Column(String)
    wiki_url = Column(String)
    last_updated = Column(DateTime, default=datetime.utcnow)

class Warframe(BaseModel):
    __tablename__ = 'warframes'
    
    health = Column(Float)
    shield = Column(Float)
    armor = Column(Float)
    energy = Column(Float)
    sprint_speed = Column(Float)
    abilities_en = Column(JSON)
    abilities_zh = Column(JSON)
    passive_en = Column(String)
    passive_zh = Column(String)
    mastery_rank = Column(Integer)
    polarities = Column(JSON)

class Weapon(BaseModel):
    __tablename__ = 'weapons'
    
    type = Column(String)
    mastery_rank = Column(Integer)
    damage = Column(JSON)
    critical_chance = Column(Float)
    critical_multiplier = Column(Float)
    status_chance = Column(Float)
    fire_rate = Column(Float)
    accuracy = Column(Float)
    magazine_size = Column(Integer)
    reload_time = Column(Float)
    disposition = Column(Integer)

class Mod(BaseModel):
    __tablename__ = 'mods'
    
    polarity = Column(String)
    rarity = Column(String)
    drain = Column(Integer)
    max_rank = Column(Integer)
    effect_en = Column(String)
    effect_zh = Column(String)
    tradable = Column(Boolean)
    mod_set = Column(String)
    base_effects = Column(JSON)
    upgrade_effects = Column(JSON)

def init_db():
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine)() 
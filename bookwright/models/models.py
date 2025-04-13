from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship
from .base import Base
import json

# Association tables for many-to-many relationships
character_scene = Table('character_scene', Base.metadata,
    Column('character_id', Integer, ForeignKey('characters.id')),
    Column('scene_id', Integer, ForeignKey('scenes.id'))
)

scene_chapter = Table('scene_chapter', Base.metadata,
    Column('scene_id', Integer, ForeignKey('scenes.id')),
    Column('chapter_id', Integer, ForeignKey('chapters.id'))
)

class Book(Base):
    __tablename__ = 'book_info'
    
    id = Column(Integer, primary_key=True)
    title = Column(String(255))
    author = Column(String(255))
    genre = Column(String(255))
    summary = Column(Text)
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

class Character(Base):
    __tablename__ = 'characters'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True)
    role = Column(String(255))
    physical_description = Column(Text)
    personality_traits = Column(Text)
    background = Column(Text)
    motivation = Column(Text)
    relationships = Column(Text)
    skills = Column(Text)
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    scenes = relationship("Scene", secondary=character_scene, back_populates="characters")

class Scene(Base):
    __tablename__ = 'scenes'
    
    id = Column(Integer, primary_key=True)
    title = Column(String(255), unique=True)
    description = Column(Text)
    location = Column(String(255))
    day = Column(String(255))
    time = Column(String(255))
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    characters = relationship("Character", secondary=character_scene, back_populates="scenes")
    chapters = relationship("Chapter", secondary=scene_chapter, back_populates="scenes")

class Chapter(Base):
    __tablename__ = 'chapters'
    
    id = Column(Integer, primary_key=True)
    title = Column(String(255), unique=True)
    description = Column(Text)
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    scenes = relationship("Scene", secondary=scene_chapter, back_populates="chapters") 
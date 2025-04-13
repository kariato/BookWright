# bookwright/utils/database_manager.py
from sqlalchemy.orm import Session
from typing import List, Optional, Dict
from ..models.models import Book, Character, Scene, Chapter
from ..models.base import Base, engine

class StoryDatabase:
    def __init__(self):
        # Create all tables
        Base.metadata.create_all(bind=engine)
    
    def save_book_info(self, db: Session, title: str, author: str, genre: str, summary: str, notes: str) -> None:
        book = db.query(Book).first()
        if book:
            book.title = title
            book.author = author
            book.genre = genre
            book.summary = summary
            book.notes = notes
        else:
            book = Book(
                title=title,
                author=author,
                genre=genre,
                summary=summary,
                notes=notes
            )
            db.add(book)
        db.commit()
    
    def get_book_info(self, db: Session) -> Optional[Dict]:
        book = db.query(Book).first()
        if book:
            return {
                "title": book.title,
                "author": book.author,
                "genre": book.genre,
                "summary": book.summary,
                "notes": book.notes
            }
        return None
    
    def save_character(self, db: Session, character_data: Dict) -> None:
        character = db.query(Character).filter(Character.name == character_data["name"]).first()
        if character:
            for key, value in character_data.items():
                setattr(character, key, value)
        else:
            character = Character(**character_data)
            db.add(character)
        db.commit()
    
    def get_characters(self, db: Session) -> List[Dict]:
        characters = db.query(Character).all()
        return [{
            "name": c.name,
            "role": c.role,
            "physical_description": c.physical_description,
            "personality_traits": c.personality_traits,
            "background": c.background,
            "motivation": c.motivation,
            "relationships": c.relationships,
            "skills": c.skills,
            "notes": c.notes
        } for c in characters]
    
    def delete_character(self, db: Session, name: str) -> None:
        character = db.query(Character).filter(Character.name == name).first()
        if character:
            db.delete(character)
            db.commit()
    
    def save_scene(self, db: Session, scene_data: Dict) -> None:
        scene = db.query(Scene).filter(Scene.title == scene_data["title"]).first()
        if scene:
            for key, value in scene_data.items():
                if key != "characters":  # Handle characters separately
                    setattr(scene, key, value)
        else:
            scene = Scene(**{k: v for k, v in scene_data.items() if k != "characters"})
            db.add(scene)
        
        # Handle character relationships
        if "characters" in scene_data:
            characters = []
            for char_name in scene_data["characters"]:
                character = db.query(Character).filter(Character.name == char_name).first()
                if character:
                    characters.append(character)
            scene.characters = characters
        
        db.commit()
    
    def get_scenes(self, db: Session) -> List[Dict]:
        scenes = db.query(Scene).all()
        return [{
            "title": s.title,
            "description": s.description,
            "location": s.location,
            "day": s.day,
            "time": s.time,
            "characters": [c.name for c in s.characters],
            "notes": s.notes
        } for s in scenes]
    
    def delete_scene(self, db: Session, title: str) -> None:
        scene = db.query(Scene).filter(Scene.title == title).first()
        if scene:
            db.delete(scene)
            db.commit()
    
    def save_chapter(self, db: Session, chapter_data: Dict) -> None:
        chapter = db.query(Chapter).filter(Chapter.title == chapter_data["title"]).first()
        if chapter:
            for key, value in chapter_data.items():
                if key != "scenes":  # Handle scenes separately
                    setattr(chapter, key, value)
        else:
            chapter = Chapter(**{k: v for k, v in chapter_data.items() if k != "scenes"})
            db.add(chapter)
        
        # Handle scene relationships
        if "scenes" in chapter_data:
            scenes = []
            for scene_title in chapter_data["scenes"]:
                scene = db.query(Scene).filter(Scene.title == scene_title).first()
                if scene:
                    scenes.append(scene)
            chapter.scenes = scenes
        
        db.commit()
    
    def get_chapters(self, db: Session) -> List[Dict]:
        chapters = db.query(Chapter).all()
        return [{
            "title": c.title,
            "description": c.description,
            "notes": c.notes,
            "scenes": [s.title for s in c.scenes]
        } for c in chapters]
    
    def delete_chapter(self, db: Session, title: str) -> None:
        chapter = db.query(Chapter).filter(Chapter.title == title).first()
        if chapter:
            db.delete(chapter)
            db.commit()

class DatabaseManager:
    def __init__(self, scenes_manager, characters_manager, chapters_manager):
        self.scenes_manager = scenes_manager
        self.characters_manager = characters_manager
        self.chapters_manager = chapters_manager
        self.db = StoryDatabase()
    
    def export_data(self) -> Dict:
        """Export all data as a JSON-compatible dictionary"""
        return {
            "export_date": datetime.now().isoformat(),
            "book_info": self.db.get_book_info(),
            "scenes": self.db.get_scenes(),
            "characters": self.db.get_characters(),
            "chapters": self.db.get_chapters()
        }
    
    def export_to_json(self) -> str:
        """Export all data as a JSON string"""
        data = self.export_data()
        return json.dumps(data, indent=2)

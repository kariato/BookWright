from typing import Dict, Any, List
from datetime import datetime
import json
from pathlib import Path

class AppData:
    def __init__(self, db_manager):
        self.db_manager = db_manager
        
    def get_current_state(self) -> Dict[str, Any]:
        """Get the current state of the application as JSON"""
        return {
            "timestamp": datetime.now().isoformat(),
            "book_info": self.db_manager.get_book_info(),
            "characters": self.db_manager.get_characters(),
            "scenes": self.db_manager.get_scenes(),
            "chapters": self.db_manager.get_chapters()
        }
    
    def save_state(self, file_path: str) -> None:
        """Save the current state to a JSON file"""
        state = self.get_current_state()
        with open(file_path, 'w') as f:
            json.dump(state, f, indent=2)
    
    def load_state(self, file_path: str) -> Dict[str, Any]:
        """Load application state from a JSON file"""
        with open(file_path, 'r') as f:
            return json.load(f)
    
    def get_character_context(self, character_id: str) -> Dict[str, Any]:
        """Get detailed context for a specific character"""
        characters = self.db_manager.get_characters()
        character = next((c for c in characters if c["id"] == character_id), None)
        if not character:
            return {}
            
        # Get related scenes
        scenes = self.db_manager.get_scenes()
        character_scenes = [s for s in scenes if character["name"] in s.get("characters", [])]
        
        # Get related chapters
        chapters = self.db_manager.get_chapters()
        character_chapters = []
        for chapter in chapters:
            chapter_scenes = [s for s in scenes if s["title"] in chapter.get("scenes", [])]
            if any(s in character_scenes for s in chapter_scenes):
                character_chapters.append(chapter)
        
        return {
            "character": character,
            "scenes": character_scenes,
            "chapters": character_chapters,
            "book_info": self.db_manager.get_book_info()
        }
    
    def get_scene_context(self, scene_id: str) -> Dict[str, Any]:
        """Get detailed context for a specific scene"""
        scenes = self.db_manager.get_scenes()
        scene = next((s for s in scenes if s["id"] == scene_id), None)
        if not scene:
            return {}
            
        # Get related characters
        characters = self.db_manager.get_characters()
        scene_characters = [c for c in characters if c["name"] in scene.get("characters", [])]
        
        # Get related chapters
        chapters = self.db_manager.get_chapters()
        scene_chapters = [c for c in chapters if scene["title"] in c.get("scenes", [])]
        
        return {
            "scene": scene,
            "characters": scene_characters,
            "chapters": scene_chapters,
            "book_info": self.db_manager.get_book_info()
        } 
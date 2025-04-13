from typing import Dict, Any
from .llm_service import LLMService
from .app_data import AppData
from ..utils.database_manager import StoryDatabase
import json

def main():
    # Initialize the database manager
    db_manager = StoryDatabase()
    
    # Initialize the app data handler
    app_data = AppData(db_manager)
    
    # Initialize the LLM service
    llm_service = LLMService(prompts_dir="bookwright/llm/prompts")
    
    # Example 1: Character Development
    character_id = "character_1"  # Replace with actual character ID
    character_context = app_data.get_character_context(character_id)
    
    # Generate character development suggestions
    response = llm_service.generate(
        prompt_name="character_development",
        app_data=character_context
    )
    
    print("Character Development Suggestions:")
    print(json.dumps(response, indent=2))
    
    # Example 2: Scene Analysis
    scene_id = "scene_1"  # Replace with actual scene ID
    scene_context = app_data.get_scene_context(scene_id)
    
    # Generate scene analysis
    response = llm_service.generate(
        prompt_name="ollama_main",
        app_data={
            "user_input": "Analyze this scene and suggest improvements",
            "app_data": scene_context
        }
    )
    
    print("\nScene Analysis:")
    print(json.dumps(response, indent=2))

if __name__ == "__main__":
    main() 
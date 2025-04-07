import gradio as gr
from typing import List, Dict, Optional
from bookwright.core.llm_interface import OllamaClient

class CharactersManager:
    def __init__(self, scenes_manager):
        self.characters: List[Dict] = []
        self.scenes_manager = scenes_manager
        self.llm = OllamaClient(model='deepseek')
        
    def set_scenes(self, scenes: List[Dict]):
        """Set the scenes list from ScenesManager"""
        self.scenes_manager.scenes = scenes
        
    def create_characters_interface(self) -> gr.Blocks:
        """Create and return the Gradio interface for characters management"""
        with gr.Blocks() as characters_interface:
            gr.Markdown("### Manage Characters")
            
            with gr.Row():
                with gr.Column(scale=2):
                    # Basic Information
                    character_name = gr.Textbox(label="Character Name")
                    character_role = gr.Dropdown(
                        choices=["Protagonist", "Antagonist", "Supporting", "Minor"],
                        label="Role in Story"
                    )
                    
                    # Physical Description
                    with gr.Group():
                        gr.Markdown("#### Physical Description")
                        appearance = gr.TextArea(label="Appearance", lines=3, placeholder="Physical characteristics, clothing style, etc.")
                        age = gr.Number(label="Age", precision=0)
                        gender = gr.Dropdown(
                            choices=["Male", "Female", "Non-binary", "Other"],
                            label="Gender"
                        )
                    
                    # Personality and Background
                    with gr.Group():
                        gr.Markdown("#### Personality and Background")
                        personality = gr.TextArea(label="Personality Traits", lines=3, placeholder="Key personality traits, mannerisms, etc.")
                        background = gr.TextArea(label="Background", lines=3, placeholder="History, upbringing, important life events")
                        motivation = gr.TextArea(label="Motivation", lines=2, placeholder="What drives this character?")
                    
                    # Relationships and Skills
                    with gr.Group():
                        gr.Markdown("#### Relationships and Skills")
                        relationships = gr.TextArea(label="Relationships", lines=3, placeholder="Key relationships with other characters")
                        skills = gr.TextArea(label="Skills/Abilities", lines=2, placeholder="Special abilities, talents, or skills")
                    
                    # Character's Scenes
                    with gr.Group():
                        gr.Markdown("#### Character's Scenes")
                        character_scenes = gr.Dataframe(
                            headers=["Scene Title", "Day", "Time", "Location", "Role in Scene", "Scene Notes"],
                            datatype=["str", "str", "str", "str", "str", "str"],
                            col_count=(6, "fixed"),
                            interactive=True
                        )
                        
                        with gr.Row():
                            update_scene_button = gr.Button("Update Scene Details")
                            add_to_scene_button = gr.Button("Add to New Scene")
                    
                    # Additional Notes
                    notes = gr.TextArea(label="Additional Notes", lines=4, placeholder="Any other important information about the character")
                    
                    with gr.Row():
                        save_button = gr.Button("Save Character")
                        clear_button = gr.Button("Clear Form")
                    
                    status = gr.Markdown("Status: _No character saved yet_")
            
            with gr.Column(scale=1):
                characters_list = gr.Dataframe(
                    headers=["Name", "Role", "Age", "Gender"],
                    datatype=["str", "str", "number", "str"],
                    col_count=(4, "fixed")
                )
                
                load_button = gr.Button("Load Selected Character")
                delete_button = gr.Button("Delete Selected Character")
            
            # Connect buttons to functions
            save_button.click(
                fn=self.save_character,
                inputs=[
                    character_name, character_role, appearance, age, gender,
                    personality, background, motivation, relationships, skills, notes
                ],
                outputs=[status, characters_list, character_scenes]
            )
            
            clear_button.click(
                fn=self.clear_form,
                inputs=[],
                outputs=[
                    character_name, character_role, appearance, age, gender,
                    personality, background, motivation, relationships, skills, notes,
                    character_scenes
                ]
            )
            
            load_button.click(
                fn=self.load_character,
                inputs=[characters_list],
                outputs=[
                    character_name, character_role, appearance, age, gender,
                    personality, background, motivation, relationships, skills, notes,
                    character_scenes
                ]
            )
            
            delete_button.click(
                fn=self.delete_character,
                inputs=[characters_list],
                outputs=[status, characters_list, character_scenes]
            )
            
            update_scene_button.click(
                fn=self.update_scene_details,
                inputs=[character_name, character_scenes],
                outputs=[status, character_scenes]
            )
            
            add_to_scene_button.click(
                fn=self.add_to_new_scene,
                inputs=[character_name],
                outputs=[status, character_scenes]
            )
            
            # Initialize characters list
            characters_list.value = self.get_characters_list()
            
        return characters_interface
    
    def get_character_scenes(self, character_name: str) -> List[List[str]]:
        """Get all scenes where this character appears"""
        if not character_name:
            return []
            
        character_scenes = []
        for scene in self.scenes_manager.scenes:
            if character_name in scene.get("characters", []):
                character_scenes.append([
                    scene["title"],
                    scene["day"],
                    scene["time"],
                    scene["location"],
                    scene.get("character_roles", {}).get(character_name, "Supporting"),
                    scene.get("character_notes", {}).get(character_name, "")
                ])
        return character_scenes
    
    def update_scene_details(self, character_name: str, scenes_data: List[List[str]]) -> tuple:
        """Update the character's details for specific scenes"""
        if not character_name or not scenes_data:
            return "No character or scenes selected", []
            
        for scene_data in scenes_data:
            scene_title = scene_data[0]
            scene_role = scene_data[4]
            scene_notes = scene_data[5]
            
            # Find the scene and update character details
            for scene in self.scenes_manager.scenes:
                if scene["title"] == scene_title:
                    if "character_roles" not in scene:
                        scene["character_roles"] = {}
                    if "character_notes" not in scene:
                        scene["character_notes"] = {}
                    
                    scene["character_roles"][character_name] = scene_role
                    scene["character_notes"][character_name] = scene_notes
                    
        return f"Updated scene details for {character_name}", self.get_character_scenes(character_name)
    
    def add_to_new_scene(self, character_name: str) -> tuple:
        """Add the character to a new scene"""
        if not character_name:
            return "No character selected", []
            
        # Create a new scene with the character
        new_scene = {
            "title": f"New Scene with {character_name}",
            "day": "Day 1",
            "time": "Morning",
            "location": "New Location",
            "characters": [character_name],
            "character_roles": {character_name: "Supporting"},
            "character_notes": {character_name: ""}
        }
        
        self.scenes_manager.scenes.append(new_scene)
        return f"Added {character_name} to new scene", self.get_character_scenes(character_name)
    
    def save_character(self, name: str, role: str, appearance: str, age: int, gender: str,
                      personality: str, background: str, motivation: str,
                      relationships: str, skills: str, notes: str) -> tuple:
        """Save a new character or update an existing one"""
        character = {
            "name": name,
            "role": role,
            "appearance": appearance,
            "age": age,
            "gender": gender,
            "personality": personality,
            "background": background,
            "motivation": motivation,
            "relationships": relationships,
            "skills": skills,
            "notes": notes
        }
        
        # Check if character with this name already exists
        existing_index = next((i for i, c in enumerate(self.characters) if c["name"] == name), None)
        
        if existing_index is not None:
            self.characters[existing_index] = character
            status = f"Updated character: {name}"
        else:
            self.characters.append(character)
            status = f"Saved new character: {name}"
            
        return status, self.get_characters_list(), self.get_character_scenes(name)
    
    def get_characters_list(self) -> List[List]:
        """Return a list of characters in the format expected by the Dataframe"""
        return [[c["name"], c["role"], c["age"], c["gender"]] for c in self.characters]
    
    def load_character(self, selected_characters: List[List]) -> tuple:
        """Load a character's details into the form"""
        if not selected_characters:
            return "", "", "", 0, "", "", "", "", "", "", "", []
            
        selected_name = selected_characters[0][0]  # First column is name
        character = next((c for c in self.characters if c["name"] == selected_name), None)
        
        if character:
            return (
                character["name"],
                character["role"],
                character["appearance"],
                character["age"],
                character["gender"],
                character["personality"],
                character["background"],
                character["motivation"],
                character["relationships"],
                character["skills"],
                character["notes"],
                self.get_character_scenes(selected_name)
            )
        return "", "", "", 0, "", "", "", "", "", "", "", []
    
    def delete_character(self, selected_characters: List[List]) -> tuple:
        """Delete the selected character"""
        if not selected_characters:
            return "No character selected", self.get_characters_list(), []
            
        selected_name = selected_characters[0][0]
        self.characters = [c for c in self.characters if c["name"] != selected_name]
        
        # Remove character from all scenes
        for scene in self.scenes_manager.scenes:
            if selected_name in scene.get("characters", []):
                scene["characters"].remove(selected_name)
                if "character_roles" in scene:
                    scene["character_roles"].pop(selected_name, None)
                if "character_notes" in scene:
                    scene["character_notes"].pop(selected_name, None)
        
        return f"Deleted character: {selected_name}", self.get_characters_list(), []
    
    def clear_form(self) -> tuple:
        """Clear all form fields"""
        return "", "", "", 0, "", "", "", "", "", "", "", [] 
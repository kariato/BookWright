import gradio as gr
from typing import List, Dict, Optional
from bookwright.core.llm_interface import OllamaClient

class ScenesManager:
    def __init__(self):
        self.scenes: List[Dict] = []
        self.llm = OllamaClient(model='deepseek')
        self.chat_history = []
        
    def create_scene_interface(self) -> gr.Blocks:
        """Create and return the Gradio interface for scenes management"""
        with gr.Blocks() as scenes_interface:
            gr.Markdown("### Manage Scenes")
            
            with gr.Row():
                with gr.Column(scale=2):
                    scene_title = gr.Textbox(label="Scene Title")
                    scene_description = gr.TextArea(label="Scene Description", lines=3)
                    scene_location = gr.Textbox(label="Location")
                    with gr.Row():
                        scene_day = gr.Textbox(label="Day", placeholder="e.g., Day 1, Monday, etc.")
                        scene_time = gr.Textbox(label="Time", placeholder="e.g., Morning, Afternoon, Evening, Night")
                    scene_characters = gr.Textbox(label="Characters (comma separated)")
                    scene_notes = gr.TextArea(label="Additional Notes", lines=4)
                    
                    with gr.Row():
                        save_button = gr.Button("Save Scene")
                        clear_button = gr.Button("Clear Form")
                    
                    status = gr.Markdown("Status: _No scene saved yet_")
            
            with gr.Column(scale=1):
                scenes_list = gr.Dataframe(
                    headers=["Title", "Location", "Day", "Time"],
                    datatype=["str", "str", "str", "str"],
                    col_count=(4, "fixed")
                )
                
                load_button = gr.Button("Load Selected Scene")
                delete_button = gr.Button("Delete Selected Scene")
            
            # Chat Interface
            with gr.Group():
                gr.Markdown("### Character Development Chat")
                chatbot = gr.Chatbot(height=300)
                msg = gr.Textbox(label="Ask about characters or scenes", placeholder="Type your message here...")
                clear_chat = gr.Button("Clear Chat")
                
                def respond(message, chat_history):
                    if not message:
                        return "", chat_history
                        
                    # Build context from current scene and characters
                    context = ""
                    if scene_title.value:
                        context += f"Current Scene: {scene_title.value}\n"
                        context += f"Description: {scene_description.value}\n"
                        context += f"Location: {scene_location.value}\n"
                        context += f"Day: {scene_day.value}\n"
                        context += f"Time: {scene_time.value}\n"
                        context += f"Characters: {scene_characters.value}\n"
                        context += f"Notes: {scene_notes.value}\n\n"
                    
                    # Add all scenes as context
                    if self.scenes:
                        context += "All Scenes:\n"
                        for scene in self.scenes:
                            context += f"- {scene['title']}: {scene['description']}\n"
                    
                    # Build prompt with context
                    prompt = f"""You are a helpful writing assistant. Use the following context to help answer questions about characters and scenes:

{context}

User: {message}
Assistant: """
                    
                    # Get response from Ollama
                    response = self.llm.generate(prompt)
                    
                    chat_history.append((message, response))
                    return "", chat_history
                
                msg.submit(respond, [msg, chatbot], [msg, chatbot])
                clear_chat.click(lambda: [], None, chatbot)
            
            # Connect buttons to functions
            save_button.click(
                fn=self.save_scene,
                inputs=[scene_title, scene_description, scene_location, scene_day, scene_time, scene_characters, scene_notes],
                outputs=[status, scenes_list]
            )
            
            clear_button.click(
                fn=self.clear_form,
                inputs=[],
                outputs=[scene_title, scene_description, scene_location, scene_day, scene_time, scene_characters, scene_notes]
            )
            
            load_button.click(
                fn=self.load_scene,
                inputs=[scenes_list],
                outputs=[scene_title, scene_description, scene_location, scene_day, scene_time, scene_characters, scene_notes]
            )
            
            delete_button.click(
                fn=self.delete_scene,
                inputs=[scenes_list],
                outputs=[status, scenes_list]
            )
            
            # Initialize scenes list
            scenes_list.value = self.get_scenes_list()
            
        return scenes_interface
    
    def save_scene(self, title: str, description: str, location: str, day: str, time: str, characters: str, notes: str) -> tuple:
        """Save a new scene or update an existing one"""
        scene = {
            "title": title,
            "description": description,
            "location": location,
            "day": day,
            "time": time,
            "characters": [c.strip() for c in characters.split(",") if c.strip()],
            "notes": notes
        }
        
        # Check if scene with this title already exists
        existing_index = next((i for i, s in enumerate(self.scenes) if s["title"] == title), None)
        
        if existing_index is not None:
            self.scenes[existing_index] = scene
            status = f"Updated scene: {title}"
        else:
            self.scenes.append(scene)
            status = f"Saved new scene: {title}"
            
        return status, self.get_scenes_list()
    
    def get_scenes_list(self) -> List[List[str]]:
        """Return a list of scenes in the format expected by the Dataframe"""
        return [[s["title"], s["location"], s["day"], s["time"]] for s in self.scenes]
    
    def load_scene(self, selected_scenes: List[List[str]]) -> tuple:
        """Load a scene's details into the form"""
        if not selected_scenes:
            return "", "", "", "", "", "", ""
            
        selected_title = selected_scenes[0][0]  # First column is title
        scene = next((s for s in self.scenes if s["title"] == selected_title), None)
        
        if scene:
            return (
                scene["title"],
                scene["description"],
                scene["location"],
                scene["day"],
                scene["time"],
                ", ".join(scene["characters"]),
                scene["notes"]
            )
        return "", "", "", "", "", "", ""
    
    def delete_scene(self, selected_scenes: List[List[str]]) -> tuple:
        """Delete the selected scene"""
        if not selected_scenes:
            return "No scene selected", self.get_scenes_list()
            
        selected_title = selected_scenes[0][0]
        self.scenes = [s for s in self.scenes if s["title"] != selected_title]
        
        return f"Deleted scene: {selected_title}", self.get_scenes_list()
    
    def clear_form(self) -> tuple:
        """Clear all form fields"""
        return "", "", "", "", "", "", "" 
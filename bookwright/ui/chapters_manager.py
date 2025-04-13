import gradio as gr
from typing import List, Dict, Optional
from bookwright.core.llm_interface import OllamaClient
from bookwright.utils.database_manager import DatabaseManager

class ChaptersManager:
    def __init__(self, scenes_manager):
        self.chapters: List[Dict] = []
        self.scenes_manager = scenes_manager
        self.llm = OllamaClient(model='deepseek')
        self.db = DatabaseManager(None, None, None).db  # Temporary until we can pass the manager
        
    def create_chapters_interface(self) -> gr.Blocks:
        """Create and return the Gradio interface for chapters management"""
        with gr.Blocks() as chapters_interface:
            gr.Markdown("### Manage Chapters")
            
            with gr.Row():
                with gr.Column(scale=2):
                    # Chapter Details
                    chapter_title = gr.Textbox(label="Chapter Title")
                    chapter_description = gr.TextArea(label="Chapter Description", lines=3)
                    chapter_notes = gr.TextArea(label="Chapter Notes", lines=4)
                    
                    with gr.Row():
                        save_chapter_button = gr.Button("Save Chapter")
                        clear_chapter_button = gr.Button("Clear Form")
                    
                    chapter_status = gr.Markdown("Status: _No chapter saved yet_")
                    
                    # Scene Assignment
                    gr.Markdown("### Assign Scenes to Chapter")
                    available_scenes = gr.Dropdown(
                        choices=self.get_available_scenes(),
                        label="Available Scenes",
                        multiselect=True
                    )
                    assign_scenes_button = gr.Button("Assign Selected Scenes")
                    
                with gr.Column(scale=1):
                    # Chapters List
                    chapters_list = gr.Dataframe(
                        headers=["Title", "Scene Count"],
                        datatype=["str", "number"],
                        col_count=(2, "fixed")
                    )
                    
                    with gr.Row():
                        load_chapter_button = gr.Button("Load Selected Chapter")
                        delete_chapter_button = gr.Button("Delete Selected Chapter")
                    
                    # Chapter's Scenes
                    gr.Markdown("### Chapter's Scenes")
                    chapter_scenes = gr.Dataframe(
                        headers=["Scene Title", "Location", "Day", "Time"],
                        datatype=["str", "str", "str", "str"],
                        col_count=(4, "fixed")
                    )
                    
                    with gr.Row():
                        remove_scene_button = gr.Button("Remove Selected Scene")
                        reorder_scenes_button = gr.Button("Reorder Scenes")
            
            # Chat Interface for Chapter Development
            with gr.Group():
                gr.Markdown("### Chapter Development Chat")
                chatbot = gr.Chatbot(height=300)
                msg = gr.Textbox(label="Ask about chapter development", placeholder="Type your message here...")
                clear_chat = gr.Button("Clear Chat")
                
                def respond(message, chat_history):
                    if not message:
                        return "", chat_history
                        
                    # Build context from current chapter and scenes
                    context = ""
                    if chapter_title.value:
                        context += f"Current Chapter: {chapter_title.value}\n"
                        context += f"Description: {chapter_description.value}\n"
                        context += f"Notes: {chapter_notes.value}\n\n"
                        
                        # Add assigned scenes context
                        if chapter_scenes.value:
                            context += "Assigned Scenes:\n"
                            for scene in chapter_scenes.value:
                                context += f"- {scene[0]}: {scene[1]}\n"
                    
                    # Add all chapters as context
                    if self.chapters:
                        context += "\nAll Chapters:\n"
                        for chapter in self.chapters:
                            context += f"- {chapter['title']}: {chapter['description']}\n"
                    
                    # Build prompt with context
                    prompt = f"""You are a helpful writing assistant. Use the following context to help answer questions about chapter development:

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
            save_chapter_button.click(
                fn=self.save_chapter,
                inputs=[chapter_title, chapter_description, chapter_notes],
                outputs=[chapter_status, chapters_list]
            )
            
            clear_chapter_button.click(
                fn=self.clear_form,
                inputs=[],
                outputs=[chapter_title, chapter_description, chapter_notes]
            )
            
            load_chapter_button.click(
                fn=self.load_chapter,
                inputs=[chapters_list],
                outputs=[chapter_title, chapter_description, chapter_notes, chapter_scenes]
            )
            
            delete_chapter_button.click(
                fn=self.delete_chapter,
                inputs=[chapters_list],
                outputs=[chapter_status, chapters_list, chapter_scenes]
            )
            
            assign_scenes_button.click(
                fn=self.assign_scenes,
                inputs=[chapter_title, available_scenes],
                outputs=[chapter_status, chapter_scenes]
            )
            
            remove_scene_button.click(
                fn=self.remove_scene,
                inputs=[chapters_list, chapter_scenes],
                outputs=[chapter_status, chapter_scenes]
            )
            
            reorder_scenes_button.click(
                fn=self.reorder_scenes,
                inputs=[chapters_list, chapter_scenes],
                outputs=[chapter_status, chapter_scenes]
            )
            
            # Initialize lists
            chapters_list.value = self.get_chapters_list()
            available_scenes.choices = self.get_available_scenes()
            
        return chapters_interface
    
    def get_available_scenes(self) -> List[str]:
        """Get list of all available scenes"""
        return [scene["title"] for scene in self.scenes_manager.scenes]
    
    def save_chapter(self, title: str, description: str, notes: str) -> str:
        """Save a chapter to the database"""
        chapter = {
            "title": title,
            "description": description,
            "notes": notes,
            "scenes": []  # Scenes will be added separately
        }
        self.db.save_chapter(chapter)
        self.chapters = self.db.get_chapters()  # Refresh the chapters list
        return f"Saved chapter: {title}"
    
    def get_chapters_list(self) -> List[List]:
        """Return a list of chapters in the format expected by the Dataframe"""
        return [[c["title"], len(c["scenes"])] for c in self.chapters]
    
    def load_chapter(self, selected_chapters: List[List]) -> tuple:
        """Load a chapter's details into the form"""
        if not selected_chapters:
            return "", "", "", []
            
        selected_title = selected_chapters[0][0]  # First column is title
        chapter = next((c for c in self.chapters if c["title"] == selected_title), None)
        
        if chapter:
            # Get scene details for the chapter's scenes
            chapter_scenes = []
            for scene_title in chapter["scenes"]:
                scene = next((s for s in self.scenes_manager.scenes if s["title"] == scene_title), None)
                if scene:
                    chapter_scenes.append([scene["title"], scene["location"], scene["day"], scene["time"]])
            
            return (
                chapter["title"],
                chapter["description"],
                chapter["notes"],
                chapter_scenes
            )
        return "", "", "", []
    
    def delete_chapter(self, title: str) -> str:
        """Delete a chapter from the database"""
        self.db.delete_chapter(title)
        self.chapters = self.db.get_chapters()  # Refresh the chapters list
        return f"Deleted chapter: {title}"
    
    def assign_scenes(self, chapter_title: str, scene_titles: List[str]) -> tuple:
        """Assign scenes to a chapter"""
        if not chapter_title or not scene_titles:
            return "No chapter or scenes selected", []
            
        chapter = next((c for c in self.chapters if c["title"] == chapter_title), None)
        if not chapter:
            return f"Chapter not found: {chapter_title}", []
            
        # Add new scenes to chapter
        for scene_title in scene_titles:
            if scene_title not in chapter["scenes"]:
                chapter["scenes"].append(scene_title)
        
        # Get scene details for display
        chapter_scenes = []
        for scene_title in chapter["scenes"]:
            scene = next((s for s in self.scenes_manager.scenes if s["title"] == scene_title), None)
            if scene:
                chapter_scenes.append([scene["title"], scene["location"], scene["day"], scene["time"]])
        
        return f"Assigned {len(scene_titles)} scenes to {chapter_title}", chapter_scenes
    
    def remove_scene(self, selected_chapters: List[List], selected_scenes: List[List]) -> tuple:
        """Remove a scene from a chapter"""
        if not selected_chapters or not selected_scenes:
            return "No chapter or scene selected", []
            
        chapter_title = selected_chapters[0][0]
        scene_title = selected_scenes[0][0]
        
        chapter = next((c for c in self.chapters if c["title"] == chapter_title), None)
        if not chapter:
            return f"Chapter not found: {chapter_title}", []
            
        # Remove scene from chapter
        if scene_title in chapter["scenes"]:
            chapter["scenes"].remove(scene_title)
            
        # Get updated scene list
        chapter_scenes = []
        for scene_title in chapter["scenes"]:
            scene = next((s for s in self.scenes_manager.scenes if s["title"] == scene_title), None)
            if scene:
                chapter_scenes.append([scene["title"], scene["location"], scene["day"], scene["time"]])
        
        return f"Removed scene from {chapter_title}", chapter_scenes
    
    def reorder_scenes(self, selected_chapters: List[List], scenes_order: List[List]) -> tuple:
        """Reorder scenes in a chapter"""
        if not selected_chapters or not scenes_order:
            return "No chapter or scenes selected", []
            
        chapter_title = selected_chapters[0][0]
        chapter = next((c for c in self.chapters if c["title"] == chapter_title), None)
        if not chapter:
            return f"Chapter not found: {chapter_title}", []
            
        # Update chapter's scene order
        chapter["scenes"] = [scene[0] for scene in scenes_order]
        
        return f"Reordered scenes in {chapter_title}", scenes_order
    
    def clear_form(self) -> tuple:
        """Clear all form fields"""
        return "", "", "", [] 
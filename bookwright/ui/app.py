# bookwright/ui/app.py

# from bookwright.utils.database_manager import StoryDatabase
# from bookwright.core.llm_interface import OllamaClient
# from bookwright.utils.prompt_builder import build_chapter_prompt

# def main():
#     # Initialize components
#     db = StoryDatabase('my_story.db')
#     llm = OllamaClient(model='deepseek')

#     # Step 1: Add some characters
#     db.add_character(
#         name='Lira',
#         description='A young warrior from the mountain tribes',
#         appearance='Tall, with braided black hair and striking green eyes',
#         personality='Brave, impulsive, fiercely loyal',
#         likes='Sword fighting, wild nature, old legends'
#     )
#     db.add_character(
#         name='Kael',
#         description='A wandering scholar with a mysterious past',
#         appearance='Lean, spectacles, always carries an old journal',
#         personality='Calm, clever, secretive',
#         likes='Ancient languages, puzzles, quiet nights'
#     )

#     # Step 2: Define chapter outline
#     chapter_title = "The Meeting at Dawn"
#     outline = """
# Lira encounters Kael by the river as dawn breaks.
# An argument breaks out over a hidden map.
# Suddenly, a shadowy threat looms from the forest, forcing uneasy cooperation.
# """

#     # Step 3: Build prompt
#     characters = db.get_characters()
#     prompt = build_chapter_prompt(chapter_title, outline, characters)

#     # Step 4: Generate text via Ollama
#     generated_text = llm.generate(prompt)

#     # Step 5: Save generated draft to database
#     db.add_chapter(chapter_title, outline, generated_text)

#     # Step 6: Output
#     print(f"\n--- {chapter_title} ---\n")
#     print(generated_text)

#     # Close db connection
#     db.close()

# if __name__ == '__main__':

import gradio as gr
import os, signal
from bookwright.ui.scenes_manager import ScenesManager
from bookwright.ui.characters_manager import CharactersManager
from bookwright.ui.chapters_manager import ChaptersManager
from bookwright.utils.database_manager import DatabaseManager
from datetime import datetime

def welcome_area():
    return """
# 📚 Welcome to BookWright AI
Your interactive AI-powered writing partner.

Use the menu to:

- **Define Characters**: Build rich bios & personalities
- **Outline Chapters**: Organize your story flow
- **Generate Drafts**: Collaborate with local DeepSeek R1 model
- **Manage Data**: View or edit your characters, scenes, and chapters
- **Settings**: Configure models and preferences

Enjoy creative writing powered by AI and structured workflow!
"""

def characters_interface():
    characters_manager = CharactersManager()
    scenes_manager = ScenesManager()
    characters_manager.set_scenes(scenes_manager.scenes)
    return characters_manager.create_characters_interface()

def chapters_interface():
    return gr.Markdown("### Manage Chapters\n_Create outlines, add scene details, and more._")

def story_generator_interface():
    return gr.Markdown("### Story Generator\n_Generate and refine narrative drafts with AI._")

def database_viewer_interface():
    return gr.Markdown("### Database Viewer\n_Browse stored data – characters, scenes, chapters._")

def settings_interface():
    return gr.Markdown("### Settings\n_Configure model options, preferences, and more._")

def scenes_interface():
    scenes_manager = ScenesManager()
    return scenes_manager.create_scene_interface()

# --- Example functions to connect your data backend ---
def save_book_meta(title, author, genre, setting, description, plot_summary, plot_points_text):
    # Here, you'd update SQLite or in-memory storage
    # For demo, just return input as confirmation
    # parse plot points text into a list again if needed
    plot_points = [p.strip() for p in plot_points_text.split('\n') if p.strip()]
    # Save to DB here...
    return f"Saved book '{title}' by {author} with {len(plot_points)} plot points."

def load_book_meta():
    # Load from DB, for example purpose returning dummy data
    title = "The Lost Kingdom"
    author = "Jane Doe"
    genre = "Fantasy"
    setting = "Ancient mountain realm threatened by dark forces"
    description = "An epic journey and the heroes who rise to the challenge."
    plot_summary = "After the king's disappearance, rebels race to secure the realm's fate."
    plot_points = [
        "Hero discovers ancient prophecy",
        "Mysterious stranger joins quest",
        "Betrayal inside rebellion",
        "Epic final battle at mountain fortress"
    ]
    plot_points_text = "\n".join(plot_points)
    return title, author, genre, setting, description, plot_summary, plot_points_text

# &#x2014; Define UI &#x2014;
def book_info_tab():
    """Create the Book Info tab interface"""
    with gr.TabItem("Book Info"):
        gr.Markdown("### Book Information")
        book_title = gr.Textbox(label="Book Title")
        book_author = gr.Textbox(label="Author")
        book_genre = gr.Dropdown(
            choices=["Fiction", "Non-Fiction", "Mystery", "Romance", "Science Fiction", "Fantasy", "Other"],
            label="Genre"
        )
        book_summary = gr.TextArea(label="Book Summary", lines=5)
        book_notes = gr.TextArea(label="Additional Notes", lines=4)
        
        with gr.Row():
            save_book_info = gr.Button("Save Book Info")
            clear_book_info = gr.Button("Clear Form")
            load_book_info = gr.Button("Load Saved Info")
        
        book_status = gr.Markdown("Status: _No book info saved yet_")

        # When clicking save
        def save_info(title, author, genre, summary, notes):
            database_manager.db.save_book_info(title, author, genre, summary, notes)
            return f"Saved book info: {title} by {author}"
        
        save_book_info.click(
            fn=save_info,
            inputs=[book_title, book_author, book_genre, book_summary, book_notes],
            outputs=book_status
        )
        
        # When clicking load
        def load_info():
            book_info = database_manager.db.get_book_info()
            if book_info:
                return (
                    book_info["title"],
                    book_info["author"],
                    book_info["genre"],
                    book_info["summary"],
                    book_info["notes"]
                )
            return "", "", "", "", ""
        
        load_book_info.click(
            fn=load_info,
            inputs=[],
            outputs=[book_title, book_author, book_genre, book_summary, book_notes]
        )
        
        # Clear/reset
        def clear_all():
            return "", "", "", "", ""
        
        clear_book_info.click(
            fn=clear_all,
            inputs=[],
            outputs=[book_title, book_author, book_genre, book_summary, book_notes]
        )

def quit_app():
    """Function to quit the application"""
    os.kill(os.getpid(), signal.SIGINT)
    return "🚪 Exiting BookWright AI..."

def create_interface():
    global database_manager
    scenes_manager = ScenesManager()
    characters_manager = CharactersManager(scenes_manager)
    chapters_manager = ChaptersManager(scenes_manager)
    database_manager = DatabaseManager(scenes_manager, characters_manager, chapters_manager)
    
    # Load initial data from database
    scenes_manager.scenes = database_manager.db.get_scenes()
    characters_manager.characters = database_manager.db.get_characters()
    chapters_manager.chapters = database_manager.db.get_chapters()
    
    with gr.Blocks(title="BookWright AI") as interface:
        gr.Markdown("# 📚 BookWright AI - Writing Assistant")
        
        with gr.Tabs():
            with gr.TabItem("Home"):
                gr.Markdown("Welcome to BookWright AI!")
            
            with gr.TabItem("Characters"):
                characters_manager.create_characters_interface()
            
            with gr.TabItem("Scenes"):
                scenes_manager.create_scene_interface()
            
            with gr.TabItem("Chapters"):
                chapters_manager.create_chapters_interface()
            
            with gr.TabItem("Story Generator"):
                gr.Markdown("Generate stories here...")
            
            with gr.TabItem("Database Viewer"):
                gr.Markdown("### Database Operations")
                
                # Export Section
                gr.Markdown("#### Export Data")
                export_status = gr.Markdown("Click the button below to export all data as JSON")
                export_button = gr.Button("Export Data")
                json_output = gr.TextArea(label="JSON Data", lines=10, interactive=False)
                
                def export_data():
                    json_data = database_manager.export_to_json()
                    return "Data exported successfully!", json_data
                
                export_button.click(
                    fn=export_data,
                    inputs=[],
                    outputs=[export_status, json_output]
                )
                
                # Download Section
                gr.Markdown("#### Download Data")
                download_button = gr.Button("Download JSON File")
                download_status = gr.Markdown("")
                download_file = gr.File(label="Download File")
                
                def download_data():
                    json_data = database_manager.export_to_json()
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"bookwright_export_{timestamp}.json"
                    
                    # Create a temporary file
                    with open(filename, "w") as f:
                        f.write(json_data)
                    
                    return f"File saved as {filename}", filename
                
                download_button.click(
                    fn=download_data,
                    inputs=[],
                    outputs=[download_status, download_file]
                )
            
            with gr.TabItem("Settings"):
                gr.Markdown("Configure your settings here.")
                quit_button = gr.Button("❌ Quit Application")
                status = gr.Markdown("")
                quit_button.click(fn=quit_app, inputs=[], outputs=status)
            
            # Add the Book Info tab
            book_info_tab()
    
    return interface

def main():
    interface = create_interface()
    interface.launch()

if __name__ == "__main__":
    main()


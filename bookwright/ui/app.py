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
    with gr.TabItem("Book Info"):
        gr.Markdown("### Book Details, Plot, and Story Settings Editor")
        title = gr.Textbox(label="Book Title")
        author = gr.Textbox(label="Author")
        genre = gr.Dropdown(choices=["Fantasy", "Sci-Fi", "Romance", "Mystery", "Horror", "Non-fiction", "Other"], label="Genre")
        setting = gr.Textbox(label="Main Setting/World")
        description = gr.Textbox(label="Book Summary / Description")
        plot_summary = gr.Textbox(label="High-Level Plot Summary")
        plot_points = gr.TextArea(label="Main Plot Points (one per line)", lines=8, placeholder="Eg:\nHero discovers prophecy\nRebels betrayed\n...")

        with gr.Row():
            save_button = gr.Button("Save Details")
            load_button = gr.Button("Load Last Saved")
            clear_button = gr.Button("Clear Form")

        status = gr.Markdown("Status: _Nothing saved yet_")

        # When clicking save
        save_button.click(
            fn=save_book_meta,
            inputs=[title, author, genre, setting, description, plot_summary, plot_points],
            outputs=status
        )
        # When clicking load/view
        load_button.click(
            fn=load_book_meta,
            inputs=[],
            outputs=[title, author, genre, setting, description, plot_summary, plot_points]
        )
        # Clear/reset
        def clear_all():
            return "", "", "", "", "", "", ""
        clear_button.click(fn=clear_all, inputs=[], outputs=[title, author, genre, setting, description, plot_summary, plot_points])


def quit_app():
    os.kill(os.getpid(), signal.SIGINT)
    return "🚪 Exiting BookWright AI..."
# --- integrate this tab into your main Blocks app ---
with gr.Blocks(title="BookWright AI") as demo:
    gr.Markdown("# 📚 BookWright AI - Writing Assistant")
    with gr.Tabs():
        with gr.TabItem("Home"):
            gr.Markdown("Welcome to BookWright AI!")
        with gr.TabItem("Characters"):
            characters_interface()
        with gr.TabItem("Scenes"):
            scenes_interface()
        with gr.TabItem("Chapters"):
            gr.Markdown("Manage Chapters here...")
        with gr.TabItem("Story Generator"):
            gr.Markdown("Generate stories here...")
        with gr.TabItem("Database Viewer"):
            gr.Markdown("View database here...")

        with gr.TabItem("Settings"):
            gr.Markdown("Configure your settings here.")
            quit_button = gr.Button("❌ Quit Application")
            status = gr.Markdown("")
            quit_button.click(fn=quit_app, inputs=[], outputs=status)
        # Add your new tab:
        book_info_tab()  # call the function defined above to insert tab

def main():
    demo.launch()

if __name__ == "__main__":
    main()


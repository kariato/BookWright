# BookWright

BookWright is a personal project developed to explore and learn the capabilities of Cursor.ai while creating a practical writing assistant application. The project combines Python, Gradio, and local AI models to help writers organize and develop their stories.

## Project Overview

BookWright is a writing assistant that helps authors manage various aspects of their writing process:

- **Character Management**: Create and organize character profiles with detailed information
- **Scene Organization**: Track scenes with location, time, and character involvement
- **Chapter Planning**: Structure chapters and assign scenes to them
- **Book Information**: Maintain book metadata and plot details
- **AI Assistance**: Get writing suggestions and development help using local AI models

## Features

### Character Management
- Create detailed character profiles
- Track character appearances in scenes
- Manage character relationships and development
- View character-specific scene information

### Scene Organization
- Create and organize scenes with location and time details
- Track character involvement in scenes
- Add scene-specific notes and descriptions
- Link scenes to chapters

### Chapter Planning
- Create chapter outlines
- Assign scenes to chapters
- Reorder scenes within chapters
- Track chapter progress and structure

### Book Information
- Store book metadata (title, author, genre)
- Maintain plot summaries and notes
- Track overall story structure

### AI Integration
- Local AI model integration via Ollama
- Context-aware writing assistance
- Character and scene development suggestions

## Technical Stack

- **Python**: Core application logic
- **Gradio**: User interface framework
- **Ollama**: Local AI model integration
- **SQLite**: Data persistence (planned)

## Project Structure

```
bookwright/
├── core/
│   └── llm_interface.py    # AI model integration
├── ui/
│   ├── app.py              # Main application
│   ├── characters_manager.py
│   ├── scenes_manager.py
│   └── chapters_manager.py
├── utils/
│   └── database_manager.py # Database operations
├── requirements.txt        # Project dependencies
└── launch.sh              # Application launcher
```

## Getting Started

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   ./launch.sh
   ```

## Development Notes

This project was created as a learning exercise to:
- Explore Cursor.ai's capabilities
- Practice Python application development
- Learn Gradio interface development
- Experiment with local AI model integration
- Understand software architecture patterns

## Future Enhancements

- Database persistence for all data
- Enhanced AI writing assistance
- Export functionality for various formats
- Collaborative writing features
- Version control integration

## License

This is a personal project and is not intended for commercial use.

## Author

[Your Name] - Learning and exploring with Cursor.ai

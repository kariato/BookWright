# bookwright/utils/prompt_builder.py

def build_chapter_prompt(title, outline, character_info):
    """
    Combine chapter outline and characters to generate a rich prompt.
    """
    prompt = f"Write the first draft of a book chapter titled '{title}'.\n\n"
    prompt += f"Chapter Outline:\n{outline}\n\n"

    if character_info:
        prompt += "Main Characters involved:\n"
        for c in character_info:
            name, desc, appearance, personality, likes = c
            prompt += f"\n{name}:\n"
            prompt += f"- Description: {desc}\n"
            prompt += f"- Appearance: {appearance}\n"
            prompt += f"- Personality: {personality}\n"
            prompt += f"- Likes: {likes}\n"

    prompt += "\nPlease write in an engaging, vivid style with natural dialogue and action beats."
    return prompt

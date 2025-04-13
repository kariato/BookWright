Below is a **complete design outline** incorporating the latest details about the centralized LLM calling function, along with a sample JSON structure that demonstrates how you might include **chain-of-thought prompts** in your system. The chain-of-thought field is optional, but if you wish to store or manage intermediate reasoning or step-by-step logic, this is one way to structure it.

---

## **AI Book Writing Assistant — Comprehensive Outline**

### 1. Introduction
- **Purpose of the Application**  
  Provide an all-in-one platform for drafting, brainstorming, editing, and publishing book-length works with AI assistance.

- **Main Features**  
  1. Creative text generation (chapters, scenes, dialogue).  
  2. Dynamic prompting to guide the writing process.  
  3. Databases for chapters, scenes, characters, prompts, etc.

---

### 2. User Interface (UI) and Experience (UX)
- **Intuitive Text Editor**  
  - Clean writing environment with minimal distractions.  
  - Formatting options for headings, paragraphs, and other text elements.

- **Real-Time Suggestions**  
  - On-the-fly recommendations for sentence completions, rephrasing, and expansions.

- **Chat Boxes for Discussion**  
  - Each screen includes an integrated chat box to discuss the current content with either the AI or human collaborators.  
  - Ideal for brainstorming, clarifying prompts, or receiving instant feedback.

- **Rollback / Revision Feature**  
  - Allows users to revert to earlier states of the document or database records.  
  - Tracks changes so you can quickly undo unwanted modifications.

---

### 3. Backend and Model Infrastructure
- **Large Language Model Integration**  
  - Connect to an LLM (e.g., Ollama, GPT-based model, etc.) that can generate and refine text.  
  - Support dynamic prompts and user-driven commands.

- **Fine-Tuning Approach**  
  - Potentially fine-tune the model on specific genres or user-provided data for more tailored outputs.

---

### 4. Key Features

#### 4.1 Dynamic Prompting
- Both user-driven prompts and AI-initiated suggestions to help with plot, character development, and editing tasks.

#### 4.2 Story Development Modules
- **Chapter Database**  
  - Each chapter is a record with fields for chapter number, title, and summary.  
  - Maintains a list of related scenes.

- **Scene Database**  
  - Each scene has its own record (location, time, summary, etc.).  
  - Sub-parts of each scene are linked records, capturing important beats or events.  
  - Relationships between sub-scenes and character interactions or traits.

- **Character Database**  
  - Each character is a record with name, role, and additional notes.  
  - Separate tables for traits, history, or interactions.  
  - Links to scenes, tracking key dialogue or emotional states.

- **Prompt Database**  
  - Stores both user-driven and AI-generated prompts.  
  - Includes fields like prompt text, context, timestamp, user ID, usage frequency.

#### 4.3 AI-Driven Editing Suggestions
- Grammar and style checks, plus voice/tone consistency.  
- Built-in rewriting or reformatting tools.

#### 4.4 Stage-by-Stage Tips
- Offers context-aware best practices (brainstorming, drafting, revising, etc.).  
- Prompts the writer to focus on key tasks relevant to each stage.

#### 4.5 Additional Features and Enhancements
- **Version Control / Revision History**  
  - Compares revisions, tracks changes, and can restore earlier versions.

- **Analytics & Writing Metrics**  
  - Tracks word count, reading level, pacing analysis, etc.

- **Theme & Tone Consistency**  
  - Lets users define a specific tone or style to maintain across the manuscript.

- **Style Profiles & Personalization**  
  - Learns each author’s writing style over time and adapts suggestions.

- **World-Building Tools** (Fantasy/Sci-Fi)  
  - Databases or sub-modules for lore, faction info, timelines, etc.

- **Collaboration Features**  
  - Multiple authors/editors can add comments, track changes, or chat in real time.

- **Publishing Pipeline**  
  - Export options for EPUB, MOBI, or direct integration with publishing platforms.

- **Project Management Dashboard**  
  - High-level overview of writing progress, to-do lists, upcoming tasks.

- **Research & Inspiration Hub**  
  - Saves web links, references, or images relevant to the manuscript.

- **Community or Marketplace** (Optional)  
  - Sharing or discovering templates, character sketches, or prompts.

---

### 5. Roadmap
1. **Phase 1 (MVP)**  
   - Basic text generation  
   - Core database tables and AI-driven suggestions

2. **Phase 2**  
   - Advanced story tools (detailed chapter, scene, and character databases)  
   - Collaboration features, stage-by-stage tips

3. **Phase 3**  
   - Personalization & style improvements  
   - Publishing pipeline, analytics, versioning expansions

---

### 6. Proposed Centralized LLM Calling Architecture

1. **Central LLM Function**  
   - A single function or microservice that handles calls to the LLM, preventing scattered LLM logic across the codebase.

2. **Prompt JSON Files**  
   - Each file defines:
     - **`llm_name`**: The identifier for which LLM to call (e.g., “ollama”).
     - **`system_card`**: System-level instructions or constraints that shape the LLM’s behavior.
     - **`prompt_card`**: The main prompt template or instructions for how to frame user data.
     - **`chain_of_thought_prompts`**: If you wish to store or guide the LLM’s intermediate reasoning steps. (Often hidden in production, but can be used for debugging or specialized flows.)
     - **`handler_code`**: Metadata or mini-scripts describing how to process a separate JSON that contains application data.

3. **Application Data JSON**  
   - Holds the current state of the app (chapters, scenes, characters, etc.).  
   - Passed to the central LLM function when generating or refining text so the LLM can reference relevant story data.

4. **Structured JSON Output**  
   - The LLM is asked to return a well-structured JSON payload, simplifying ingestion back into the database or UI.  
   - Example: AI might return updated scene summaries, character arcs, or direct suggestions.

5. **Ollama LLM + LangGraph Integration**  
   - **LangGraph** helps orchestrate structured queries, manage state, and handle data flow between your app and Ollama.  
   - Ensures consistent input-output flows with validation.

---

## **Sample JSON Structure with Chain-of-Thought Prompts**

Below is a **hypothetical** JSON file illustrating how you might store the system card, prompt card, and chain-of-thought instructions for the **centralized LLM function**. This file could live in your codebase under something like `prompts/ollama_main.json`.

```json
{
  "llm_name": "ollama",
  "system_card": "You are a helpful writing assistant specialized in structuring and editing stories. Always follow the user’s style and be consistent with established story details.",
  "prompt_card": "Please reference the provided application data (chapters, scenes, characters). Summarize or rewrite content based on user requests. Return output in valid JSON format.",
  "chain_of_thought_prompts": [
    "Step 1: Read the user input carefully and extract any relevant context.",
    "Step 2: Verify the user’s writing style or constraints from system_card instructions.",
    "Step 3: Summarize or rewrite the content using the story data from the application JSON.",
    "Step 4: Format the final response as properly structured JSON, referencing characters, scenes, or chapters as needed."
  ],
  "handler_code": "function handleData(data) { /* Code to parse 'data' and insert into the final prompt. */ }"
}
```

### Explanation

- **`llm_name`**: Tells the app which model to call—useful if you support multiple models.  
- **`system_card`**: The “role” or “persona” that sets overall behavior for the LLM.  
- **`prompt_card`**: High-level instructions or templates for how the LLM should process user queries.  
- **`chain_of_thought_prompts`**: If you wish to store or guide the LLM’s intermediate reasoning or step-by-step approach, you can specify those instructions here. In a production environment, you might keep these hidden or remove them for privacy/security reasons.  
- **`handler_code`**: Pseudocode or instructions that show how your application will handle the `Application Data JSON` and incorporate it into the final LLM prompt.

---

### Putting It All Together

1. **Load the JSON** (e.g., `prompts/ollama_main.json`) when the user initiates an AI action.  
2. **Combine** the prompt template, chain-of-thought steps (if needed), and the **Application Data JSON** to build a final text prompt.  
3. **Send** the final prompt to Ollama via LangGraph, ensuring it’s set to return structured JSON.  
4. **Parse** the returned JSON. Update your app’s data or display the results in the UI.  
5. **Store** the prompt and response in your `Prompt Database` for reference or model improvement.

---

## **Conclusion and Next Steps**

- This design outlines how you might **centralize all LLM calls** in one place.  
- Using **prompt JSON files** simplifies version control and ensures consistent prompt formatting across the application.  
- **Chain-of-thought prompts** can be included in these JSONs for debugging or specialized reasoning workflows.  
- The **LangGraph** + **Ollama** stack provides a structured approach to model orchestration.

With this plan, you can move from design to **prototype** by creating your Python or Node.js functions, setting up the database schema, and connecting everything in a small proof of concept. Over time, you’ll refine data flows, user interactions, and the AI’s output for a polished, full-featured writing platform.

---

**I hope this detailed design and JSON example help clarify how you can store prompts, chain-of-thought, and application data for a centralized LLM approach.** If you need more specifics or a deeper dive into any particular step (such as how to implement handler_code or how to parse structured JSON responses), let me know!
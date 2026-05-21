
```markdown
# Autonomous Agent Sidekick 🤖

An agentic, multi-step research assistant built with a **Worker-Evaluator pattern**. This project utilizes **LangGraph** for cyclical task execution, **Playwright** for autonomous web navigation, and **SQLite** for state persistence.

## 🏗️ Architecture: The Worker-Evaluator Loop

The system operates on a feedback loop where an **Agent Worker** attempts a task, and an **Evaluator** assesses the output against predefined success criteria. If the output fails, the Evaluator provides feedback, and the Worker retries until the criteria are met.



## 🚀 Key Features
- **Self-Correcting Loops:** Evaluator-led retries ensure high-quality, verified results.
- **Persistent Memory:** Uses `AsyncSqliteSaver` to maintain conversation history across sessions.
- **Autonomous Browsing:** Leverages Playwright to research live web data.
- **Local Persistence:** Conversation states are stored locally in a SQLite database, ensuring privacy and continuity.

## 🛠️ Setup Instructions

Follow these steps to run the agent locally on your machine.

### 1. Prerequisites
- **Python 3.10+** installed on your system.
- **Git** installed.

### 2. Clone the Repository
```bash
git clone [https://github.com/IbrahemAmar/Autonomous-Agent-Sidekick.git](https://github.com/IbrahemAmar/Autonomous-Agent-Sidekick.git)
cd Autonomous-Agent-Sidekick

```

### 3. Environment Configuration

Create a `.env` file in the root directory and add your API keys:

```text
OPENAI_API_KEY=your_openai_api_key_here

```

### 4. Install Dependencies

Create a virtual environment and install the required packages:

```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Install requirements
pip install -r requirements.txt
playwright install chromium

```

### 5. Running the Agent

Once dependencies are installed, launch the interface:

```bash
python app.py

```

Open the provided URL (`http://127.0.0.1:7860`) in your browser to interact with your Sidekick.

## 📂 Project Structure

* `sidekick.py`: Core Agent logic and Graph definition.
* `sidekick_tools.py`: Tool definitions for web browsing and file manipulation.
* `app.py`: Gradio web interface and orchestration.
* `data/`: SQLite database storage for memory persistence.

## 🚧 Planned Features

* [ ] Integration with additional research tools (ArXiv, Google Scholar).
* [ ] Support for alternative LLM providers (Anthropic, OpenRouter).
* [ ] Enhanced UI dashboard for monitoring evaluator feedback cycles.

```

---

### Final Check Before Pushing:
1.  Ensure your `requirements.txt` is updated: Run `pip freeze > requirements.txt` in your terminal first.
2.  Ensure your `.gitignore` is present and contains `.env`, `data/`, and `.venv/`.
3.  **Now you are ready to copy, save, and perform the final `git add .`, `git commit`, and `git push`.**

Your project is now professionally documented and ready for any recruiter to review! Is there anything else you want to polish before we call this project "Done"?

```

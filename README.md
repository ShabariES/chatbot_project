# chatbot_project
# NewTurn AI — Real-Time Streaming Chatbot Platform

**NewTurn AI** is a modern, high-performance web-based AI assistant built with **Django** and powered by the **Groq API**. It features real-time Server-Sent Events (SSE) token streaming, user authentication, multi-conversation thread management, markdown rendering, and syntax-highlighted code execution previews in a sleek, responsive interface.

---

## ✨ Features

- **⚡ Real-Time SSE Token Streaming**: Ultra-fast response streaming powered by Groq's high-speed LLM inference engine.
- **💬 Conversation Management**: Create, switch between, and delete multiple chat threads stored persistently per user.
- **🔒 Full User Authentication**: Built-in signup, login, and secure session management.
- **🎨 Modern Dark UI**: Sleek, distraction-free aesthetic with smooth micro-animations.
- **📝 Markdown & Code Highlighting**: Rich text formatting with live code block syntax highlighting (via `marked.js` and `highlight.js`) and one-click copy buttons.
- **🗃️ Persistent Chat History**: All user and assistant messages are stored in Django models for seamless session continuity.

---

## 🛠️ Tech Stack

- **Backend**: Python 3.12+, Django 5.x
- **AI Integration**: Groq SDK (`groq/compound` inference engine)
- **Frontend**: HTML5, CSS3 (Vanilla CSS with Flexbox/Grid), JavaScript (ES6+ with EventSource SSE)
- **Database**: SQLite (default, easily adaptable to PostgreSQL/MySQL)

---

## 🚀 Quick Start

### 1. Prerequisites
- Python 3.10+
- A valid [Groq API Key](https://console.groq.com/)

### 2. Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/NewTurn-AI.git
   cd NewTurn-AI
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install django groq
   ```

4. **Configure your API Key:**
   In `chatbot_project/settings.py` (or via environment variables):
   ```python
   GROQ_API_KEY = "your-groq-api-key-here"
   GROQ_MODEL = "groq/compound"
   ```

5. **Run Database Migrations:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Start the Development Server:**
   ```bash
   python manage.py runserver
   ```

7. **Access the App:**
   Open your browser and navigate to `http://127.0.0.1:8000/`.

---

## 📸 Screenshots & Demo

*(Add screenshots of your UI here!)*

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.


# 🎓 AI Study Assistant

An AI-powered study assistant built using Python, FastAPI, Google Gemini API, HTML, CSS and JavaScript.

It helps students understand academic concepts through simple explanations, examples and multi-turn conversations.

## ✨ Features

- AI-powered answers using Google Gemini.
- Multi-turn conversation memory.
- Unique conversation IDs.
- Context management using recent conversation history.
- Custom system prompt for student-friendly responses.
- Simple and responsive chat interface.
- Caramel and cream user interface.
- API error handling.
- Secure API key management using environment variables.

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Backend programming |
| FastAPI | REST API development |
| Google Gemini API | AI responses |
| HTML | Webpage structure |
| CSS | User interface styling |
| JavaScript | Frontend and API communication |
| python-dotenv | Environment variable management |

## 📁 Project Structure

```text
AI-Study-Assistant/
│
├── backend/
│   └── main.py
│
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── script.js
│
├── .gitignore
├── README.md
├── requirements.txt
└── .env (create locally)
```

## ⚙️ Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/Padmapriya2121/AI-Study-Assistant.git
cd AI-Study-Assistant
```

### 2. Create a virtual environment

```bash
py -m venv venv
```

### 3. Activate the virtual environment

Windows:

```bash
venv\Scripts\activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure the Gemini API key

Create a `.env` file in the project root directory.

Add:

```env
GEMINI_API_KEY=your_gemini_api_key
```

Replace the placeholder with your own Gemini API key.

### 6. Run the application

```bash
py -m uvicorn backend.main:app --reload
```

### 7. Open the application

Visit:

http://127.0.0.1:8000/

## 🧠 Conversation Memory

The application maintains separate conversation histories using unique conversation IDs.

It sends the latest 10 messages as context to Gemini so that the assistant can understand previous messages.

Conversation history is stored in memory while the server is running.

## 🔐 Security

- API keys are loaded from environment variables.
- The `.env` file is excluded from Git using `.gitignore`.
- API keys should never be
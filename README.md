# 🌐 LinguaBot — Multi-Language Translator Chatbot
🚀 Live Demo: https://linguabot-xrkdqzm2yek4nkeig3dwrd.streamlit.app/

A smart AI-powered chatbot that detects your language automatically and responds in the same language. Type or speak in Hindi, Telugu, Marathi, Spanish, French and more — LinguaBot understands and replies in your language!

---

## ✨ Features

- 🔍 **Auto Language Detection** — Detects language automatically from your text
- 🎤 **Voice Input** — Speak in your language, bot transcribes in native script
- 🔊 **Voice Output** — Bot speaks the reply back in your language
- 🌍 **12 Languages Supported** — Hindi, Telugu, Marathi, Tamil, Spanish, French, German, Japanese, Korean, Arabic, Russian, English
- 💬 **Conversation Memory** — Remembers last 6 messages for context
- 🎨 **Beautiful Dark UI** — Custom designed interface with stats dashboard

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| UI | Streamlit |
| Language Detection | langdetect |
| Translation | deep-translator (Google Translate) |
| AI Model | Groq API — LLaMA 3.3 70B |
| Voice Input | SpeechRecognition + PyAudio |
| Voice Output | gTTS + pygame |
| Environment | Python 3.12 |

---

## 📁 Project Structure
```
linguabot/
│
├── app.py              # Main application code
├── style.css           # Custom UI styling
├── requirements.txt    # Python dependencies
├── .env                # API keys (not uploaded)
└── .gitignore          # Git ignore rules
```

---

## 🚀 Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/yourname/linguabot.git
cd linguabot
```

### 2. Create virtual environment
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Get your free Groq API key
- Go to [console.groq.com](https://console.groq.com)
- Sign up and create an API key

### 5. Create `.env` file
```
GROQ_API_KEY=your_api_key_here
```

### 6. Run the app
```bash
streamlit run app.py
```

Open `http://localhost:8501` in your browser 🎉

---

## 📸 Screenshots

<p align="center">
  <img src="https://github.com/user-attachments/assets/5900a402-4530-4c3d-a50d-e62f01e3930c" width="400"/>
  <img src="https://github.com/user-attachments/assets/4c74ab28-c97b-4cd2-bd7b-94d11cde0aa2" width="400"/>
</p>

## 🔮 Future Plans

- 📤 Export chat history as PDF
- 🌐 Deploy online via Streamlit Cloud
- 📱 Mobile friendly version

---

Made with ❤️ by **Nirvigna**

---

## ⭐ If you liked this project, give it a star on GitHub!


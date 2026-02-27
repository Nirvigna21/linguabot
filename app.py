import os
import streamlit as st
from langdetect import detect
from deep_translator import GoogleTranslator
from groq import Groq
from dotenv import load_dotenv
import speech_recognition as sr
from gtts import gTTS
import pygame
import tempfile
import time

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

lang_map = {
    "en": ("🇬🇧", "English", "en"),
    "hi": ("🇮🇳", "Hindi", "hi"),
    "te": ("🇮🇳", "Telugu", "te"),
    "mr": ("🇮🇳", "Marathi", "mr"),
    "es": ("🇪🇸", "Spanish", "es"),
    "fr": ("🇫🇷", "French", "fr"),
    "de": ("🇩🇪", "German", "de"),
    "ja": ("🇯🇵", "Japanese", "ja"),
    "ar": ("🇸🇦", "Arabic", "ar"),
    "ru": ("🇷🇺", "Russian", "ru"),
    "ko": ("🇰🇷", "Korean", "ko"),
    "ta": ("🇮🇳", "Tamil", "ta"),
}

voice_lang_options = {
    "Auto (English)": "en-US",
    "Hindi": "hi-IN",
    "Telugu": "te-IN",
    "Marathi": "mr-IN",
    "Tamil": "ta-IN",
    "Spanish": "es-ES",
    "French": "fr-FR",
    "German": "de-DE",
    "Japanese": "ja-JP",
    "Korean": "ko-KR",
    "Arabic": "ar-SA",
    "Russian": "ru-RU",
}

def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css("style.css")

st.set_page_config(page_title="LinguaBot", page_icon="🌐", layout="centered")

st.markdown("""
<div class="title-banner">
    <h1>🌐 LinguaBot</h1>
    <p>Speak or type in any language — I detect, understand & reply in yours</p>
    <div class="status-row">
        <span class="status-chip">● Live</span>
        <span class="status-chip blue">🤖 LLaMA 3.3 70B</span>
        <span class="status-chip purple">🗺️ 12 Languages</span>
    </div>
</div>
""", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []
if "detected_langs" not in st.session_state:
    st.session_state.detected_langs = []

total_msgs = len(st.session_state.messages)
unique_langs = len(set(st.session_state.detected_langs))

st.markdown(f"""
<div class="stats-bar">
    <div class="stat-card">
        <div class="stat-val">{total_msgs}</div>
        <div class="stat-label">Messages</div>
    </div>
    <div class="stat-card">
        <div class="stat-val">{unique_langs}</div>
        <div class="stat-label">Languages</div>
    </div>
    <div class="stat-card">
        <div class="stat-val">🟢</div>
        <div class="stat-label">Status</div>
    </div>
</div>
""", unsafe_allow_html=True)

def record_voice(lang_code="en-US"):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=1)
        try:
            audio = r.listen(source, timeout=8, phrase_time_limit=10)
            text = r.recognize_google(audio, language=lang_code)
            if text:
                base_lang = lang_code.split("-")[0]
                try:
                    if base_lang != "en":
                        proper_text = GoogleTranslator(source="en", target=base_lang).translate(text)
                    else:
                        proper_text = text
                except:
                    proper_text = text
                return proper_text, base_lang
            return None, None
        except:
            return None, None

def speak_text(text, lang_code):
    try:
        tts = gTTS(text=text, lang=lang_code, slow=False)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as f:
            temp_path = f.name
        tts.save(temp_path)
        pygame.mixer.init()
        pygame.mixer.music.load(temp_path)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            time.sleep(0.1)
        pygame.mixer.music.unload()
        os.remove(temp_path)
    except Exception as e:
        st.warning(f"Voice output error: {e}")

def process_input(user_input, forced_lang=None):
    try:
        if forced_lang and forced_lang != "en":
            detected_lang = forced_lang
        elif len(user_input.strip()) < 5:
            detected_lang = "en"
        else:
            try:
                detected_lang = detect(user_input)
                valid_langs = list(lang_map.keys())
                if detected_lang not in valid_langs and forced_lang:
                    detected_lang = forced_lang
                elif detected_lang not in valid_langs:
                    detected_lang = "en"
            except:
                detected_lang = forced_lang if forced_lang else "en"
    except:
        detected_lang = "en"

    flag, lang_name, gtts_code = lang_map.get(detected_lang, ("🌐", detected_lang.upper(), "en"))

    with st.chat_message("user"):
        st.write(user_input)
        st.markdown(f'<div class="lang-badge">{flag} {lang_name} detected</div>', unsafe_allow_html=True)

    try:
        english_input = GoogleTranslator(source="auto", target="en").translate(user_input)
    except:
        english_input = user_input

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are a helpful assistant. Keep responses concise and friendly."},
                *[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages[-6:]],
                {"role": "user", "content": english_input}
            ]
        )
        english_reply = response.choices[0].message.content
    except Exception as e:
        english_reply = f"Sorry, could not connect. Error: {str(e)}"

    try:
        final_reply = GoogleTranslator(source="en", target=detected_lang).translate(english_reply) if detected_lang != "en" else english_reply
    except:
        final_reply = english_reply

    with st.chat_message("assistant"):
        st.write(final_reply)
        if st.button("🔊 Speak Reply", key=f"speak_{len(st.session_state.messages)}"):
            speak_text(final_reply, gtts_code)

    st.session_state.messages.append({"role": "user", "content": user_input})
    st.session_state.messages.append({"role": "assistant", "content": final_reply})
    st.session_state.detected_langs.append(detected_lang)

for i, msg in enumerate(st.session_state.messages):
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
        if msg["role"] == "user" and i // 2 < len(st.session_state.detected_langs):
            lang_code = st.session_state.detected_langs[i // 2]
            flag, lang_name, _ = lang_map.get(lang_code, ("🌐", lang_code.upper(), "en"))
            st.markdown(f'<div class="lang-badge">{flag} {lang_name} detected</div>', unsafe_allow_html=True)

st.divider()

selected_voice_lang = st.selectbox(
    "🎤 Select your speaking language before clicking Speak:",
    options=list(voice_lang_options.keys()),
    index=0
)

col1, col2 = st.columns([5, 1])

with col2:
    voice_clicked = st.button("🎤 Speak", use_container_width=True)

with col1:
    user_input = st.chat_input("💬 Type in any language — Hindi, Telugu, Marathi, Spanish...")

if voice_clicked:
    selected_code = voice_lang_options[selected_voice_lang]
    with st.spinner("🎤 Listening... Speak now!"):
        spoken_text, spoken_lang = record_voice(lang_code=selected_code)
    if spoken_text:
        st.success(f"🎙️ You said: **{spoken_text}**")
        process_input(spoken_text, forced_lang=spoken_lang)
    else:
        st.error("❌ Couldn't hear anything. Try again!")

if user_input:
    process_input(user_input)

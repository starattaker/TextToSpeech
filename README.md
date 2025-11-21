# 🗣️ English Practice AI Assistant

**English Practice AI** is a modern, desktop-class application that helps users improve spoken English through interactive role-play conversations.  
It behaves like a real conversational partner — **speaks naturally, listens using deep-learning STT, and gives instant accuracy feedback**.

---

## ✨ Key Features

### 🎙️ Real-time Conversation Loop
The AI speaks → you respond → the app listens instantly using Whisper STT.

### 🧠 Advanced Speech Recognition
Powered by **OpenAI Whisper (Base Model)** for accurate transcription across accents.

### 🗣️ Natural Neural TTS
Uses **Microsoft Edge Neural TTS** for lifelike, non-robotic speech.

### ⚡ Smart NLP Validation
Uses fuzzy logic (TheFuzz) and accepts answers with **≥ 80% similarity**, allowing natural variations.

### 🎨 Modern UI (Dark Mode)
Built using **Flet** featuring:
- Animated glitter background  
- Responsive cards  
- Clean and minimal dark-theme layout  

### 📚 Three Practice Scenarios
- Train Inquiry  
- Home Loan Assistance  
- College Function Chief Guest  

---

## 🛠️ Tech Stack

| Component        | Technology               | Reason                                      |
|------------------|---------------------------|----------------------------------------------|
| Frontend UI      | Flet (Flutter for Python) | Beautiful, reactive UI with animations       |
| Speech-to-Text   | Whisper (Base)            | Superior accuracy vs Vosk/Sphinx             |
| Text-to-Speech   | Edge-TTS                  | Free Microsoft Neural voices                 |
| Audio Engine     | Pygame                    | Smooth background audio playback             |
| NLP Matching     | TheFuzz                   | Flexible Levenshtein-based similarity check  |

---

## ⚙️ Installation

### **Prerequisites**
- Python **3.10+**
- **FFmpeg** installed and added to PATH  
  - Windows: `winget install Gyan.FFmpeg`  
  - Mac: `brew install ffmpeg`  
  - Linux: `sudo apt install ffmpeg`

---

### **Setup Steps**

```bash
# Clone the repository
git clone https://github.com/yourusername/english-practice-ai.git
cd english-practice-ai

# Create a virtual environment
python -m venv venv

# Activate it
# Windows:
.\venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

#Launch App
python app.py
```
##👂 STT (Speech-to-Text)

Technology Used: OpenAI Whisper (Base Model)
Library: openai-whisper + SpeechRecognition

###How it works:
-Capture: When the user clicks the recording icon, the SpeechRecognition library activates the microphone and listens for voice input.
-Save: The captured audio is temporarily saved as a .wav file in the system's temp folder.
-Transcribe: The Python script passes this .wav file to the Whisper Model. Whisper is a deep learning model trained on 680,000 hours of multilingual data. It analyzes the audio waveforms and converts them into a text string (e.g., "Yes, please").
-Result: This text string is returned to the main app for checking.

##🗣️ TTS (Text-to-Speech)

###Technology Used: Microsoft Edge Neural Voices
Library: edge-tts + pygame

###How it works:

-Request: When the AI needs to speak (e.g., "Excuse me, Madam"), the app sends this text to the edge-tts library.
-Generation: edge-tts communicates with Microsoft's online Neural TTS service (the same one used in the Edge browser's "Read Aloud" feature). This generates a high-quality, human-like audio stream.
-Playback: The audio is saved as a temporary .mp3 file. To avoid opening visible media players (like Windows Media Player), we use pygame.mixer, which is a game audio engine. It plays the file invisibly in the background.

##🧠 NLP (Natural Language Processing)

Technology Used: Fuzzy Logic / Levenshtein Distance
Library: thefuzz

###How it works:

-The Problem: Humans are inconsistent. If the script says "Yes, please", but the user says "Yeah, please" or "Yes please", a strict code check (if user == expected) would fail.
-The Solution: We use Fuzzy Matching. This algorithm calculates the "Levenshtein Distance"—essentially counting how many edits (insertions, deletions, or substitutions) it takes to turn the user's sentence into the expected sentence.

-The Threshold: The app calculates a similarity score from 0 to 100.

If Score >= 80: The app marks it as Correct.
If Score < 80: The app marks it as Incorrect and asks to retry.

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

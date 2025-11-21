import flet as ft
import asyncio
import edge_tts
import speech_recognition as sr
import whisper
import os
import tempfile
import pygame
import warnings
import random
from thefuzz import fuzz

# --- CONFIGURATION & DATA ---
STT_MODEL_SIZE = "base"
VOICE = "en-US-AriaNeural"
warnings.filterwarnings("ignore")

# Scenario Data
SCENARIOS = {
    "train": {
        "title": "Train Inquiry",
        "icon": "train",
        "desc": "Ask about schedules",
        "dialogue": [
            {"ai": "Excuse me, Madam.", "user": "Yes, Please."},
            {"ai": "Could you please tell me, what time is the next train to Ahmedabad?", "user": "The next departure is scheduled at 6:45 pm."},
            {"ai": "Are you aware, what time it will reach Ahmedabad?", "user": "It reaches Ahmedabad around 4 am, early morning."},
            {"ai": "Ok. Thank you for the information.", "user": "You are welcome."}
        ]
    },
    "loan": {
        "title": "Home Loan Info",
        "icon": "home", 
        "desc": "Bank assistance",
        "dialogue": [
            {"ai": "Excuse me. Would you please tell me, who could give me information about the home loan?", "user": "The lady at the 3rd counter is from the home loan department. She would assist you."},
            {"ai": "Thank you!", "user": "You are welcome."},
            {"ai": "Excuse me madam, I would like to get the information about the home loan.", "user": "Sure. You please fill in this form and I would give you all the related information."}
        ]
    },
    "college": {
        "title": "College Function",
        "icon": "school",
        "desc": "Chief guest details",
        "dialogue": [
            {"ai": "Hello, who is the chief guest for today's college function?", "user": "Mr. Joshi has been invited as the chief guest."},
            {"ai": "When will he be coming here?", "user": "He has confirmed that he will reach the venue by 6 p.m."},
            {"ai": "What is his occupation?", "user": "He is a famous social worker."},
            {"ai": "Okay, is he the one who was recently in the news for movement against child labour?", "user": "Yes, you got it right."}
        ]
    }
}

# --- AI BACKEND CLASS ---
class EnglishAI:
    def __init__(self):
        self.model = None
        self.recognizer = sr.Recognizer()
        pygame.mixer.init()

    def load_model(self):
        if not self.model:
            print("Loading Whisper... (One time only)")
            self.model = whisper.load_model(STT_MODEL_SIZE)

    def stop_audio(self):
        """Forces audio to stop immediately."""
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()
            pygame.mixer.music.unload()

    async def speak(self, text):
        communicate = edge_tts.Communicate(text, VOICE)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
            temp_filename = fp.name
        await communicate.save(temp_filename)
        try:
            pygame.mixer.music.load(temp_filename)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                # Check if we need to abort (e.g. user left page)
                await asyncio.sleep(0.1)
            pygame.mixer.music.unload()
        except Exception as e:
            print(f"Audio Error: {e}")
        finally:
            try: os.remove(temp_filename)
            except: pass

    def listen(self):
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
            try:
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=8)
                with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as fp:
                    fp.write(audio.get_wav_data())
                    audio_filename = fp.name
                
                result = self.model.transcribe(audio_filename)
                text = result["text"].strip()
                os.remove(audio_filename)
                return text
            except Exception:
                return ""

    def check_similarity(self, user_text, expected_text):
        if not user_text: return 0
        return fuzz.ratio(user_text.lower(), expected_text.lower())

ai_engine = EnglishAI()

# --- VISUAL EFFECTS: GLITTER/STARS ---
class StarField(ft.Stack):
    """Python equivalent of the Glitter effect using Flet Animations"""
    def __init__(self, page_width, page_height, star_count=60):
        super().__init__()
        self.stars = []
        # FIX: Ensure width/height are integers and default to 1080p if None
        w = int(page_width if page_width else 1920)
        h = int(page_height if page_height else 1080)
        
        self.width = w
        self.height = h
        
        for _ in range(star_count):
            left = random.randint(0, w)
            top = random.randint(0, h)
            size = random.randint(2, 4)
            
            star = ft.Container(
                width=size, height=size,
                bgcolor="white",
                border_radius=50,
                left=left, top=top,
                opacity=random.random(),
                animate_opacity=ft.Animation(duration=random.randint(1000, 3000), curve="easeInOut")
            )
            self.stars.append(star)
            self.controls.append(star)

    async def animate(self):
        while True:
            for star in self.stars:
                star.opacity = random.random()
                star.update()
            await asyncio.sleep(2)

# --- UI APPLICATION ---
async def main(page: ft.Page):
    page.title = "English Practice AI"
    page.theme_mode = ft.ThemeMode.DARK
    page.fonts = {"Inter": "https://fonts.gstatic.com/s/inter/v12/UcC73FwrK3iLTeHuS_fvQtMwCp50KnMa1ZL7.ttf"}
    page.theme = ft.Theme(font_family="Inter")
    
    ai_engine.load_model()

    # State to handle stopping audio when leaving pages
    state = {"is_active": True}

    # --- VIEW 1: THE DEV JOURNEY PAGE ---
    async def show_journey(e=None):
        page.clean()
        state["is_active"] = False
        ai_engine.stop_audio()
        
        # SCROLL FIX: Enable scrolling on the PAGE level
        page.scroll = ft.ScrollMode.AUTO
        page.vertical_alignment = ft.MainAxisAlignment.START
        page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        
        async def go_back(e):
            page.scroll = None # Disable scrolling when leaving this page
            await show_landing()

        def section_header(text):
            return ft.Text(text, size=24, weight="bold", color=ft.Colors.CYAN_400, font_family="Inter")
        
        def body_text(text):
            return ft.Text(text, size=16, color=ft.Colors.GREY_400, font_family="Inter")

        def tech_card(name, desc):
            return ft.Container(
                content=ft.Column([
                    ft.Text(name, weight="bold", color="white"),
                    ft.Text(desc, size=12, color="grey")
                ]),
                padding=15, bgcolor=ft.Colors.GREY_900, border_radius=10, width=300
            )

        content = ft.Column([
            ft.Container(height=20),
            ft.Row([
                ft.IconButton("arrow_back", on_click=go_back),
                ft.Text("The Development Journey", size=30, weight="bold")
            ]),
            ft.Divider(color="transparent"),
            
            section_header("From Prototype to Production"),
            body_text("This project started with a simple goal: build an English practice partner. Initially, we used basic tools like 'pyttsx3' for speech and 'Vosk' for listening. However, we faced challenges: the robotic voice wasn't engaging, and Vosk struggled with Indian accents."),
            ft.Container(height=10),
            body_text("We decided to overhaul the core. We replaced the old engine with OpenAI's Whisper (for state-of-the-art accuracy) and Microsoft Edge Neural TTS (for lifelike human voices). We also moved from a command-line interface to this modern Flet UI."),
            
            ft.Divider(height=40, color=ft.Colors.GREY_800),
            
            section_header("The Tech Stack"),
            ft.Container(height=10),
            ft.Row([
                tech_card("Flet (UI)", "Modern React-like Python framework for beautiful interfaces."),
                tech_card("OpenAI Whisper", "Deep learning model for high-accuracy Speech-to-Text."),
            ], alignment="center"),
            ft.Container(height=10),
            ft.Row([
                tech_card("Edge-TTS", "Microsoft Azure's Neural voices for natural speech."),
                tech_card("TheFuzz", "Fuzzy logic NLP to match user intent with 80% tolerance."),
            ], alignment="center"),
             ft.Container(height=10),
            ft.Row([
                tech_card("Pygame", "Invisible background audio mixer for seamless playback."),
            ], alignment="center"),
            
            ft.Container(height=50), # Extra space at bottom

        ], width=700) # SCROLL FIX: Removed scroll=AUTO from here, handled by Page

        page.add(content)

    # --- VIEW 2: CONVERSATION ---
    async def start_conversation(scenario_key):
        page.clean()
        state["is_active"] = True
        data = SCENARIOS[scenario_key]
        dialogue_list = data["dialogue"]
        current_step = 0

        chat_list = ft.ListView(expand=True, spacing=15, padding=20, auto_scroll=True)
        status_text = ft.Text("Initializing...", italic=True, color="grey")
        hint_text = ft.Text("", color=ft.Colors.CYAN_200, size=16, weight="bold")
        mic_icon = ft.Icon(name="mic", size=40, color="grey")
        
        def add_chat_bubble(text, is_ai=True):
            bubble = ft.Container(
                content=ft.Text(text, size=16, font_family="Inter"),
                padding=20,
                border_radius=ft.border_radius.only(
                    top_left=20, top_right=20, 
                    bottom_left=0 if is_ai else 20, 
                    bottom_right=20 if is_ai else 0
                ),
                bgcolor=ft.Colors.GREY_800 if is_ai else ft.Colors.CYAN_900,
                alignment=ft.alignment.center_left if is_ai else ft.alignment.center_right,
                margin=ft.margin.only(right=50) if is_ai else ft.margin.only(left=50),
                shadow=ft.BoxShadow(blur_radius=5, color=ft.Colors.BLACK26)
            )
            chat_list.controls.append(bubble)
            page.update()

        async def play_turn():
            nonlocal current_step
            if not state["is_active"]: return

            if current_step >= len(dialogue_list):
                add_chat_bubble("Conversation Complete! returning to menu...", True)
                await asyncio.sleep(3)
                if state["is_active"]: await show_scenarios()
                return

            line = dialogue_list[current_step]
            
            status_text.value = "AI is speaking..."
            mic_icon.color = "grey"
            page.update()
            
            add_chat_bubble(line["ai"], True)
            await ai_engine.speak(line["ai"])
            
            if not state["is_active"]: return 

            hint_text.value = f"Hint: Say '{line['user']}'"
            status_text.value = "Listening... Speak now!"
            mic_icon.color = "red"
            mic_icon.scale = 1.2
            page.update()
            
            loop = asyncio.get_running_loop()
            user_text = await loop.run_in_executor(None, ai_engine.listen)
            
            mic_icon.color = "grey"
            mic_icon.scale = 1.0
            
            if not state["is_active"]: return 

            if not user_text:
                status_text.value = "Didn't hear anything. Trying again..."
                page.update()
                await asyncio.sleep(1)
                await play_turn()
                return

            add_chat_bubble(user_text, False)
            score = ai_engine.check_similarity(user_text, line["user"])
            if score >= 80:
                status_text.value = f"Correct! (Match: {score}%)"
                status_text.color = "green"
                page.update()
                await ai_engine.speak("Good job!")
                current_step += 1
                await asyncio.sleep(1)
                await play_turn()
            else:
                status_text.value = f"Not quite. (Match: {score}%) Try again."
                status_text.color = "red"
                page.update()
                await ai_engine.speak("Let's try that again.")
                await play_turn()

        async def go_back(e):
            state["is_active"] = False 
            ai_engine.stop_audio() 
            await show_scenarios()

        page.add(ft.Column([
            ft.Container(
                content=ft.Row([ft.IconButton("arrow_back", on_click=go_back), ft.Text(data["title"], size=20, weight="bold")]),
                padding=10, bgcolor=ft.Colors.GREY_900
            ),
            chat_list,
            ft.Divider(height=1, color="transparent"),
            ft.Container(
                content=ft.Column([hint_text, ft.Row([mic_icon, status_text], alignment="center")], horizontal_alignment="center"),
                padding=20, bgcolor=ft.Colors.GREY_900, border_radius=ft.border_radius.only(top_left=20, top_right=20)
            )
        ], expand=True))
        await asyncio.sleep(1)
        await play_turn()

    # --- VIEW 3: SCENARIO SELECTION ---
    async def show_scenarios(e=None):
        page.clean()
        state["is_active"] = False
        ai_engine.stop_audio()

        page.vertical_alignment = ft.MainAxisAlignment.START
        page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

        def create_card(key, info):
            async def on_card_click(e): await start_conversation(key)
            return ft.Container(
                content=ft.Column([
                    ft.Icon(name=info["icon"], size=45, color=ft.Colors.CYAN_200),
                    ft.Container(height=10),
                    ft.Text(info["title"], size=18, weight="bold", color="white"),
                    ft.Text(info["desc"], size=12, color="grey", italic=True)
                ], alignment="center", horizontal_alignment="center"),
                width=200, height=200, bgcolor=ft.Colors.GREY_900,
                border=ft.border.all(1, ft.Colors.CYAN_400), border_radius=20, padding=20,
                on_click=on_card_click, shadow=ft.BoxShadow(blur_radius=15, spread_radius=1, color=ft.Colors.CYAN_900),
                animate_scale=ft.Animation(100, "easeOut"),
                on_hover=lambda e: card_hover(e.control, e.data)
            )

        def card_hover(card, is_hovering):
            card.scale = 1.05 if is_hovering == "true" else 1.0
            card.border = ft.border.all(2, ft.Colors.CYAN_200) if is_hovering == "true" else ft.border.all(1, ft.Colors.CYAN_400)
            card.update()

        instructions = ft.Container(
            content=ft.Column([
                ft.Text("How it works", weight="bold", color=ft.Colors.CYAN_400),
                ft.Text("• The AI will speak first (Line A), and you'll need to respond (Line B)"),
                ft.Text("• Click the microphone button and speak your response clearly"),
                ft.Text("• The app will check if your response matches (80% threshold)"),
                ft.Text("• If correct, you'll move to the next line. If not, try again!")
            ], spacing=5),
            padding=20, border=ft.border.all(1, ft.Colors.GREY_800), border_radius=10, bgcolor=ft.Colors.GREY_900, width=650
        )
        
        async def go_home(e): await show_landing()

        # Navigation Bar
        nav_bar = ft.Container(
            content=ft.Row([
                ft.IconButton("home", on_click=go_home, tooltip="Back to Home"),
                ft.Text("Scenarios", size=20, weight="bold")
            ]),
            padding=10
        )

        page.add(ft.Column([
            nav_bar,
            ft.Container(height=20),
            ft.Text("Choose a Scenario", size=35, weight="bold", font_family="Inter"),
            ft.Container(height=20),
            instructions,
            ft.Container(height=40),
            ft.Row([create_card(k, v) for k, v in SCENARIOS.items()], alignment="center", wrap=True, spacing=30)
        ], horizontal_alignment="center", alignment="center"))

    # --- VIEW 4: LANDING PAGE ---
    async def show_landing(e=None):
        page.clean()
        state["is_active"] = False
        ai_engine.stop_audio()

        page.vertical_alignment = ft.MainAxisAlignment.CENTER
        
        # 1. Glitter Effect Layer
        # FIX: Changed page.window_width to page.width (window_width is deprecated)
        stars = StarField(page.width, page.height)
        
        async def on_start_click(e): await show_scenarios()
        
        titles = ["amazing", "new", "wonderful", "beautiful", "smart"]
        animated_text = ft.Text(value=titles[0], size=60, weight="bold", color=ft.Colors.CYAN_400,
                                animate_opacity=300, offset=ft.Offset(0,0), 
                                animate_offset=ft.Animation(300, "easeOut"))

        async def animate_text_loop():
            idx = 0
            while True:
                try:
                    await asyncio.sleep(2)
                    animated_text.opacity = 0; animated_text.offset = ft.Offset(0, -0.5); animated_text.update()
                    await asyncio.sleep(0.3)
                    idx = (idx + 1) % len(titles)
                    animated_text.value = titles[idx]
                    animated_text.offset = ft.Offset(0, 0.5); animated_text.update()
                    animated_text.opacity = 1; animated_text.offset = ft.Offset(0, 0); animated_text.update()
                except: break
        
        asyncio.create_task(animate_text_loop())
        asyncio.create_task(stars.animate())

        badge = ft.Container(
            content=ft.Row([ft.Text("Read how I was made", size=12), ft.Icon("info", size=14)], alignment="center"),
            padding=ft.padding.symmetric(horizontal=15, vertical=8),
            border_radius=20, bgcolor=ft.Colors.GREY_900,
            on_click=show_journey
        )

        features = ft.Row(
            [
                ft.Text("No sign-up required", color="grey", size=12),
                ft.Text("•", color="grey"),
                ft.Text("Works locally", color="grey", size=12),
                ft.Text("•", color="grey"),
                ft.Text("Free to use", color="grey", size=12),
            ],
            alignment="center"
        )

        main_content = ft.Column([
            badge,
            ft.Container(height=20),
            ft.Column([ft.Text("This is something", size=60, weight="bold", color="white"), ft.Container(content=animated_text, height=80)], spacing=0, horizontal_alignment="center"),
            ft.Text("Master spoken English with AI.", size=18, color="grey", text_align="center"),
            ft.Container(height=20),
            features,
            ft.Container(height=40),
            ft.ElevatedButton("Start Learning", icon="arrow_forward", height=50, color="black", bgcolor="white", on_click=on_start_click)
        ], horizontal_alignment="center", alignment="center")

        page.add(ft.Stack([
            stars,
            ft.Container(content=main_content, alignment=ft.alignment.center)
        ], expand=True))

    await show_landing()

if __name__ == "__main__":
    ft.app(target=main)
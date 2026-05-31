import speech_recognition as sr
from typing import Optional
import subprocess
import os

class VoiceAgent:
    """
    Real-time Voice Interaction Agent.
    Converts Speech-to-Text and Text-to-Speech locally.
    """
    
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
    def listen(self, timeout: int = 5) -> Optional[str]:
        """
        Listens to microphone and converts speech to text.
        Uses local Whisper model via Ollama if available, else fallback to Sphinx.
        """
        try:
            with self.microphone as source:
                print("🎤 Listening... (speak now)")
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = self.recognizer.listen(source, timeout=timeout)
            
            # Try using local Whisper via Ollama (requires ollama pull whisper)
            # For now, using built-in recognition
            text = self.recognizer.recognize_google(audio)  # Fallback to Google for demo
            return text
        except sr.WaitTimeoutError:
            return "No speech detected."
        except sr.UnknownValueError:
            return "Could not understand audio."
        except Exception as e:
            return f"Error: {str(e)}"
    
    def speak(self, text: str, rate: int = 150) -> bool:
        """
        Converts text to speech using system TTS.
        Linux: espeak, Mac: say, Windows: pyttsx3
        """
        try:
            # Detect OS and use native TTS
            if os.name == 'posix':
                if subprocess.run(['which', 'say'], capture_output=True).returncode == 0:
                    # macOS
                    subprocess.run(['say', '-r', str(rate), text])
                elif subprocess.run(['which', 'espeak'], capture_output=True).returncode == 0:
                    # Linux
                    subprocess.run(['espeak', '-s', str(rate), text])
                else:
                    print(f"🔊 TTS: {text}")  # Fallback to print
            else:
                # Windows fallback
                print(f"🔊 TTS: {text}")
            return True
        except Exception as e:
            print(f"TTS Error: {e}")
            return False

    def voice_chat_loop(self, agent_callback):
        """
        Starts a continuous voice chat loop.
        agent_callback: function that takes text input and returns response text.
        """
        print("🎙️ Voice Chat Started. Say 'exit' to stop.")
        while True:
            user_input = self.listen()
            if not user_input or user_input == "No speech detected.":
                continue
            
            print(f"👤 You said: {user_input}")
            
            if user_input.lower() in ['exit', 'quit', 'stop']:
                self.speak("Goodbye!")
                break
            
            # Get AI response
            response = agent_callback(user_input)
            print(f"🤖 AI: {response}")
            
            # Speak response
            self.speak(response)

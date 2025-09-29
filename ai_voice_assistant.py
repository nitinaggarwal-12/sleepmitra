"""
AI Voice Assistant for SleepMitra
This module provides voice-to-text and AI-powered responses in Hindi
"""

import streamlit as st
import openai
import speech_recognition as sr
import pyttsx3
from datetime import datetime
import os

class SleepMitraVoiceAssistant:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.tts_engine = pyttsx3.init()
        self.setup_tts()
    
    def setup_tts(self):
        """Setup text-to-speech engine for Hindi"""
        voices = self.tts_engine.getProperty('voices')
        # Try to find Hindi voice
        for voice in voices:
            if 'hindi' in voice.name.lower() or 'indian' in voice.name.lower():
                self.tts_engine.setProperty('voice', voice.id)
                break
        
        # Set speech rate and volume
        self.tts_engine.setProperty('rate', 150)  # Speed of speech
        self.tts_engine.setProperty('volume', 0.8)  # Volume level
    
    def listen_to_voice(self):
        """Listen to user's voice and convert to text"""
        try:
            with self.microphone as source:
                st.info("🎤 सुन रहा हूं... बोलिए")
                self.recognizer.adjust_for_ambient_noise(source)
                audio = self.recognizer.listen(source, timeout=5)
            
            # Convert speech to text
            text = self.recognizer.recognize_google(audio, language='hi-IN')
            return text
        except sr.WaitTimeoutError:
            return "समय समाप्त - कोई आवाज नहीं सुनी गई"
        except sr.UnknownValueError:
            return "आवाज समझ नहीं आई - कृपया दोबारा बोलें"
        except Exception as e:
            return f"त्रुटि: {str(e)}"
    
    def get_ai_response(self, user_question):
        """Get AI response using OpenAI API"""
        try:
            # Set up OpenAI API
            openai.api_key = st.secrets.get("OPENAI_API_KEY", os.getenv("OPENAI_API_KEY"))
            
            if not openai.api_key:
                return "OpenAI API key नहीं मिली। कृपया API key सेट करें।"
            
            # Create prompt for sleep-related questions in Hindi
            prompt = f"""
            आप SleepMitra के AI असिस्टेंट हैं। नींद चिकित्सा विशेषज्ञ के रूप में हिंदी में जवाब दें।
            
            उपयोगकर्ता का सवाल: {user_question}
            
            कृपया:
            1. हिंदी में जवाब दें
            2. नींद चिकित्सा के विशेषज्ञ के रूप में सलाह दें
            3. व्यावहारिक सुझाव दें
            4. यदि गंभीर समस्या है तो डॉक्टर से मिलने की सलाह दें
            5. 2-3 वाक्यों में संक्षिप्त जवाब दें
            """
            
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "आप SleepMitra के AI असिस्टेंट हैं। नींद चिकित्सा विशेषज्ञ के रूप में हिंदी में जवाब दें।"},
                    {"role": "user", "content": user_question}
                ],
                max_tokens=200,
                temperature=0.7
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"AI से जवाब नहीं मिल सका: {str(e)}"
    
    def speak_response(self, text):
        """Convert text to speech"""
        try:
            self.tts_engine.say(text)
            self.tts_engine.runAndWait()
        except Exception as e:
            st.error(f"आवाज में जवाब नहीं सुना सका: {str(e)}")
    
    def process_voice_query(self):
        """Complete voice processing pipeline"""
        # Step 1: Listen to voice
        user_text = self.listen_to_voice()
        
        if "त्रुटि" in user_text or "समय समाप्त" in user_text:
            return user_text, ""
        
        # Step 2: Get AI response
        ai_response = self.get_ai_response(user_text)
        
        # Step 3: Speak response
        self.speak_response(ai_response)
        
        return user_text, ai_response

# Streamlit integration functions
def setup_voice_assistant():
    """Setup voice assistant in Streamlit"""
    if 'voice_assistant' not in st.session_state:
        st.session_state.voice_assistant = SleepMitraVoiceAssistant()
    return st.session_state.voice_assistant

def voice_chat_interface():
    """Voice chat interface for Streamlit"""
    assistant = setup_voice_assistant()
    
    st.subheader("🎤 वॉइस चैट")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown("""
        <div style="padding: 1rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border-radius: 10px; margin: 1rem 0;">
            <h4 style="color: white; margin: 0 0 1rem 0;">🎤 वॉइस असिस्टेंट</h4>
            <p style="margin: 0 0 0.5rem 0;">• "हेलो, मुझे नींद नहीं आ रही"</p>
            <p style="margin: 0 0 0.5rem 0;">• "CBT-I थेरेपी क्या है?"</p>
            <p style="margin: 0 0 0.5rem 0;">• "डॉक्टर से कब मिलना चाहिए?"</p>
            <p style="margin: 0;">• "अपॉइंटमेंट कैसे बुक करें?"</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        if st.button("🎤 वॉइस रिकॉर्ड करें", use_container_width=True, key="voice_record_ai"):
            with st.spinner("🎤 सुन रहा हूं..."):
                user_question, ai_response = assistant.process_voice_query()
            
            if user_question and ai_response:
                # Display conversation
                st.markdown("### 💬 वॉइस चैट")
                
                # User question
                st.markdown(f"""
                <div style="background: #e3f2fd; padding: 1rem; border-radius: 10px; margin: 0.5rem 0;">
                    <strong>👤 आप:</strong> {user_question}
                </div>
                """, unsafe_allow_html=True)
                
                # AI response
                st.markdown(f"""
                <div style="background: #e8f5e8; padding: 1rem; border-radius: 10px; margin: 0.5rem 0;">
                    <strong>🤖 AI असिस्टेंट:</strong> {ai_response}
                </div>
                """, unsafe_allow_html=True)
                
                # Save to chat history
                if 'voice_chat_history' not in st.session_state:
                    st.session_state.voice_chat_history = []
                
                st.session_state.voice_chat_history.append({
                    'timestamp': datetime.now().strftime("%H:%M:%S"),
                    'user': user_question,
                    'ai': ai_response
                })
    
    # Display voice chat history
    if 'voice_chat_history' in st.session_state and st.session_state.voice_chat_history:
        st.markdown("### 📝 वॉइस चैट हिस्ट्री")
        
        for chat in reversed(st.session_state.voice_chat_history[-5:]):  # Show last 5
            st.markdown(f"""
            <div style="background: #f8f9fa; padding: 1rem; border-radius: 10px; margin: 0.5rem 0; border-left: 4px solid #6C5CE7;">
                <small style="color: #666;">{chat['timestamp']}</small>
                <p><strong>👤 आप:</strong> {chat['user']}</p>
                <p><strong>🤖 AI:</strong> {chat['ai']}</p>
            </div>
            """, unsafe_allow_html=True)

# Configuration instructions
def show_ai_setup_instructions():
    """Show instructions for setting up AI voice assistant"""
    st.markdown("---")
    st.subheader("🔧 AI वॉइस असिस्टेंट सेटअप")
    
    with st.expander("AI वॉइस असिस्टेंट कैसे सेटअप करें?", expanded=False):
        st.markdown("""
        ### 📋 आवश्यक सेटअप:
        
        **1. Python पैकेज इंस्टॉल करें:**
        ```bash
        pip install openai speechrecognition pyttsx3 pyaudio
        ```
        
        **2. OpenAI API Key सेट करें:**
        - [OpenAI](https://platform.openai.com/api-keys) से API key प्राप्त करें
        - Streamlit secrets में जोड़ें:
        ```toml
        # .streamlit/secrets.toml
        OPENAI_API_KEY = "your-api-key-here"
        ```
        
        **3. माइक्रोफोन अनुमति:**
        - ब्राउज़र को माइक्रोफोन एक्सेस दें
        - HTTPS कनेक्शन आवश्यक
        
        **4. हिंदी TTS वॉइस:**
        - Windows: Hindi voice pack इंस्टॉल करें
        - macOS: System Preferences में Hindi voice सेट करें
        - Linux: espeak या festival इंस्टॉल करें
        """)
        
        st.code("""
        # Example usage in your Streamlit app:
        from ai_voice_assistant import voice_chat_interface
        
        # In your chatbot page:
        voice_chat_interface()
        """, language="python")

if __name__ == "__main__":
    # Test the voice assistant
    st.title("🎤 SleepMitra Voice Assistant Test")
    voice_chat_interface()
    show_ai_setup_instructions()

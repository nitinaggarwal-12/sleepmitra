import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
import openai
import requests
from typing import Dict, List, Any

# AI Voice Assistant Functions
def get_ai_response(user_message: str) -> str:
    """Get AI response from OpenAI GPT-4 for Hindi sleep-related queries"""
    try:
        # Get API key from secrets (try multiple methods)
        api_key = None
        
        # Method 1: Direct access
        try:
            api_key = st.secrets["OPENAI_API_KEY"]
        except:
            pass
        
        # Method 2: Get method
        if not api_key:
            try:
                api_key = st.secrets.get("OPENAI_API_KEY")
            except:
                pass
        
        # Method 3: Environment variable fallback
        if not api_key:
            import os
            api_key = os.getenv("OPENAI_API_KEY")
        
        if not api_key:
            # Debug information
            debug_info = []
            try:
                debug_info.append(f"Secrets available: {list(st.secrets.keys())}")
            except:
                debug_info.append("No secrets available")
            
            try:
                import os
                env_keys = [k for k in os.environ.keys() if 'OPENAI' in k]
                debug_info.append(f"Environment variables: {env_keys}")
            except:
                debug_info.append("No environment variables found")
            
            return f"❌ OpenAI API key not configured.\n\nDebug info:\n" + "\n".join(debug_info) + "\n\nPlease add OPENAI_API_KEY to Streamlit Cloud secrets."
        
        # Initialize OpenAI client
        client = openai.OpenAI(api_key=api_key)
        
        # Create a sleep therapy expert prompt
        system_prompt = """You are a female Hindi-speaking sleep therapy expert from North India. 
        You help patients with sleep problems in Hindi. Speak like a caring, knowledgeable North Indian woman.
        Use North Indian Hindi expressions, be warm and motherly in your tone.
        Always respond in Hindi (Devanagari script). Keep responses concise but informative.
        Use phrases like "बेटा/बेटी", "अरे हां", "देखिए", "समझिए", "अच्छा".
        Focus on CBT-I techniques, sleep hygiene, and when to see a doctor.
        Be empathetic and use North Indian cultural references when appropriate."""
        
        # Get response from OpenAI
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            max_tokens=300,
            temperature=0.7
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        return f"❌ AI असिस्टेंट में त्रुटि: {str(e)}"

def process_voice_input(transcribed_text: str) -> str:
    """Process voice input and return AI response"""
    if not transcribed_text.strip():
        return "कृपया अपना सवाल स्पष्ट रूप से बोलें।"
    
    # Get AI response
    ai_response = get_ai_response(transcribed_text)
    return ai_response

# Page configuration
st.set_page_config(
    page_title="SleepMitra - Hindi Insomnia Management System",
    page_icon="🌙",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Hindi support
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+Devanagari:wght@300;400;500;600;700&display=swap');
    
    .main {
        font-family: 'Noto Sans Devanagari', sans-serif;
    }
    
    .hindi-text {
        font-family: 'Noto Sans Devanagari', sans-serif;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        margin: 0.5rem 0;
    }
    
    .assessment-card {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #6C5CE7;
        margin: 1rem 0;
    }
    
    .success-card {
        background: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    
    .warning-card {
        background: #fff3cd;
        border: 1px solid #ffeaa7;
        color: #856404;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    
    .danger-card {
        background: #f8d7da;
        border: 1px solid #f5c6cb;
        color: #721c24;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    
    /* Navigation button styles */
    .stButton > button {
        font-family: 'Noto Sans Devanagari', sans-serif;
        font-weight: 500;
        border-radius: 8px;
        border: 2px solid #e1e5e9;
        background: white;
        color: #333;
        transition: all 0.3s ease;
        margin-bottom: 0.5rem;
    }
    
    .stButton > button:hover {
        border-color: #6C5CE7;
        background: rgba(108, 92, 231, 0.1);
        color: #6C5CE7;
        transform: translateY(-1px);
        box-shadow: 0 2px 8px rgba(108, 92, 231, 0.2);
    }
    
    .stButton > button:active {
        transform: translateY(0);
    }
    
    /* Active page indicator */
    .active-page {
        border-color: #6C5CE7 !important;
        background: linear-gradient(135deg, #6C5CE7, #00B894) !important;
        color: white !important;
        box-shadow: 0 2px 8px rgba(108, 92, 231, 0.3) !important;
    }
    
    /* Reduce spacing for compact layout */
    .main .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
    }
    
    .stHeader {
        margin-bottom: 0.5rem;
    }
    
    .stSubheader {
        margin-top: 0.5rem;
        margin-bottom: 0.5rem;
    }
    
    .element-container {
        margin-bottom: 0.5rem;
    }
    
    /* Main logo button styling */
    div[data-testid="column"] button[kind="secondary"][title="Click to go to Dashboard"] {
        background: transparent !important;
        border: none !important;
        color: #6C5CE7 !important;
        font-size: 2rem !important;
        font-weight: bold !important;
        padding: 0.5rem 1rem !important;
        margin: 0 !important;
        box-shadow: none !important;
    }
    
    div[data-testid="column"] button[kind="secondary"][title="Click to go to Dashboard"]:hover {
        background: rgba(108, 92, 231, 0.1) !important;
        color: #6C5CE7 !important;
        transform: none !important;
    }
    
</style>
""", unsafe_allow_html=True)

# Doctor profiles database
DOCTORS = [
    {
        'id': 'dr_rajesh_kumar',
        'name': 'डॉ. राजेश कुमार',
        'specialty': 'नींद चिकित्सा विशेषज्ञ',
        'qualification': 'MD, Sleep Medicine, AIIMS',
        'experience': '15+ वर्ष',
        'languages': ['हिंदी', 'English', 'पंजाबी'],
        'location': 'दिल्ली',
        'clinic': 'SleepCare Clinic, CP',
        'rating': 4.8,
        'patients_treated': 2500,
        'consultation_fee': 1500,
        'availability': ['Monday', 'Wednesday', 'Friday'],
        'time_slots': ['10:00 AM', '2:00 PM', '4:00 PM'],
        'specialties': ['CBT-I', 'Sleep Apnea', 'Insomnia'],
        'bio': 'नींद चिकित्सा में 15+ वर्ष का अनुभव। CBT-I और नींद विकारों के विशेषज्ञ।',
        'image': '👨‍⚕️'
    },
    {
        'id': 'dr_priya_sharma',
        'name': 'डॉ. प्रिया शर्मा',
        'specialty': 'मनोचिकित्सक और नींद विशेषज्ञ',
        'qualification': 'MD Psychiatry, MBBS',
        'experience': '12+ वर्ष',
        'languages': ['हिंदी', 'English', 'मराठी'],
        'location': 'मुंबई',
        'clinic': 'Mind & Sleep Center, Bandra',
        'rating': 4.9,
        'patients_treated': 1800,
        'consultation_fee': 2000,
        'availability': ['Tuesday', 'Thursday', 'Saturday'],
        'time_slots': ['11:00 AM', '3:00 PM', '5:00 PM'],
        'specialties': ['Anxiety & Sleep', 'Depression & Insomnia', 'CBT-I'],
        'bio': 'मनोचिकित्सा और नींद विकारों के विशेषज्ञ। चिंता और नींद की समस्याओं में विशेषज्ञता।',
        'image': '👩‍⚕️'
    },
    {
        'id': 'dr_amit_singh',
        'name': 'डॉ. अमित सिंह',
        'specialty': 'नींद चिकित्सा और श्वसन विशेषज्ञ',
        'qualification': 'MD Pulmonology, Sleep Medicine',
        'experience': '10+ वर्ष',
        'languages': ['हिंदी', 'English', 'गुजराती'],
        'location': 'अहमदाबाद',
        'clinic': 'Respiratory & Sleep Clinic',
        'rating': 4.7,
        'patients_treated': 1200,
        'consultation_fee': 1200,
        'availability': ['Monday', 'Wednesday', 'Friday', 'Sunday'],
        'time_slots': ['9:00 AM', '1:00 PM', '3:00 PM'],
        'specialties': ['Sleep Apnea', 'Snoring', 'CBT-I'],
        'bio': 'श्वसन और नींद विकारों के विशेषज्ञ। स्लीप एपनिया और खर्राटों के उपचार में विशेषज्ञता।',
        'image': '👨‍⚕️'
    },
    {
        'id': 'dr_sunita_reddy',
        'name': 'डॉ. सुनीता रेड्डी',
        'specialty': 'नींद चिकित्सा और मनोविज्ञान',
        'qualification': 'PhD Psychology, Sleep Medicine',
        'experience': '8+ वर्ष',
        'languages': ['हिंदी', 'English', 'तेलुगु', 'तमिल'],
        'location': 'बैंगलोर',
        'clinic': 'Sleep Psychology Center',
        'rating': 4.6,
        'patients_treated': 900,
        'consultation_fee': 1800,
        'availability': ['Tuesday', 'Thursday', 'Saturday'],
        'time_slots': ['10:30 AM', '2:30 PM', '4:30 PM'],
        'specialties': ['Sleep Psychology', 'CBT-I', 'Relaxation Therapy'],
        'bio': 'नींद मनोविज्ञान में विशेषज्ञ। CBT-I और रिलैक्सेशन थेरेपी में अनुभवी।',
        'image': '👩‍⚕️'
    },
    {
        'id': 'dr_vikram_jain',
        'name': 'डॉ. विक्रम जैन',
        'specialty': 'नींद चिकित्सा और न्यूरोलॉजी',
        'qualification': 'MD Neurology, Sleep Medicine',
        'experience': '18+ वर्ष',
        'languages': ['हिंदी', 'English', 'राजस्थानी'],
        'location': 'जयपुर',
        'clinic': 'Neuro Sleep Center',
        'rating': 4.9,
        'patients_treated': 3000,
        'consultation_fee': 2500,
        'availability': ['Monday', 'Wednesday', 'Friday'],
        'time_slots': ['9:30 AM', '1:30 PM', '3:30 PM'],
        'specialties': ['Neurological Sleep Disorders', 'CBT-I', 'Sleep Studies'],
        'bio': 'न्यूरोलॉजी और नींद चिकित्सा के वरिष्ठ विशेषज्ञ। जटिल नींद विकारों के उपचार में विशेषज्ञता।',
        'image': '👨‍⚕️'
    },
    {
        'id': 'dr_meera_patel',
        'name': 'डॉ. मीरा पटेल',
        'specialty': 'नींद चिकित्सा और व्यवहार चिकित्सा',
        'qualification': 'MD, Behavioral Medicine, Sleep Therapy',
        'experience': '6+ वर्ष',
        'languages': ['हिंदी', 'English', 'गुजराती'],
        'location': 'सूरत',
        'clinic': 'Behavioral Sleep Clinic',
        'rating': 4.5,
        'patients_treated': 600,
        'consultation_fee': 1000,
        'availability': ['Tuesday', 'Thursday', 'Saturday'],
        'time_slots': ['11:00 AM', '2:00 PM', '4:00 PM'],
        'specialties': ['Behavioral Sleep Therapy', 'CBT-I', 'Sleep Hygiene'],
        'bio': 'व्यवहार चिकित्सा और नींद थेरेपी में विशेषज्ञ। युवा वयस्कों में नींद की समस्याओं के उपचार में अनुभवी।',
        'image': '👩‍⚕️'
    }
]

# Therapy modules data
THERAPY_MODULES = [
    {
        'id': 'cbti_basics',
        'name': 'CBT-I मूल बातें',
        'description': 'नींद चिकित्सा की मूल बातें और CBT-I तकनीकों का परिचय',
        'duration': '30 मिनट',
        'difficulty': 'शुरुआती',
        'video_url': 'https://www.youtube.com/watch?v=GyxqKoQAxTk',
        'icon': '🧠'
    },
    {
        'id': 'sleep_restriction',
        'name': 'नींद प्रतिबंध तकनीक',
        'description': 'सोने के समय को नियंत्रित करने की तकनीक',
        'duration': '25 मिनट',
        'difficulty': 'मध्यम',
        'video_url': 'https://www.youtube.com/watch?v=DdtHsaZ_Xp4',
        'icon': '⏰'
    },
    {
        'id': 'sleep_hygiene',
        'name': 'नींद स्वच्छता',
        'description': 'अच्छी नींद के लिए आदतें और वातावरण',
        'duration': '20 मिनट',
        'difficulty': 'शुरुआती',
        'video_url': 'https://www.youtube.com/watch?v=s2dQPI9ZPO0',
        'icon': '🌙'
    },
    {
        'id': 'progressive_relaxation',
        'name': 'प्रगतिशील मांसपेशी रिलैक्सेशन',
        'description': 'शरीर को आराम देने की तकनीक',
        'duration': '35 मिनट',
        'difficulty': 'मध्यम',
        'video_url': 'https://www.youtube.com/watch?v=STPuP0kUnTo',
        'icon': '🧘‍♀️'
    },
    {
        'id': 'breathing_techniques',
        'name': 'गहरी सांस लेने की तकनीक',
        'description': 'तनाव कम करने के लिए सांस लेने के व्यायाम',
        'duration': '15 मिनट',
        'difficulty': 'शुरुआती',
        'video_url': 'https://www.youtube.com/watch?v=kQUae5zodJ8',
        'icon': '🫁'
    },
    {
        'id': 'bedroom_environment',
        'name': 'बेडरूम का वातावरण',
        'description': 'नींद के लिए आदर्श वातावरण बनाना',
        'duration': '20 मिनट',
        'difficulty': 'शुरुआती',
        'video_url': 'https://www.youtube.com/watch?v=dxsR_l5bu7w',
        'icon': '🏠'
    },
    {
        'id': 'sleep_routine',
        'name': 'दिनचर्या और नींद',
        'description': 'नियमित दिनचर्या का महत्व',
        'duration': '25 मिनट',
        'difficulty': 'शुरुआती',
        'video_url': 'https://www.youtube.com/watch?v=KVfDhbFRfy0',
        'icon': '📅'
    },
    {
        'id': 'cognitive_restructuring',
        'name': 'संज्ञानात्मक पुनर्गठन',
        'description': 'नींद के बारे में नकारात्मक विचारों को बदलना',
        'duration': '40 मिनट',
        'difficulty': 'उन्नत',
        'video_url': 'https://www.youtube.com/watch?v=SclJBsQYI_Q',
        'icon': '💭'
    },
    {
        'id': 'sleep_restriction_therapy',
        'name': 'नींद प्रतिबंध चिकित्सा',
        'description': 'नींद की दक्षता बढ़ाने की तकनीक',
        'duration': '30 मिनट',
        'difficulty': 'उन्नत',
        'video_url': 'https://www.youtube.com/watch?v=7okjM6Tq14E',
        'icon': '🎯'
    }
]

# Initialize session state
if 'diary_entries' not in st.session_state:
    st.session_state.diary_entries = []
if 'assessment_results' not in st.session_state:
    st.session_state.assessment_results = []
if 'bookings' not in st.session_state:
    st.session_state.bookings = []
if 'therapy_sessions' not in st.session_state:
    st.session_state.therapy_sessions = []
if 'therapy_reminders' not in st.session_state:
    st.session_state.therapy_reminders = []
if 'therapy_plan' not in st.session_state:
    st.session_state.therapy_plan = None
if 'completed_modules' not in st.session_state:
    st.session_state.completed_modules = []

# Sample data for demonstration
def get_sample_diary_data():
    """Generate sample sleep diary data"""
    dates = pd.date_range(start=datetime.now() - timedelta(days=7), end=datetime.now(), freq='D')
    data = []
    
    for date in dates:
        data.append({
            'date': date.strftime('%Y-%m-%d'),
            'bedtime': f"{np.random.randint(22, 24)}:{np.random.randint(0, 60):02d}",
            'wake_time': f"{np.random.randint(6, 8)}:{np.random.randint(0, 60):02d}",
            'sleep_latency': np.random.randint(5, 30),
            'wake_ups': np.random.randint(0, 4),
            'sleep_quality': np.random.randint(6, 10),
            'notes': 'अच्छी नींद' if np.random.random() > 0.3 else 'थोड़ी परेशानी'
        })
    
    return pd.DataFrame(data)

def calculate_sleep_metrics(df):
    """Calculate sleep metrics from diary data"""
    metrics = {}
    
    if len(df) > 0:
        # Sleep efficiency
        total_bed_time = 0
        total_sleep_time = 0
        
        for _, row in df.iterrows():
            bedtime = datetime.strptime(row['bedtime'], '%H:%M')
            wake_time = datetime.strptime(row['wake_time'], '%H:%M')
            
            if wake_time < bedtime:
                wake_time += timedelta(days=1)
            
            bed_duration = (wake_time - bedtime).total_seconds() / 3600
            sleep_duration = bed_duration - (row['sleep_latency'] / 60) - (row['wake_ups'] * 0.25)
            
            total_bed_time += bed_duration
            total_sleep_time += sleep_duration
        
        metrics['sleep_efficiency'] = (total_sleep_time / total_bed_time * 100) if total_bed_time > 0 else 0
        metrics['avg_sleep_duration'] = total_sleep_time / len(df)
        metrics['avg_sleep_latency'] = df['sleep_latency'].mean()
        metrics['avg_wake_ups'] = df['wake_ups'].mean()
        metrics['avg_sleep_quality'] = df['sleep_quality'].mean()
    
    return metrics

def get_isi_questions():
    """ISI (Insomnia Severity Index) questions"""
    return [
        {
            'id': 'isi_1',
            'question': 'पिछले 2 सप्ताह में आपको सोने में कितनी कठिनाई हुई है?',
            'options': [
                ('कोई कठिनाई नहीं', 0),
                ('थोड़ी कठिनाई', 1),
                ('कुछ कठिनाई', 2),
                ('काफी कठिनाई', 3),
                ('बहुत कठिनाई', 4)
            ]
        },
        {
            'id': 'isi_2',
            'question': 'पिछले 2 सप्ताह में आपको रात में जागने में कितनी कठिनाई हुई है?',
            'options': [
                ('कोई समस्या नहीं', 0),
                ('थोड़ी समस्या', 1),
                ('कुछ समस्या', 2),
                ('काफी समस्या', 3),
                ('बहुत समस्या', 4)
            ]
        },
        {
            'id': 'isi_3',
            'question': 'पिछले 2 सप्ताह में आपको जल्दी उठने में कितनी कठिनाई हुई है?',
            'options': [
                ('कोई कठिनाई नहीं', 0),
                ('थोड़ी कठिनाई', 1),
                ('कुछ कठिनाई', 2),
                ('काफी कठिनाई', 3),
                ('बहुत कठिनाई', 4)
            ]
        },
        {
            'id': 'isi_4',
            'question': 'पिछले 2 सप्ताह में आप अपनी नींद से कितने संतुष्ट हैं?',
            'options': [
                ('बहुत संतुष्ट', 0),
                ('काफी संतुष्ट', 1),
                ('कुछ संतुष्ट', 2),
                ('कुछ असंतुष्ट', 3),
                ('बहुत असंतुष्ट', 4)
            ]
        },
        {
            'id': 'isi_5',
            'question': 'पिछले 2 सप्ताह में आपकी नींद की समस्या दूसरों को कितनी दिखाई दी है?',
            'options': [
                ('बिल्कुल नहीं', 0),
                ('थोड़ा', 1),
                ('कुछ', 2),
                ('काफी', 3),
                ('बहुत', 4)
            ]
        },
        {
            'id': 'isi_6',
            'question': 'पिछले 2 सप्ताह में आपकी नींद की समस्या ने आपके जीवन की गुणवत्ता को कितना प्रभावित किया है?',
            'options': [
                ('बिल्कुल नहीं', 0),
                ('थोड़ा', 1),
                ('कुछ', 2),
                ('काफी', 3),
                ('बहुत', 4)
            ]
        },
        {
            'id': 'isi_7',
            'question': 'पिछले 2 सप्ताह में आपकी नींद की समस्या ने आपके मूड, काम या रिश्तों को कितना प्रभावित किया है?',
            'options': [
                ('बिल्कुल नहीं', 0),
                ('थोड़ा', 1),
                ('कुछ', 2),
                ('काफी', 3),
                ('बहुत', 4)
            ]
        }
    ]

def calculate_isi_score(answers):
    """Calculate ISI score and severity"""
    total_score = sum(answers.values())
    
    if total_score <= 7:
        severity = 'हल्का'
        color = 'success'
        recommendations = [
            'आपकी नींद की गुणवत्ता अच्छी है।',
            'नियमित दिनचर्या बनाए रखें।',
            'सोने से पहले रिलैक्सेशन तकनीकों का उपयोग करें।'
        ]
    elif total_score <= 14:
        severity = 'मध्यम'
        color = 'warning'
        recommendations = [
            'नींद की गुणवत्ता में सुधार की आवश्यकता है।',
            'CBT-I (Cognitive Behavioral Therapy for Insomnia) तकनीकों का उपयोग करें।',
            'सोने का समय निर्धारित करें और उसका पालन करें।',
            'बेडरूम को ठंडा, अंधेरा और शांत रखें।'
        ]
    else:
        severity = 'गंभीर'
        color = 'danger'
        recommendations = [
            'तुरंत चिकित्सकीय सलाह लें।',
            'नींद विशेषज्ञ से परामर्श करें।',
            'संभावित अंतर्निहित चिकित्सा स्थितियों की जांच कराएं।',
            'दवा के विकल्पों पर चर्चा करें।'
        ]
    
    return {
        'total_score': total_score,
        'max_score': 28,
        'severity': severity,
        'color': color,
        'recommendations': recommendations
    }

def recommend_doctors(assessment_result=None, language_preference="हिंदी", location_preference=None, max_doctors=3):
    """Recommend doctors based on assessment results, language, and location"""
    if not assessment_result:
        # If no assessment, still consider language and location preferences
        doctor_scores = []
        
        for doctor in DOCTORS:
            score = 0
            reasons = []
            
            # Base score from rating
            base_score = doctor['rating'] * 10
            score += base_score
            reasons.append(f"रेटिंग: {doctor['rating']} ({base_score:.0f} अंक)")
            
            # Language preference match
            if language_preference in doctor['languages']:
                score += 20
                reasons.append(f"भाषा मैच: {language_preference} (+20 अंक)")
            else:
                reasons.append(f"भाषा मैच नहीं: {language_preference} (0 अंक)")
            
            # Location preference match
            if location_preference and location_preference.lower() in doctor['location'].lower():
                score += 15
                reasons.append(f"स्थान मैच: {location_preference} (+15 अंक)")
            elif location_preference:
                reasons.append(f"स्थान मैच नहीं: {location_preference} (0 अंक)")
            
            # Experience bonus
            experience_years = int(doctor['experience'].split('+')[0])
            exp_bonus = experience_years * 2
            score += exp_bonus
            reasons.append(f"अनुभव बोनस: {experience_years} वर्ष (+{exp_bonus} अंक)")
            
            # Patient count bonus
            patient_bonus = min(doctor['patients_treated'] / 100, 20)
            score += patient_bonus
            reasons.append(f"मरीज अनुभव: {doctor['patients_treated']} मरीज (+{patient_bonus:.0f} अंक)")
            
            # Add reasons to doctor data
            doctor_with_reasons = doctor.copy()
            doctor_with_reasons['recommendation_score'] = score
            doctor_with_reasons['recommendation_reasons'] = reasons
            
            doctor_scores.append((doctor_with_reasons, score))
        
        # Sort by score and return top recommendations
        doctor_scores.sort(key=lambda x: x[1], reverse=True)
        return [doctor for doctor, score in doctor_scores[:max_doctors]]
    
    severity = assessment_result.get('severity', 'हल्का')
    total_score = assessment_result.get('total_score', 0)
    
    # Scoring system for doctor recommendations
    doctor_scores = []
    
    for doctor in DOCTORS:
        score = 0
        reasons = []
        
        # Base score from rating
        base_score = doctor['rating'] * 10
        score += base_score
        reasons.append(f"रेटिंग: {doctor['rating']} ({base_score:.0f} अंक)")
        
        # Language preference match
        if language_preference in doctor['languages']:
            score += 20
            reasons.append(f"भाषा मैच: {language_preference} (+20 अंक)")
        else:
            reasons.append(f"भाषा मैच नहीं: {language_preference} (0 अंक)")
        
        # Location preference match
        if location_preference and location_preference.lower() in doctor['location'].lower():
            score += 15
            reasons.append(f"स्थान मैच: {location_preference} (+15 अंक)")
        elif location_preference:
            reasons.append(f"स्थान मैच नहीं: {location_preference} (0 अंक)")
        
        # Severity-based specialty matching
        if severity in ['गंभीर']:
            # For severe cases, prefer experienced doctors with specific specialties
            if 'CBT-I' in doctor['specialties']:
                score += 25
                reasons.append("CBT-I विशेषज्ञता (+25 अंक)")
            if int(doctor['experience'].split('+')[0]) >= 10:
                score += 15
                reasons.append("10+ वर्ष अनुभव (+15 अंक)")
            if 'Neurological Sleep Disorders' in doctor['specialties']:
                score += 20
                reasons.append("न्यूरोलॉजिकल नींद विकार विशेषज्ञता (+20 अंक)")
        elif severity == 'मध्यम':
            # For moderate cases, prefer CBT-I specialists
            if 'CBT-I' in doctor['specialties']:
                score += 20
                reasons.append("CBT-I विशेषज्ञता (+20 अंक)")
            if 'Sleep Psychology' in doctor['specialties']:
                score += 15
                reasons.append("नींद मनोविज्ञान विशेषज्ञता (+15 अंक)")
        else:
            # For mild cases, prefer general sleep specialists
            if 'Sleep Hygiene' in doctor['specialties']:
                score += 15
                reasons.append("नींद स्वच्छता विशेषज्ञता (+15 अंक)")
            if 'Behavioral Sleep Therapy' in doctor['specialties']:
                score += 10
                reasons.append("व्यवहार नींद चिकित्सा (+10 अंक)")
        
        # Experience bonus
        experience_years = int(doctor['experience'].split('+')[0])
        exp_bonus = experience_years * 2
        score += exp_bonus
        reasons.append(f"अनुभव बोनस: {experience_years} वर्ष (+{exp_bonus} अंक)")
        
        # Patient count bonus (more patients = more experience)
        patient_bonus = min(doctor['patients_treated'] / 100, 20)
        score += patient_bonus
        reasons.append(f"मरीज अनुभव: {doctor['patients_treated']} मरीज (+{patient_bonus:.0f} अंक)")
        
        # Add reasons to doctor data
        doctor_with_reasons = doctor.copy()
        doctor_with_reasons['recommendation_score'] = score
        doctor_with_reasons['recommendation_reasons'] = reasons
        
        doctor_scores.append((doctor_with_reasons, score))
    
    # Sort by score and return top recommendations
    doctor_scores.sort(key=lambda x: x[1], reverse=True)
    return [doctor for doctor, score in doctor_scores[:max_doctors]]

def create_therapy_plan(assessment_result):
    """Create a personalized therapy plan based on assessment results"""
    severity = assessment_result.get('severity', 'हल्का')
    total_score = assessment_result.get('total_score', 0)
    
    # Define therapy plans based on severity
    if severity == 'हल्का':
        plan = {
            'name': 'बुनियादी नींद सुधार योजना',
            'description': 'हल्की नींद की समस्याओं के लिए बुनियादी तकनीकें',
            'duration_weeks': 4,
            'modules': [
                {'id': 'sleep_hygiene', 'week': 1, 'required': True, 'unlocked': True},
                {'id': 'bedroom_environment', 'week': 1, 'required': True, 'unlocked': False},
                {'id': 'sleep_routine', 'week': 2, 'required': True, 'unlocked': False},
                {'id': 'breathing_techniques', 'week': 2, 'required': False, 'unlocked': False},
                {'id': 'progressive_relaxation', 'week': 3, 'required': False, 'unlocked': False},
                {'id': 'cbti_basics', 'week': 4, 'required': False, 'unlocked': False}
            ]
        }
    elif severity == 'मध्यम':
        plan = {
            'name': 'मध्यम नींद चिकित्सा योजना',
            'description': 'मध्यम नींद की समस्याओं के लिए संरचित चिकित्सा',
            'duration_weeks': 6,
            'modules': [
                {'id': 'sleep_hygiene', 'week': 1, 'required': True, 'unlocked': True},
                {'id': 'bedroom_environment', 'week': 1, 'required': True, 'unlocked': False},
                {'id': 'sleep_routine', 'week': 2, 'required': True, 'unlocked': False},
                {'id': 'breathing_techniques', 'week': 2, 'required': True, 'unlocked': False},
                {'id': 'progressive_relaxation', 'week': 3, 'required': True, 'unlocked': False},
                {'id': 'cbti_basics', 'week': 4, 'required': True, 'unlocked': False},
                {'id': 'sleep_restriction', 'week': 5, 'required': True, 'unlocked': False},
                {'id': 'cognitive_restructuring', 'week': 6, 'required': False, 'unlocked': False}
            ]
        }
    else:  # गंभीर
        plan = {
            'name': 'गहन नींद चिकित्सा योजना',
            'description': 'गंभीर नींद की समस्याओं के लिए व्यापक चिकित्सा',
            'duration_weeks': 8,
            'modules': [
                {'id': 'sleep_hygiene', 'week': 1, 'required': True, 'unlocked': True},
                {'id': 'bedroom_environment', 'week': 1, 'required': True, 'unlocked': False},
                {'id': 'sleep_routine', 'week': 2, 'required': True, 'unlocked': False},
                {'id': 'breathing_techniques', 'week': 2, 'required': True, 'unlocked': False},
                {'id': 'progressive_relaxation', 'week': 3, 'required': True, 'unlocked': False},
                {'id': 'cbti_basics', 'week': 4, 'required': True, 'unlocked': False},
                {'id': 'sleep_restriction', 'week': 5, 'required': True, 'unlocked': False},
                {'id': 'cognitive_restructuring', 'week': 6, 'required': True, 'unlocked': False},
                {'id': 'sleep_restriction_therapy', 'week': 7, 'required': True, 'unlocked': False}
            ]
        }
    
    return plan

def update_module_unlock_status():
    """Update which modules are unlocked based on completed modules"""
    if not st.session_state.therapy_plan:
        return
    
    # Reset all modules to locked except the first one
    for module in st.session_state.therapy_plan['modules']:
        module['unlocked'] = False
    
    # Unlock the first module
    if st.session_state.therapy_plan['modules']:
        st.session_state.therapy_plan['modules'][0]['unlocked'] = True
    
    # Unlock modules based on completion
    completed_ids = [m['id'] for m in st.session_state.completed_modules]
    
    for i, module in enumerate(st.session_state.therapy_plan['modules']):
        if module['id'] in completed_ids:
            # Unlock the next module if this one is completed
            if i + 1 < len(st.session_state.therapy_plan['modules']):
                st.session_state.therapy_plan['modules'][i + 1]['unlocked'] = True

def check_and_show_reminders():
    """Check for active reminders and show them"""
    current_time = datetime.now()
    active_reminders = []
    
    for reminder in st.session_state.therapy_reminders:
        if reminder['status'] == 'pending':
            reminder_time = datetime.fromisoformat(reminder['reminder_datetime'])
            # Show reminder if it's time (within 5 minutes of reminder time)
            if abs((current_time - reminder_time).total_seconds()) <= 300:  # 5 minutes
                active_reminders.append(reminder)
    
    if active_reminders:
        for reminder in active_reminders:
            st.warning(f"🔔 **रिमाइंडर:** {reminder['message']}")
            col1, col2 = st.columns([1, 4])
            with col1:
                if st.button("✅ देख लिया", key=f"dismiss_{reminder['id']}"):
                    reminder['status'] = 'dismissed'
                    st.rerun()
            with col2:
                if st.button("📅 चिकित्सा पेज पर जाएं", key=f"goto_therapy_{reminder['id']}"):
                    st.session_state.current_page = "चिकित्सा"
                    st.rerun()

def main():
    # Check and show active reminders
    check_and_show_reminders()
    
    # Header - SleepMitra with golden crescent moon (clickable to dashboard)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🌙 SleepMitra", key="header_logo", use_container_width=True):
            st.session_state.current_page = "डैशबोर्ड"
            st.rerun()
    
    # Style the header button to look like the original design
    st.markdown("""
    <style>
    div[data-testid="column"]:nth-of-type(2) button {
        background: transparent !important;
        border: none !important;
        color: #6C5CE7 !important;
        font-size: 2.2rem !important;
        font-weight: bold !important;
        padding: 0.5rem 0 !important;
        margin: 0 !important;
        box-shadow: none !important;
        text-align: center !important;
    }
    div[data-testid="column"]:nth-of-type(2) button:hover {
        background: rgba(108, 92, 231, 0.1) !important;
        border-radius: 8px !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Initialize current page if not set
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "डैशबोर्ड"
    
    page = st.session_state.current_page
    
    # Navigation buttons with active state
    dashboard_active = page == "डैशबोर्ड"
    diary_active = page == "नींद डायरी"
    assessment_active = page == "नींद आकलन"
    booking_active = page == "अपॉइंटमेंट"
    analytics_active = page == "विश्लेषण"
    therapy_active = page == "चिकित्सा"
    chatbot_active = page == "चैटबॉट"
    
    if st.sidebar.button("🏠 डैशबोर्ड", use_container_width=True, type="primary" if dashboard_active else "secondary", key="nav_dashboard"):
        st.session_state.current_page = "डैशबोर्ड"
        st.rerun()
    
    if st.sidebar.button("📝 नींद डायरी", use_container_width=True, type="primary" if diary_active else "secondary", key="nav_diary"):
        st.session_state.current_page = "नींद डायरी"
        st.rerun()
    
    if st.sidebar.button("📋 नींद आकलन", use_container_width=True, type="primary" if assessment_active else "secondary", key="nav_assessment"):
        st.session_state.current_page = "नींद आकलन"
        st.rerun()
    
    if st.sidebar.button("📅 अपॉइंटमेंट", use_container_width=True, type="primary" if booking_active else "secondary", key="nav_booking"):
        st.session_state.current_page = "अपॉइंटमेंट"
        st.rerun()
    
    if st.sidebar.button("📊 विश्लेषण", use_container_width=True, type="primary" if analytics_active else "secondary", key="nav_analytics"):
        st.session_state.current_page = "विश्लेषण"
        st.rerun()
    
    if st.sidebar.button("🧠 चिकित्सा", use_container_width=True, type="primary" if therapy_active else "secondary", key="nav_therapy"):
        st.session_state.current_page = "चिकित्सा"
        st.rerun()
    
    if st.sidebar.button("🤖 चैटबॉट", use_container_width=True, type="primary" if chatbot_active else "secondary", key="nav_chatbot"):
        st.session_state.current_page = "चैटबॉट"
        st.rerun()
    
    if page == "डैशबोर्ड":
        show_dashboard()
    elif page == "नींद डायरी":
        show_sleep_diary()
    elif page == "नींद आकलन":
        show_assessment()
    elif page == "अपॉइंटमेंट":
        show_booking()
    elif page == "विश्लेषण":
        show_analytics()
    elif page == "चिकित्सा":
        show_therapy()
    elif page == "चैटबॉट":
        show_chatbot()

def show_dashboard():
    st.markdown("### 📊 डैशबोर्ड")
    
    # Get sample data
    diary_df = get_sample_diary_data()
    metrics = calculate_sleep_metrics(diary_df)
    
    # KPI Cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h3>नींद दक्षता</h3>
            <h1>{metrics['sleep_efficiency']:.1f}%</h1>
            <p>↗ +5.2% पिछले सप्ताह से</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <h3>सोने की देरी</h3>
            <h1>{metrics['avg_sleep_latency']:.0f} मिनट</h1>
            <p>↘ -8.5% पिछले सप्ताह से</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <h3>नींद अवधि</h3>
            <h1>{metrics['avg_sleep_duration']:.1f} घंटे</h1>
            <p>↗ +2.1% पिछले सप्ताह से</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <h3>जागने की संख्या</h3>
            <h1>{metrics['avg_wake_ups']:.1f}</h1>
            <p>↘ -15.3% पिछले सप्ताह से</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Quick Actions
    st.subheader("🚀 त्वरित कार्य")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📝 नींद डायरी", use_container_width=True, key="quick_diary"):
            st.session_state.current_page = "नींद डायरी"
            st.rerun()
    
    with col2:
        if st.button("📋 नींद आकलन", use_container_width=True, key="quick_assessment"):
            st.session_state.current_page = "नींद आकलन"
            st.rerun()
    
    with col3:
        if st.button("📅 अपॉइंटमेंट", use_container_width=True, key="quick_booking"):
            st.session_state.current_page = "अपॉइंटमेंट"
            st.rerun()

def show_sleep_diary():
    st.markdown("### 📝 नींद डायरी")
    
    # Add new entry form
    st.subheader("नई एंट्री जोड़ें")
    
    with st.form("diary_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            date = st.date_input("तारीख", value=datetime.now().date())
            bedtime = st.time_input("सोने का समय", value=datetime.strptime("23:00", "%H:%M").time())
            sleep_latency = st.number_input("सोने में लगा समय (मिनट)", min_value=0, max_value=120, value=15)
        
        with col2:
            wake_time = st.time_input("जागने का समय", value=datetime.strptime("07:00", "%H:%M").time())
            wake_ups = st.number_input("रात में जागने की संख्या", min_value=0, max_value=10, value=1)
            sleep_quality = st.slider("नींद की गुणवत्ता (1-10)", min_value=1, max_value=10, value=7)
        
        notes = st.text_area("टिप्पणी", placeholder="आज की नींद के बारे में कुछ नोट्स...")
        
        if st.form_submit_button("सेव करें", use_container_width=True):
            entry = {
                'date': date.strftime('%Y-%m-%d'),
                'bedtime': bedtime.strftime('%H:%M'),
                'wake_time': wake_time.strftime('%H:%M'),
                'sleep_latency': sleep_latency,
                'wake_ups': wake_ups,
                'sleep_quality': sleep_quality,
                'notes': notes
            }
            
            st.session_state.diary_entries.append(entry)
            st.success("नींद डायरी एंट्री सफलतापूर्वक सेव हो गई!")
    
    # Display entries
    if st.session_state.diary_entries:
        st.subheader("पिछली एंट्रीज")
        
        entries_df = pd.DataFrame(st.session_state.diary_entries)
        st.dataframe(entries_df, use_container_width=True)
        
        # Calculate and display metrics
        metrics = calculate_sleep_metrics(entries_df)
        
        st.subheader("आपके नींद के आंकड़े")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("औसत नींद अवधि", f"{metrics['avg_sleep_duration']:.1f} घंटे")
        
        with col2:
            st.metric("औसत नींद दक्षता", f"{metrics['sleep_efficiency']:.1f}%")
        
        with col3:
            st.metric("औसत नींद गुणवत्ता", f"{metrics['avg_sleep_quality']:.1f}/10")

def show_assessment():
    st.markdown("### 📋 नींद आकलन")
    st.markdown("अपनी नींद की गुणवत्ता का पूर्ण आकलन करें और व्यक्तिगत सुझाव प्राप्त करें।")
    
    # ISI Assessment
    st.subheader("इनसोम्निया सीविटी इंडेक्स (ISI)")
    
    isi_questions = get_isi_questions()
    answers = {}
    
    for i, question in enumerate(isi_questions):
        st.markdown(f"**{i+1}. {question['question']}**")
        
        selected_option = st.radio(
            "उत्तर चुनें:",
            [option[0] for option in question['options']],
            key=question['id'],
            horizontal=True
        )
        
        # Find the score for selected option
        for option_text, score in question['options']:
            if option_text == selected_option:
                answers[question['id']] = score
                break
    
    if st.button("आकलन पूर्ण करें", use_container_width=True, key="complete_assessment"):
        result = calculate_isi_score(answers)
        
        st.markdown("---")
        st.subheader("📊 आकलन परिणाम")
        
        # Score display
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.markdown(f"""
            <div style="text-align: center; padding: 2rem; background: #f8f9fa; border-radius: 10px;">
                <h1 style="color: #6C5CE7; font-size: 3rem; margin: 0;">{result['total_score']}</h1>
                <p style="margin: 0;">/ {result['max_score']}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            # Severity badge
            if result['color'] == 'success':
                st.markdown(f"""
                <div class="success-card">
                    <h3>गंभीरता: {result['severity']}</h3>
                </div>
                """, unsafe_allow_html=True)
            elif result['color'] == 'warning':
                st.markdown(f"""
                <div class="warning-card">
                    <h3>गंभीरता: {result['severity']}</h3>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="danger-card">
                    <h3>गंभीरता: {result['severity']}</h3>
                </div>
                """, unsafe_allow_html=True)
        
        # Recommendations
        st.subheader("💡 सुझाव")
        for recommendation in result['recommendations']:
            st.markdown(f"• {recommendation}")
        
        # Save result
        result['timestamp'] = datetime.now().isoformat()
        result['answers'] = answers
        st.session_state.assessment_results.append(result)

def show_booking():
    st.markdown("### 📅 अपॉइंटमेंट बुकिंग")
    st.markdown("नींद विशेषज्ञ के साथ अपॉइंटमेंट बुक करें। आपके आकलन परिणामों के आधार पर सर्वोत्तम डॉक्टरों की सिफारिश की जाती है।")
    
    # Get user preferences
    col1, col2 = st.columns(2)
    
    with col1:
        language_preference = st.selectbox("भाषा प्राथमिकता", ["हिंदी", "English", "पंजाबी", "मराठी", "गुजराती", "तेलुगु", "तमिल", "राजस्थानी"], key="language_pref")
    
    with col2:
        location_preference = st.selectbox("स्थान प्राथमिकता", ["कोई प्राथमिकता नहीं", "दिल्ली", "मुंबई", "अहमदाबाद", "बैंगलोर", "जयपुर", "सूरत"], key="location_pref")
        if location_preference == "कोई प्राथमिकता नहीं":
            location_preference = None
    
    # Get assessment result for recommendations
    last_assessment = None
    if st.session_state.assessment_results:
        last_assessment = st.session_state.assessment_results[-1]
    
    # Show assessment-based recommendations
    if last_assessment:
        st.info(f"📊 आपके आकलन परिणाम (ISI स्कोर: {last_assessment['total_score']}, गंभीरता: {last_assessment['severity']}) के आधार पर डॉक्टरों की सिफारिश की जा रही है।")
    
    # Get recommended doctors - this will recalculate when preferences change
    recommended_doctors = recommend_doctors(
        assessment_result=last_assessment,
        language_preference=language_preference,
        location_preference=location_preference,
        max_doctors=3
    )
    
    # Add refresh button to recalculate recommendations
    if st.button("🔄 सिफारिशें अपडेट करें", use_container_width=True, key="refresh_recommendations"):
        st.rerun()
    
    # Display recommended doctors
    st.subheader("🎯 आपके लिए अनुशंसित डॉक्टर")
    
    for i, doctor in enumerate(recommended_doctors):
        # Show recommendation score and reasons
        score = doctor.get('recommendation_score', 0)
        reasons = doctor.get('recommendation_reasons', [])
        
        with st.expander(f"{doctor['image']} {doctor['name']} - {doctor['specialty']} ⭐ {doctor['rating']}", expanded=(i==0)):
            col1, col2 = st.columns([1, 2])
            
            with col1:
                st.markdown(f"""
                <div style="text-align: center; padding: 1rem;">
                    <div style="font-size: 3rem; margin-bottom: 0.5rem;">{doctor['image']}</div>
                    <div style="font-size: 0.9rem; color: #666;">{doctor['location']}</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                **{doctor['name']}**  
                {doctor['specialty']}  
                {doctor['qualification']}  
                ⭐ {doctor['rating']} ({doctor['experience']})  
                💰 ₹{doctor['consultation_fee']}  
                👥 {doctor['patients_treated']} मरीजों का इलाज  
                
                **भाषाएं:** {', '.join(doctor['languages'])}  
                **क्लिनिक:** {doctor['clinic']}  
                **विशेषज्ञता:** {', '.join(doctor['specialties'])}  
                
                {doctor['bio']}
                """)
                
                # Show availability
                st.markdown("**उपलब्धता:**")
                availability_cols = st.columns(len(doctor['availability']))
                for j, day in enumerate(doctor['availability']):
                    with availability_cols[j]:
                        st.markdown(f"📅 {day}")
                
                # Booking button for this doctor
                if st.button(f"📅 {doctor['name']} के साथ अपॉइंटमेंट बुक करें", key=f"book_{doctor['id']}", use_container_width=True):
                    st.session_state.selected_doctor = doctor
                    st.rerun()
    
    # Show all doctors option
    if st.button("👥 सभी डॉक्टर देखें", use_container_width=True):
        st.session_state.show_all_doctors = True
        st.rerun()
    
    # Show all doctors if requested
    if st.session_state.get('show_all_doctors', False):
        st.subheader("👥 सभी उपलब्ध डॉक्टर")
        
        # Filter options
        filter_col1, filter_col2, filter_col3 = st.columns(3)
        
        with filter_col1:
            specialty_filter = st.selectbox("विशेषज्ञता", ["सभी", "CBT-I", "Sleep Apnea", "Sleep Psychology", "Neurological Sleep Disorders", "Behavioral Sleep Therapy"])
        
        with filter_col2:
            location_filter = st.selectbox("स्थान", ["सभी", "दिल्ली", "मुंबई", "अहमदाबाद", "बैंगलोर", "जयपुर", "सूरत"])
        
        with filter_col3:
            rating_filter = st.selectbox("न्यूनतम रेटिंग", ["सभी", "4.5+", "4.7+", "4.8+", "4.9+"])
        
        # Filter doctors
        filtered_doctors = DOCTORS.copy()
        
        if specialty_filter != "सभी":
            filtered_doctors = [d for d in filtered_doctors if specialty_filter in d['specialties']]
        
        if location_filter != "सभी":
            filtered_doctors = [d for d in filtered_doctors if location_filter in d['location']]
        
        if rating_filter != "सभी":
            min_rating = float(rating_filter.replace("+", ""))
            filtered_doctors = [d for d in filtered_doctors if d['rating'] >= min_rating]
        
        # Display filtered doctors
        for doctor in filtered_doctors:
            with st.expander(f"{doctor['image']} {doctor['name']} - {doctor['specialty']} ⭐ {doctor['rating']}"):
                col1, col2 = st.columns([1, 2])
                
                with col1:
                    st.markdown(f"""
                    <div style="text-align: center; padding: 1rem;">
                        <div style="font-size: 3rem; margin-bottom: 0.5rem;">{doctor['image']}</div>
                        <div style="font-size: 0.9rem; color: #666;">{doctor['location']}</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    st.markdown(f"""
                    **{doctor['name']}**  
                    {doctor['specialty']}  
                    {doctor['qualification']}  
                    ⭐ {doctor['rating']} ({doctor['experience']})  
                    💰 ₹{doctor['consultation_fee']}  
                    👥 {doctor['patients_treated']} मरीजों का इलाज  
                    
                    **भाषाएं:** {', '.join(doctor['languages'])}  
                    **क्लिनिक:** {doctor['clinic']}  
                    **विशेषज्ञता:** {', '.join(doctor['specialties'])}  
                    
                    {doctor['bio']}
                    """)
                    
                    if st.button(f"📅 {doctor['name']} के साथ अपॉइंटमेंट बुक करें", key=f"book_all_{doctor['id']}", use_container_width=True):
                        st.session_state.selected_doctor = doctor
                        st.rerun()
        
        if st.button("🔙 अनुशंसित डॉक्टर पर वापस जाएं", use_container_width=True):
            st.session_state.show_all_doctors = False
            st.rerun()
    
    # Booking form for selected doctor
    if st.session_state.get('selected_doctor'):
        doctor = st.session_state.selected_doctor
        st.subheader(f"📅 {doctor['name']} के साथ अपॉइंटमेंट बुक करें")
        
        with st.form("booking_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                appointment_date = st.date_input("तारीख चुनें", min_value=datetime.now().date())
                appointment_time = st.selectbox("समय चुनें", doctor['time_slots'])
            
            with col2:
                appointment_type = st.selectbox("अपॉइंटमेंट प्रकार", [
                    "टेलीकंसल्टेशन (वीडियो कॉल)",
                    "क्लिनिक विजिट (व्यक्तिगत)"
                ])
                
                patient_name = st.text_input("आपका नाम")
                patient_phone = st.text_input("फोन नंबर")
            
            reason = st.text_area("समस्या का विवरण", placeholder="अपनी नींद की समस्या के बारे में बताएं...")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.form_submit_button("अपॉइंटमेंट बुक करें", use_container_width=True):
                    booking = {
                        'doctor_id': doctor['id'],
                        'doctor_name': doctor['name'],
                        'doctor_specialty': doctor['specialty'],
                        'date': appointment_date.strftime('%Y-%m-%d'),
                        'time': appointment_time,
                        'type': appointment_type,
                        'patient_name': patient_name,
                        'patient_phone': patient_phone,
                        'reason': reason,
                        'consultation_fee': doctor['consultation_fee'],
                        'timestamp': datetime.now().isoformat()
                    }
                    
                    st.session_state.bookings.append(booking)
                    st.success(f"🎉 {doctor['name']} के साथ आपकी अपॉइंटमेंट सफलतापूर्वक बुक हो गई है!")
                    st.session_state.selected_doctor = None
                    st.rerun()
            
            with col2:
                if st.form_submit_button("रद्द करें", use_container_width=True):
                    st.session_state.selected_doctor = None
                    st.rerun()
    
    # Display bookings
    if st.session_state.bookings:
        st.subheader("📋 आपकी अपॉइंटमेंट्स")
        
        for booking in st.session_state.bookings:
            with st.container():
                st.markdown(f"""
                <div style="background: #f8f9fa; padding: 1rem; border-radius: 8px; margin-bottom: 1rem; border-left: 4px solid #6C5CE7;">
                    <h4 style="margin: 0 0 0.5rem 0; color: #333;">{booking['doctor_name']}</h4>
                    <p style="margin: 0 0 0.5rem 0; color: #666;">{booking['doctor_specialty']}</p>
                    <p style="margin: 0 0 0.5rem 0;"><strong>तारीख:</strong> {booking['date']} | <strong>समय:</strong> {booking['time']}</p>
                    <p style="margin: 0 0 0.5rem 0;"><strong>प्रकार:</strong> {booking['type']} | <strong>फीस:</strong> ₹{booking['consultation_fee']}</p>
                    <p style="margin: 0; color: #666;"><strong>समस्या:</strong> {booking['reason']}</p>
                </div>
                """, unsafe_allow_html=True)

def show_analytics():
    st.markdown("### 📊 नींद विश्लेषण")
    st.markdown("अपनी नींद के पैटर्न और रुझानों का विस्तृत विश्लेषण देखें।")
    
    # Get sample data for demonstration
    diary_df = get_sample_diary_data()
    
    # Sleep Duration Chart
    st.subheader("नींद की अवधि (घंटे)")
    
    # Calculate sleep duration for each day
    sleep_durations = []
    for _, row in diary_df.iterrows():
        bedtime = datetime.strptime(row['bedtime'], '%H:%M')
        wake_time = datetime.strptime(row['wake_time'], '%H:%M')
        
        if wake_time < bedtime:
            wake_time += timedelta(days=1)
        
        bed_duration = (wake_time - bedtime).total_seconds() / 3600
        sleep_duration = bed_duration - (row['sleep_latency'] / 60) - (row['wake_ups'] * 0.25)
        sleep_durations.append(sleep_duration)
    
    diary_df['sleep_duration'] = sleep_durations
    
    fig_duration = px.line(
        diary_df, 
        x='date', 
        y='sleep_duration',
        title='नींद की अवधि का रुझान',
        labels={'sleep_duration': 'नींद अवधि (घंटे)', 'date': 'तारीख'}
    )
    fig_duration.update_layout(font_family="Noto Sans Devanagari")
    st.plotly_chart(fig_duration, use_container_width=True)
    
    # Sleep Quality Chart
    st.subheader("नींद की गुणवत्ता")
    
    fig_quality = px.bar(
        diary_df, 
        x='date', 
        y='sleep_quality',
        title='नींद की गुणवत्ता का रुझान',
        labels={'sleep_quality': 'नींद गुणवत्ता (1-10)', 'date': 'तारीख'},
        color='sleep_quality',
        color_continuous_scale='RdYlGn'
    )
    fig_quality.update_layout(font_family="Noto Sans Devanagari")
    st.plotly_chart(fig_quality, use_container_width=True)
    
    # Wake-ups Chart
    st.subheader("रात में जागने की संख्या")
    
    fig_wakeups = px.bar(
        diary_df, 
        x='date', 
        y='wake_ups',
        title='रात में जागने की संख्या',
        labels={'wake_ups': 'जागने की संख्या', 'date': 'तारीख'},
        color='wake_ups',
        color_continuous_scale='Reds'
    )
    fig_wakeups.update_layout(font_family="Noto Sans Devanagari")
    st.plotly_chart(fig_wakeups, use_container_width=True)
    
    # Insights
    st.subheader("💡 अंतर्दृष्टि और सुझाव")
    
    avg_duration = diary_df['sleep_duration'].mean()
    avg_quality = diary_df['sleep_quality'].mean()
    avg_wakeups = diary_df['wake_ups'].mean()
    
    col1, col2 = st.columns(2)
    
    with col1:
        if avg_duration >= 7 and avg_quality >= 7:
            st.markdown("""
            <div class="success-card">
                <h4>सकारात्मक रुझान</h4>
                <p>पिछले सप्ताह में आपकी नींद की गुणवत्ता में सुधार हुआ है। औसत नींद की अवधि {:.1f} घंटे है।</p>
            </div>
            """.format(avg_duration), unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="warning-card">
                <h4>सुधार की आवश्यकता</h4>
                <p>नींद की गुणवत्ता में सुधार की आवश्यकता है। नियमित दिनचर्या बनाए रखें।</p>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        if avg_wakeups <= 2:
            st.markdown("""
            <div class="success-card">
                <h4>अच्छी नींद की निरंतरता</h4>
                <p>आपकी नींद में कम व्यवधान है। यह अच्छी नींद की गुणवत्ता का संकेत है।</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="warning-card">
                <h4>नींद में व्यवधान</h4>
                <p>रात में जागने की संख्या को कम करने के लिए नियमित दिनचर्या बनाए रखें।</p>
            </div>
            """, unsafe_allow_html=True)

def show_therapy():
    st.markdown("### 🧠 चिकित्सा सुझाव")
    st.markdown("आपके आकलन परिणामों के आधार पर व्यक्तिगत चिकित्सा सुझाव और उपचार वीडियो")
    
    # Get last assessment result
    last_assessment = None
    if st.session_state.assessment_results:
        last_assessment = st.session_state.assessment_results[-1]
    
    # Create or update therapy plan based on assessment
    if last_assessment and not st.session_state.therapy_plan:
        st.session_state.therapy_plan = create_therapy_plan(last_assessment)
        st.success(f"🎯 आपके लिए व्यक्तिगत चिकित्सा योजना बनाई गई है: **{st.session_state.therapy_plan['name']}**")
    
    # Update module unlock status
    if st.session_state.therapy_plan:
        update_module_unlock_status()
    
    # Display therapy plan
    if st.session_state.therapy_plan:
        st.subheader("🎯 आपकी व्यक्तिगत चिकित्सा योजना")
        
        plan = st.session_state.therapy_plan
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 1.5rem; border-radius: 12px; margin-bottom: 2rem;">
            <h3 style="margin: 0 0 0.5rem 0; color: white;">{plan['name']}</h3>
            <p style="margin: 0 0 1rem 0; opacity: 0.9;">{plan['description']}</p>
            <div style="display: flex; gap: 2rem; align-items: center;">
                <div><strong>अवधि:</strong> {plan['duration_weeks']} सप्ताह</div>
                <div><strong>मॉड्यूल:</strong> {len(plan['modules'])} मॉड्यूल</div>
                <div><strong>पूर्ण:</strong> {len(st.session_state.completed_modules)}/{len(plan['modules'])}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Show progress
        progress = len(st.session_state.completed_modules) / len(plan['modules'])
        st.progress(progress, text=f"प्रगति: {int(progress * 100)}%")
        
        # Display modules with lock/unlock status
        st.subheader("📚 चिकित्सा मॉड्यूल")
        
        for i, module_plan in enumerate(plan['modules']):
            # Find the actual module data
            module_data = next((m for m in THERAPY_MODULES if m['id'] == module_plan['id']), None)
            if not module_data:
                continue
            
            is_completed = module_plan['id'] in [m['id'] for m in st.session_state.completed_modules]
            is_unlocked = module_plan['unlocked']
            
            # Determine styling based on status
            if is_completed:
                border_color = "#28a745"
                bg_color = "#e8f5e8"
                status_icon = "✅"
                status_text = "पूर्ण"
            elif is_unlocked:
                border_color = "#6C5CE7"
                bg_color = "#f8f9fa"
                status_icon = "🔓"
                status_text = "उपलब्ध"
            else:
                border_color = "#6c757d"
                bg_color = "#f8f9fa"
                status_icon = "🔒"
                status_text = "लॉक"
            
            with st.container():
                col1, col2, col3 = st.columns([4, 1, 1])
                
                with col1:
                    st.markdown(f"""
                    <div style="background: {bg_color}; padding: 1rem; border-radius: 8px; margin-bottom: 1rem; border-left: 4px solid {border_color};">
                        <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.5rem;">
                            <span style="font-size: 1.2rem;">{module_data['icon']}</span>
                            <h4 style="margin: 0; color: #333;">{module_data['name']}</h4>
                            <span style="font-size: 0.8rem; color: #666;">{status_icon} {status_text}</span>
                        </div>
                        <p style="margin: 0 0 0.5rem 0; color: #666;">{module_data['description']}</p>
                        <div style="display: flex; gap: 1rem; font-size: 0.9rem; color: #666;">
                            <span>📅 सप्ताह {module_plan['week']}</span>
                            <span>⏱️ {module_data['duration']}</span>
                            <span>📊 {module_data['difficulty']}</span>
                            <span>{'✅ आवश्यक' if module_plan['required'] else '🔹 वैकल्पिक'}</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    if is_completed:
                        st.markdown("**✅ पूर्ण**")
                    elif is_unlocked:
                        if st.button("▶️ शुरू करें", key=f"start_module_{module_plan['id']}", use_container_width=True):
                            # Mark module as completed
                            completed_module = {
                                'id': module_plan['id'],
                                'name': module_data['name'],
                                'completed_at': datetime.now().isoformat(),
                                'week': module_plan['week']
                            }
                            st.session_state.completed_modules.append(completed_module)
                            st.success(f"✅ {module_data['name']} पूर्ण हो गया!")
                            st.rerun()
                    else:
                        st.markdown("**🔒 लॉक**")
                
                with col3:
                    if is_unlocked and not is_completed:
                        if st.button("📅 शेड्यूल", key=f"schedule_module_{module_plan['id']}", use_container_width=True):
                            # Pre-fill the scheduling form with this module
                            st.session_state.selected_module_for_scheduling = module_data
                            st.rerun()
    
    elif last_assessment:
        # Create therapy plan button
        if st.button("🎯 मेरी चिकित्सा योजना बनाएं", use_container_width=True):
            st.session_state.therapy_plan = create_therapy_plan(last_assessment)
            st.rerun()
    else:
        st.info("💡 चिकित्सा योजना बनाने के लिए पहले नींद आकलन पूर्ण करें।")
    
    st.markdown("---")
    
    # Therapy scheduling section
    st.subheader("📅 चिकित्सा सत्र शेड्यूल करें")
    
    with st.expander("🕐 नया चिकित्सा सत्र शेड्यूल करें", expanded=False):
        with st.form("therapy_scheduling_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                session_date = st.date_input("तारीख चुनें", min_value=datetime.now().date(), key="therapy_date")
                session_time = st.time_input("समय चुनें", value=datetime.now().time(), key="therapy_time")
            
            with col2:
                # Therapy module selection - only show unlocked modules from therapy plan
                if st.session_state.therapy_plan:
                    # Get unlocked modules from therapy plan
                    unlocked_modules = []
                    for module_plan in st.session_state.therapy_plan['modules']:
                        if module_plan['unlocked']:
                            module_data = next((m for m in THERAPY_MODULES if m['id'] == module_plan['id']), None)
                            if module_data:
                                unlocked_modules.append(module_data)
                    
                    if unlocked_modules:
                        module_options = {f"{module['icon']} {module['name']} ({module['duration']})": module for module in unlocked_modules}
                        # Pre-select if a module was selected from the therapy plan
                        default_index = 0
                        if hasattr(st.session_state, 'selected_module_for_scheduling'):
                            selected_module_name = f"{st.session_state.selected_module_for_scheduling['icon']} {st.session_state.selected_module_for_scheduling['name']} ({st.session_state.selected_module_for_scheduling['duration']})"
                            if selected_module_name in module_options:
                                default_index = list(module_options.keys()).index(selected_module_name)
                            # Clear the selected module after using it
                            delattr(st.session_state, 'selected_module_for_scheduling')
                        
                        selected_module_name = st.selectbox("चिकित्सा मॉड्यूल चुनें (केवल उपलब्ध)", list(module_options.keys()), index=default_index, key="therapy_module")
                        selected_module = module_options[selected_module_name]
                    else:
                        st.warning("कोई मॉड्यूल उपलब्ध नहीं है। पहले पिछले मॉड्यूल पूर्ण करें।")
                        selected_module = None
                else:
                    # Fallback to all modules if no therapy plan
                    module_options = {f"{module['icon']} {module['name']} ({module['duration']})": module for module in THERAPY_MODULES}
                    selected_module_name = st.selectbox("चिकित्सा मॉड्यूल चुनें", list(module_options.keys()), key="therapy_module")
                    selected_module = module_options[selected_module_name]
                
                # Reminder options
                reminder_options = ["15 मिनट पहले", "30 मिनट पहले", "1 घंटा पहले", "2 घंटे पहले", "1 दिन पहले"]
                reminder_time = st.selectbox("रिमाइंडर समय", reminder_options, key="reminder_time")
            
            session_notes = st.text_area("नोट्स (वैकल्पिक)", placeholder="इस सत्र के लिए कोई विशेष नोट्स...", key="session_notes")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.form_submit_button("📅 सत्र शेड्यूल करें", use_container_width=True):
                    if selected_module is None:
                        st.error("कृपया एक चिकित्सा मॉड्यूल चुनें।")
                    else:
                        # Create therapy session
                        session_datetime = datetime.combine(session_date, session_time)
                        
                        therapy_session = {
                            'id': f"session_{len(st.session_state.therapy_sessions) + 1}",
                            'date': session_date.strftime('%Y-%m-%d'),
                            'time': session_time.strftime('%H:%M'),
                            'datetime': session_datetime.isoformat(),
                            'module': selected_module,
                            'reminder_time': reminder_time,
                            'notes': session_notes,
                            'status': 'scheduled',  # scheduled, completed, missed
                            'created_at': datetime.now().isoformat()
                        }
                        
                        st.session_state.therapy_sessions.append(therapy_session)
                        
                        # Create reminder
                        reminder_datetime = session_datetime
                        if "15 मिनट" in reminder_time:
                            reminder_datetime = session_datetime - timedelta(minutes=15)
                        elif "30 मिनट" in reminder_time:
                            reminder_datetime = session_datetime - timedelta(minutes=30)
                        elif "1 घंटा" in reminder_time:
                            reminder_datetime = session_datetime - timedelta(hours=1)
                        elif "2 घंटे" in reminder_time:
                            reminder_datetime = session_datetime - timedelta(hours=2)
                        elif "1 दिन" in reminder_time:
                            reminder_datetime = session_datetime - timedelta(days=1)
                        
                        reminder = {
                            'id': f"reminder_{len(st.session_state.therapy_reminders) + 1}",
                            'session_id': therapy_session['id'],
                            'reminder_datetime': reminder_datetime.isoformat(),
                            'message': f"🔔 आपका चिकित्सा सत्र {selected_module['name']} {session_date.strftime('%d/%m/%Y')} को {session_time.strftime('%H:%M')} बजे शुरू होने वाला है।",
                            'status': 'pending'  # pending, sent, dismissed
                        }
                        
                        st.session_state.therapy_reminders.append(reminder)
                        
                        st.success(f"🎉 आपका चिकित्सा सत्र {selected_module['name']} {session_date.strftime('%d/%m/%Y')} को {session_time.strftime('%H:%M')} बजे शेड्यूल हो गया है!")
                        st.rerun()
            
            with col2:
                if st.form_submit_button("❌ रद्द करें", use_container_width=True):
                    st.rerun()
    
    # Display scheduled therapy sessions
    if st.session_state.therapy_sessions:
        st.subheader("📋 आपके शेड्यूल किए गए चिकित्सा सत्र")
        
        # Filter sessions by status
        scheduled_sessions = [s for s in st.session_state.therapy_sessions if s['status'] == 'scheduled']
        completed_sessions = [s for s in st.session_state.therapy_sessions if s['status'] == 'completed']
        
        if scheduled_sessions:
            st.markdown("**🕐 आगामी सत्र:**")
            for session in sorted(scheduled_sessions, key=lambda x: x['datetime']):
                session_datetime = datetime.fromisoformat(session['datetime'])
                module = session['module']
                
                with st.container():
                    col1, col2, col3 = st.columns([3, 1, 1])
                    
                    with col1:
                        st.markdown(f"""
                        <div style="background: #f8f9fa; padding: 1rem; border-radius: 8px; margin-bottom: 1rem; border-left: 4px solid #6C5CE7;">
                            <h4 style="margin: 0 0 0.5rem 0; color: #333;">{module['icon']} {module['name']}</h4>
                            <p style="margin: 0 0 0.5rem 0; color: #666;">{module['description']}</p>
                            <p style="margin: 0 0 0.5rem 0;"><strong>तारीख:</strong> {session['date']} | <strong>समय:</strong> {session['time']}</p>
                            <p style="margin: 0 0 0.5rem 0;"><strong>अवधि:</strong> {module['duration']} | <strong>कठिनाई:</strong> {module['difficulty']}</p>
                            {f'<p style="margin: 0; color: #666;"><strong>नोट्स:</strong> {session["notes"]}</p>' if session['notes'] else ''}
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col2:
                        if st.button("▶️ शुरू करें", key=f"start_{session['id']}", use_container_width=True):
                            # Mark session as completed
                            session['status'] = 'completed'
                            session['completed_at'] = datetime.now().isoformat()
                            st.success("✅ सत्र पूर्ण हो गया!")
                            st.rerun()
                    
                    with col3:
                        if st.button("❌ रद्द करें", key=f"cancel_{session['id']}", use_container_width=True):
                            # Mark session as missed
                            session['status'] = 'missed'
                            session['cancelled_at'] = datetime.now().isoformat()
                            st.warning("❌ सत्र रद्द हो गया!")
                            st.rerun()
        
        if completed_sessions:
            st.markdown("**✅ पूर्ण सत्र:**")
            for session in sorted(completed_sessions, key=lambda x: x.get('completed_at', ''), reverse=True)[:3]:
                module = session['module']
                st.markdown(f"""
                <div style="background: #e8f5e8; padding: 0.8rem; border-radius: 6px; margin-bottom: 0.5rem; border-left: 4px solid #28a745;">
                    <strong>{module['icon']} {module['name']}</strong> - {session['date']} {session['time']} ✅
                </div>
                """, unsafe_allow_html=True)
    
    # Show upcoming reminders
    upcoming_reminders = [r for r in st.session_state.therapy_reminders if r['status'] == 'pending']
    if upcoming_reminders:
        st.subheader("🔔 आगामी रिमाइंडर")
        for reminder in sorted(upcoming_reminders, key=lambda x: x['reminder_datetime'])[:3]:
            reminder_datetime = datetime.fromisoformat(reminder['reminder_datetime'])
            st.info(f"📅 {reminder_datetime.strftime('%d/%m/%Y %H:%M')}: {reminder['message']}")
    
    st.markdown("---")
    
    # Get last assessment result
    last_assessment = None
    if st.session_state.assessment_results:
        last_assessment = st.session_state.assessment_results[-1]
    
    # Assessment Results Summary
    st.subheader("📊 आपके आकलन परिणाम")
    
    if last_assessment:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"""
            <div style="background: #f8f9fa; padding: 1.5rem; border-radius: 12px; border-left: 4px solid #6C5CE7;">
                <h4 style="color: #333; margin-bottom: 1rem;">ISI स्कोर: {last_assessment['total_score']}</h4>
                <h4 style="color: #333; margin-bottom: 1rem;">गंभीरता: {last_assessment['severity']}</h4>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div style="background: #f8f9fa; padding: 1.5rem; border-radius: 12px;">
                <h4 style="color: #333; margin-bottom: 1rem;">सुझाव:</h4>
                <p style="color: #666; line-height: 1.6;">{' '.join(last_assessment['recommendations'])}</p>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("पहले नींद आकलन पूर्ण करें ताकि व्यक्तिगत चिकित्सा सुझाव प्राप्त कर सकें।")
    
    # Therapy Modules
    st.subheader("🎯 अनुशंसित चिकित्सा मॉड्यूल")
    
    # CBT-I Module
    with st.expander("🧠 CBT-I (संज्ञानात्मक व्यवहार चिकित्सा) - अत्यधिक अनुशंसित", expanded=True):
        st.markdown("CBT-I नींद की समस्याओं के लिए सबसे प्रभावी उपचार है। यह दवा के बिना नींद की गुणवत्ता में सुधार करता है।")
        
        st.markdown("**शैक्षिक वीडियो:**")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📹 CBT-I का परिचय", use_container_width=True, key="video_cbti_intro"):
                st.markdown("[CBT-I का परिचय - नींद चिकित्सा की मूल बातें](https://www.youtube.com/watch?v=GyxqKoQAxTk)")
        
        with col2:
            if st.button("📹 नींद प्रतिबंध तकनीक", use_container_width=True, key="video_sleep_restriction"):
                st.markdown("[नींद प्रतिबंध तकनीक - सोने के समय को नियंत्रित करना](https://www.youtube.com/watch?v=DdtHsaZ_Xp4)")
        
        with col3:
            if st.button("📹 नींद स्वच्छता", use_container_width=True, key="video_sleep_hygiene"):
                st.markdown("[नींद स्वच्छता - अच्छी नींद के लिए आदतें](https://www.youtube.com/watch?v=s2dQPI9ZPO0)")
    
    # Relaxation Techniques
    with st.expander("🧘‍♀️ रिलैक्सेशन तकनीकें - अनुशंसित"):
        st.markdown("तनाव कम करने और नींद में सुधार के लिए विभिन्न रिलैक्सेशन तकनीकें सीखें।")
        
        st.markdown("**रिलैक्सेशन वीडियो:**")
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📹 प्रगतिशील मांसपेशी रिलैक्सेशन", use_container_width=True, key="video_pmr"):
                st.markdown("[प्रगतिशील मांसपेशी रिलैक्सेशन - शरीर को आराम देने की तकनीक](https://www.youtube.com/watch?v=STPuP0kUnTo)")
        
        with col2:
            if st.button("📹 गहरी सांस लेने की तकनीक", use_container_width=True, key="video_breathing"):
                st.markdown("[गहरी सांस लेने की तकनीक - तनाव कम करने के लिए सांस लेने के व्यायाम](https://www.youtube.com/watch?v=kQUae5zodJ8)")
    
    # Sleep Hygiene
    with st.expander("🌙 नींद स्वच्छता - सभी के लिए"):
        st.markdown("अच्छी नींद के लिए आवश्यक आदतें और वातावरण बनाने के तरीके।")
        
        st.markdown("**नींद स्वच्छता वीडियो:**")
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📹 बेडरूम का वातावरण", use_container_width=True, key="video_bedroom"):
                st.markdown("[बेडरूम का वातावरण - नींद के लिए आदर्श वातावरण बनाना](https://www.youtube.com/watch?v=dxsR_l5bu7w)")
        
        with col2:
            if st.button("📹 दिनचर्या और नींद", use_container_width=True, key="video_routine"):
                st.markdown("[दिनचर्या और नींद - नियमित दिनचर्या का महत्व](https://www.youtube.com/watch?v=KVfDhbFRfy0)")
    
    # Advanced Techniques
    with st.expander("🎯 उन्नत तकनीकें - अनुभवी उपयोगकर्ता"):
        st.markdown("गंभीर नींद की समस्याओं के लिए उन्नत चिकित्सा तकनीकें।")
        
        st.markdown("**उन्नत तकनीक वीडियो:**")
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📹 संज्ञानात्मक पुनर्गठन", use_container_width=True, key="video_cognitive"):
                st.markdown("[संज्ञानात्मक पुनर्गठन - नींद के बारे में नकारात्मक विचारों को बदलना](https://www.youtube.com/watch?v=SclJBsQYI_Q)")
        
        with col2:
            if st.button("📹 नींद प्रतिबंध चिकित्सा", use_container_width=True, key="video_restriction_therapy"):
                st.markdown("[नींद प्रतिबंध चिकित्सा - नींद की दक्षता बढ़ाने की तकनीक](https://www.youtube.com/watch?v=7okjM6Tq14E)")
    
    # Therapy Schedule
    st.subheader("📅 चिकित्सा कार्यक्रम")
    
    tab1, tab2, tab3 = st.tabs(["सप्ताह 1: नींद स्वच्छता", "सप्ताह 2: रिलैक्सेशन तकनीकें", "सप्ताह 3-4: CBT-I तकनीकें"])
    
    with tab1:
        st.markdown("""
        **सप्ताह 1: नींद स्वच्छता**
        - ✅ नियमित सोने का समय निर्धारित करें
        - ✅ बेडरूम को ठंडा और अंधेरा रखें
        - ⏳ सोने से 1 घंटे पहले स्क्रीन से दूर रहें
        - ⏳ कैफीन का सेवन कम करें
        """)
    
    with tab2:
        st.markdown("""
        **सप्ताह 2: रिलैक्सेशन तकनीकें**
        - ⏳ प्रगतिशील मांसपेशी रिलैक्सेशन सीखें
        - ⏳ गहरी सांस लेने की तकनीक अभ्यास करें
        - ⏳ मेडिटेशन शुरू करें
        - ⏳ सोने से पहले रिलैक्सेशन रूटीन बनाएं
        """)
    
    with tab3:
        st.markdown("""
        **सप्ताह 3-4: CBT-I तकनीकें**
        - ⏳ नींद प्रतिबंध तकनीक सीखें
        - ⏳ संज्ञानात्मक पुनर्गठन अभ्यास करें
        - ⏳ नींद डायरी रखना जारी रखें
        - ⏳ प्रगति का मूल्यांकन करें
        """)
    
    # Download Therapy Plan
    st.subheader("📥 चिकित्सा योजना डाउनलोड करें")
    
    if st.button("📄 व्यक्तिगत चिकित्सा योजना डाउनलोड करें", use_container_width=True, key="download_therapy_plan"):
        if last_assessment:
            therapy_plan = f"""नींद साथी - व्यक्तिगत चिकित्सा योजना

आकलन परिणाम:
- ISI स्कोर: {last_assessment['total_score']}
- गंभीरता: {last_assessment['severity']}

अनुशंसित चिकित्सा:
{chr(10).join([f"• {rec}" for rec in last_assessment['recommendations']])}

चिकित्सा कार्यक्रम:
सप्ताह 1: नींद स्वच्छता
• नियमित सोने का समय निर्धारित करें
• बेडरूम को ठंडा और अंधेरा रखें
• सोने से 1 घंटे पहले स्क्रीन से दूर रहें
• कैफीन का सेवन कम करें

सप्ताह 2: रिलैक्सेशन तकनीकें
• प्रगतिशील मांसपेशी रिलैक्सेशन सीखें
• गहरी सांस लेने की तकनीक अभ्यास करें
• मेडिटेशन शुरू करें
• सोने से पहले रिलैक्सेशन रूटीन बनाएं

सप्ताह 3-4: CBT-I तकनीकें
• नींद प्रतिबंध तकनीक सीखें
• संज्ञानात्मक पुनर्गठन अभ्यास करें
• नींद डायरी रखना जारी रखें
• प्रगति का मूल्यांकन करें

वीडियो लिंक्स:
1. CBT-I का परिचय: https://www.youtube.com/watch?v=GyxqKoQAxTk
2. नींद प्रतिबंध तकनीक: https://www.youtube.com/watch?v=DdtHsaZ_Xp4
3. नींद स्वच्छता: https://www.youtube.com/watch?v=s2dQPI9ZPO0
4. प्रगतिशील मांसपेशी रिलैक्सेशन: https://www.youtube.com/watch?v=STPuP0kUnTo
5. गहरी सांस लेने की तकनीक: https://www.youtube.com/watch?v=kQUae5zodJ8
6. बेडरूम का वातावरण: https://www.youtube.com/watch?v=dxsR_l5bu7w
7. दिनचर्या और नींद: https://www.youtube.com/watch?v=KVfDhbFRfy0
8. संज्ञानात्मक पुनर्गठन: https://www.youtube.com/watch?v=SclJBsQYI_Q
9. नींद प्रतिबंध चिकित्सा: https://www.youtube.com/watch?v=7okjM6Tq14E

तैयार किया गया: {datetime.now().strftime('%d/%m/%Y')}
SleepMitra - Hindi Insomnia Management System"""
        else:
            therapy_plan = f"""नींद साथी - सामान्य चिकित्सा योजना

सामान्य नींद स्वच्छता सुझाव:
• नियमित सोने का समय निर्धारित करें
• बेडरूम को ठंडा, अंधेरा और शांत रखें
• सोने से 1 घंटे पहले स्क्रीन से दूर रहें
• कैफीन और शराब से बचें
• रिलैक्सेशन तकनीकों का उपयोग करें
• नियमित व्यायाम करें

वीडियो लिंक्स:
1. CBT-I का परिचय: https://www.youtube.com/watch?v=GyxqKoQAxTk
2. नींद प्रतिबंध तकनीक: https://www.youtube.com/watch?v=DdtHsaZ_Xp4
3. नींद स्वच्छता: https://www.youtube.com/watch?v=s2dQPI9ZPO0
4. प्रगतिशील मांसपेशी रिलैक्सेशन: https://www.youtube.com/watch?v=STPuP0kUnTo
5. गहरी सांस लेने की तकनीक: https://www.youtube.com/watch?v=kQUae5zodJ8
6. बेडरूम का वातावरण: https://www.youtube.com/watch?v=dxsR_l5bu7w
7. दिनचर्या और नींद: https://www.youtube.com/watch?v=KVfDhbFRfy0
8. संज्ञानात्मक पुनर्गठन: https://www.youtube.com/watch?v=SclJBsQYI_Q
9. नींद प्रतिबंध चिकित्सा: https://www.youtube.com/watch?v=7okjM6Tq14E

तैयार किया गया: {datetime.now().strftime('%d/%m/%Y')}
SleepMitra - Hindi Insomnia Management System"""
        
        st.download_button(
            label="📥 चिकित्सा योजना डाउनलोड करें",
            data=therapy_plan,
            file_name=f"sleepmitra-therapy-plan-{datetime.now().strftime('%Y-%m-%d')}.txt",
            mime="text/plain"
        )

def show_chatbot():
    st.markdown("### 🤖 नींद सहायक चैटबॉट")
    st.markdown("नींद से जुड़े आपके सवालों के जवाब पाएं।")
    
    # Initialize chat history in session state
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = [
            {"role": "bot", "content": "नमस्ते! मैं आपकी नींद से जुड़ी समस्याओं में मदद कर सकता हूं। आप क्या जानना चाहते हैं?"}
        ]
    
    # Knowledge base for the chatbot
    chatbot_knowledge = {
        'नींद की गुणवत्ता कैसे सुधारें?': {
            'answer': 'नींद की गुणवत्ता सुधारने के लिए ये उपाय अपनाएं:\n\n• नियमित सोने का समय निर्धारित करें\n• सोने से 1 घंटे पहले स्क्रीन से दूर रहें\n• बेडरूम को ठंडा, अंधेरा और शांत रखें\n• कैफीन और शराब से बचें\n• रिलैक्सेशन तकनीकों का उपयोग करें\n• नियमित व्यायाम करें लेकिन सोने से 3-4 घंटे पहले नहीं',
            'suggestions': ['CBT-I क्या है?', 'अनिद्रा के लक्षण क्या हैं?', 'डॉक्टर से कब मिलना चाहिए?']
        },
        'CBT-I क्या है?': {
            'answer': 'CBT-I (Cognitive Behavioral Therapy for Insomnia) नींद की समस्याओं के लिए एक प्रभावी उपचार है:\n\n• सोने के समय को नियंत्रित करना\n• बेडरूम को सिर्फ सोने के लिए उपयोग करना\n• नकारात्मक विचारों को बदलना\n• रिलैक्सेशन तकनीकें सीखना\n• नींद की स्वच्छता के नियमों का पालन करना\n\nयह दवा के बिना नींद की समस्याओं को ठीक करने का सबसे प्रभावी तरीका है।',
            'suggestions': ['नींद की गुणवत्ता कैसे सुधारें?', 'अनिद्रा के लक्षण क्या हैं?']
        },
        'अनिद्रा के लक्षण क्या हैं?': {
            'answer': 'अनिद्रा के मुख्य लक्षण हैं:\n\n• सोने में कठिनाई\n• रात में बार-बार जागना\n• जल्दी उठ जाना और फिर न सो पाना\n• दिन में थकान और नींद आना\n• एकाग्रता में कमी\n• मूड में बदलाव\n• चिंता और तनाव\n\nयदि ये लक्षण 3 सप्ताह से अधिक समय तक रहें तो डॉक्टर से सलाह लें।',
            'suggestions': ['डॉक्टर से कब मिलना चाहिए?', 'CBT-I क्या है?']
        },
        'डॉक्टर से कब मिलना चाहिए?': {
            'answer': 'नींद विशेषज्ञ से मिलने के लिए ये स्थितियां हैं:\n\n• 3 सप्ताह से अधिक समय तक नींद की समस्या\n• दिन में काम पर प्रभाव पड़ना\n• चिंता या अवसाद के लक्षण\n• नींद की गोलियों पर निर्भरता\n• सांस लेने में तकलीफ या खर्राटे\n• पैरों में बेचैनी\n\nहमारे पास डॉ. प्रिया शर्मा जैसे अनुभवी विशेषज्ञ हैं जो आपकी मदद कर सकते हैं।',
            'suggestions': ['अपॉइंटमेंट कैसे बुक करें?', 'CBT-I क्या है?']
        },
        'अपॉइंटमेंट कैसे बुक करें?': {
            'answer': 'अपॉइंटमेंट बुक करने के लिए:\n\n1. "अपॉइंटमेंट" पेज पर जाएं\n2. उपलब्ध समय स्लॉट चुनें\n3. टेलीकंसल्टेशन या क्लिनिक विजिट चुनें\n4. अपनी जानकारी भरें\n5. बुकिंग की पुष्टि करें\n\nहमारे पास सुबह 9 बजे से शाम 4 बजे तक स्लॉट उपलब्ध हैं।',
            'suggestions': ['डॉक्टर से कब मिलना चाहिए?', 'टेलीकंसल्टेशन क्या है?']
        },
        'टेलीकंसल्टेशन क्या है?': {
            'answer': 'टेलीकंसल्टेशन एक वीडियो कॉल के माध्यम से डॉक्टर से मिलने का तरीका है:\n\n• घर बैठे डॉक्टर से सलाह\n• समय और पैसे की बचत\n• सुरक्षित और सुविधाजनक\n• उतनी ही प्रभावी जितनी व्यक्तिगत मुलाकात\n• सभी जरूरी जांच और सलाह मिलती है\n\nआप अपने मोबाइल या कंप्यूटर से आसानी से जुड़ सकते हैं।',
            'suggestions': ['अपॉइंटमेंट कैसे बुक करें?', 'डॉक्टर से कब मिलना चाहिए?']
        }
    }
    
    def get_bot_response(message):
        """Get bot response based on user message"""
        lower_message = message.lower()
        
        # Check for exact matches first
        if message in chatbot_knowledge:
            return chatbot_knowledge[message]
        
        # Check for keyword matches
        if 'नींद' in lower_message and ('सुधार' in lower_message or 'बेहतर' in lower_message):
            return chatbot_knowledge['नींद की गुणवत्ता कैसे सुधारें?']
        
        if 'cbt' in lower_message or 'थेरेपी' in lower_message:
            return chatbot_knowledge['CBT-I क्या है?']
        
        if 'लक्षण' in lower_message or 'समस्या' in lower_message:
            return chatbot_knowledge['अनिद्रा के लक्षण क्या हैं?']
        
        if 'डॉक्टर' in lower_message or 'विशेषज्ञ' in lower_message:
            return chatbot_knowledge['डॉक्टर से कब मिलना चाहिए?']
        
        if 'अपॉइंटमेंट' in lower_message or 'बुक' in lower_message:
            return chatbot_knowledge['अपॉइंटमेंट कैसे बुक करें?']
        
        if 'टेली' in lower_message or 'वीडियो' in lower_message:
            return chatbot_knowledge['टेलीकंसल्टेशन क्या है?']
        
        # Default response
        return {
            'answer': 'मुझे खेद है, मैं आपके सवाल को पूरी तरह समझ नहीं पाया। कृपया नीचे दिए गए विकल्पों में से कोई चुनें या अपना सवाल दोबारा पूछें।',
            'suggestions': ['नींद की गुणवत्ता कैसे सुधारें?', 'CBT-I क्या है?', 'अनिद्रा के लक्षण क्या हैं?', 'डॉक्टर से कब मिलना चाहिए?']
        }
    
    # Display chat history
    chat_container = st.container()
    
    with chat_container:
        for message in st.session_state.chat_history:
            if message["role"] == "bot":
                with st.chat_message("assistant"):
                    st.markdown(message["content"])
            else:
                with st.chat_message("user"):
                    st.markdown(message["content"])
    
    # Quick question buttons
    st.subheader("🚀 त्वरित प्रश्न")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("नींद की गुणवत्ता कैसे सुधारें?", use_container_width=True, key="chat_quality"):
            response = get_bot_response("नींद की गुणवत्ता कैसे सुधारें?")
            st.session_state.chat_history.append({"role": "user", "content": "नींद की गुणवत्ता कैसे सुधारें?"})
            st.session_state.chat_history.append({"role": "bot", "content": response['answer']})
            st.rerun()
        
        if st.button("CBT-I क्या है?", use_container_width=True, key="chat_cbti"):
            response = get_bot_response("CBT-I क्या है?")
            st.session_state.chat_history.append({"role": "user", "content": "CBT-I क्या है?"})
            st.session_state.chat_history.append({"role": "bot", "content": response['answer']})
            st.rerun()
    
    with col2:
        if st.button("अनिद्रा के लक्षण क्या हैं?", use_container_width=True, key="chat_symptoms"):
            response = get_bot_response("अनिद्रा के लक्षण क्या हैं?")
            st.session_state.chat_history.append({"role": "user", "content": "अनिद्रा के लक्षण क्या हैं?"})
            st.session_state.chat_history.append({"role": "bot", "content": response['answer']})
            st.rerun()
        
        if st.button("डॉक्टर से कब मिलना चाहिए?", use_container_width=True, key="chat_doctor"):
            response = get_bot_response("डॉक्टर से कब मिलना चाहिए?")
            st.session_state.chat_history.append({"role": "user", "content": "डॉक्टर से कब मिलना चाहिए?"})
            st.session_state.chat_history.append({"role": "bot", "content": response['answer']})
            st.rerun()
    
    # Chat input
    st.subheader("💬 अपना सवाल पूछें")
    
    with st.form("chat_form"):
        user_input = st.text_area("आपका सवाल:", placeholder="नींद से जुड़ा कोई भी सवाल पूछें...", height=100)
        submitted = st.form_submit_button("भेजें", use_container_width=True)
        
        if submitted and user_input:
            # Add user message to history
            st.session_state.chat_history.append({"role": "user", "content": user_input})
            
            # Get bot response
            response = get_bot_response(user_input)
            
            # Add bot response to history
            st.session_state.chat_history.append({"role": "bot", "content": response['answer']})
            
            st.rerun()
    
    # Clear chat button
    if st.button("🗑️ चैट हिस्ट्री साफ करें", use_container_width=True, key="clear_chat"):
        st.session_state.chat_history = [
            {"role": "bot", "content": "नमस्ते! मैं आपकी नींद से जुड़ी समस्याओं में मदद कर सकता हूं। आप क्या जानना चाहते हैं?"}
        ]
        st.rerun()
    
    # Contact options section
    st.markdown("---")
    st.subheader("📞 हमसे संपर्क करें")
    st.markdown("अधिक सहायता के लिए हमसे सीधे संपर्क करें:")
    
    # Contact buttons in a row
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📞 कॉल करें", use_container_width=True, key="call_button"):
            st.markdown("""
            <div style="text-align: center; padding: 1rem; background: #e8f5e8; border-radius: 10px; margin: 1rem 0;">
                <h4>📞 कॉल सेंटर</h4>
                <p><strong>फोन:</strong> +91-9876543210</p>
                <p><strong>समय:</strong> सुबह 9 बजे - शाम 6 बजे</p>
                <p><strong>भाषा:</strong> हिंदी, अंग्रेजी</p>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        if st.button("💬 टेक्स्ट मैसेज", use_container_width=True, key="text_button"):
            st.markdown("""
            <div style="text-align: center; padding: 1rem; background: #e3f2fd; border-radius: 10px; margin: 1rem 0;">
                <h4>💬 SMS सहायता</h4>
                <p><strong>नंबर:</strong> +91-9876543210</p>
                <p><strong>फॉर्मेट:</strong> "SLEEP [आपका सवाल]"</p>
                <p><strong>उदाहरण:</strong> SLEEP नींद नहीं आ रही</p>
            </div>
            """, unsafe_allow_html=True)
    
    with col3:
        if st.button("📱 WhatsApp", use_container_width=True, key="whatsapp_button"):
            st.markdown("""
            <div style="text-align: center; padding: 1rem; background: #e8f5e8; border-radius: 10px; margin: 1rem 0;">
                <h4>📱 WhatsApp सहायता</h4>
                <p><strong>नंबर:</strong> +91-9876543210</p>
                <p><strong>समय:</strong> 24/7 उपलब्ध</p>
                <p><strong>भाषा:</strong> हिंदी, अंग्रेजी</p>
            </div>
            """, unsafe_allow_html=True)
    
    # AI Voice Assistant section
    st.markdown("---")
    st.subheader("🤖 AI वॉइस असिस्टेंट")
    st.markdown("अपनी आवाज से सवाल पूछें और तुरंत जवाब पाएं:")
    
    # Voice input section
    col1, col2 = st.columns([2, 1])
    
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
        # AI Voice Assistant Form - Always visible
        st.markdown("**🎤 AI वॉइस असिस्टेंट**")
        
        # Voice Interface using Streamlit components
        st.markdown("### 🎤 वॉइस असिस्टेंट")
        
        # Voice Input Section
        st.markdown("**🎤 वॉइस इनपुट:**")
        
        # Simple Voice Mode Interface
        st.markdown("### 🎤 सरल वॉइस मोड")
        
        # Initialize voice mode state
        if 'voice_mode' not in st.session_state:
            st.session_state.voice_mode = False
        
        # Single voice mode toggle button
        if st.session_state.voice_mode:
            if st.button("🔴 वॉइस मोड बंद करें", use_container_width=True, key="voice_toggle"):
                st.session_state.voice_mode = False
                st.rerun()
        else:
            if st.button("🎤 वॉइस मोड चालू करें", use_container_width=True, key="voice_toggle"):
                st.session_state.voice_mode = True
                st.rerun()
        
        # Voice mode interface
        if st.session_state.voice_mode:
            st.success("🎤 वॉइस मोड चालू है! अब आप बोल सकते हैं और AI आपसे बात करेगा")
            
            # Initialize conversation history
            if 'conversation_history' not in st.session_state:
                st.session_state.conversation_history = []
            
            # Voice input area
            voice_input = st.text_area(
                "🎤 अपना सवाल बोलें या लिखें:",
                placeholder="यहाँ अपना सवाल लिखें या बोलें...",
                height=100,
                key="voice_input"
            )
            
            # Voice conversation buttons
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("🎤 वॉइस रिकॉर्डिंग शुरू करें", use_container_width=True, key="start_voice"):
                    st.info("🎤 वॉइस रिकॉर्डिंग शुरू! ब्राउज़र की अनुमति दें...")
                    
                    # Create a simple HTML file with voice recording
                    st.markdown("""
                    <div style="background: #d4edda; padding: 1.5rem; border-radius: 10px; margin: 1rem 0; border-left: 4px solid #28a745;">
                        <h5>🎤 वॉइस रिकॉर्डिंग चालू है</h5>
                        <p>नीचे दिए गए बटन पर क्लिक करें और ब्राउज़र की अनुमति दें:</p>
                        
                        <button onclick="startRecording()" style="background: #28a745; color: white; border: none; padding: 12px 24px; border-radius: 25px; margin: 10px 0; cursor: pointer; font-size: 16px;">
                            🎤 माइक्रोफोन अनुमति दें
                        </button>
                        
                        <div id="status" style="background: white; padding: 1rem; border-radius: 8px; margin: 1rem 0; border: 2px solid #28a745;">
                            <p style="margin: 0; font-weight: bold; color: #155724;">क्लिक करें और बोलें</p>
                        </div>
                        
                        <div id="transcript" style="background: #f8f9fa; padding: 1rem; border-radius: 8px; margin: 1rem 0; min-height: 60px; border: 1px solid #dee2e6;">
                            <p style="margin: 0; color: #6c757d;">आपकी आवाज यहाँ दिखेगी...</p>
                        </div>
                    </div>
                    
                    <script>
                    let recognition;
                    
                    function startRecording() {
                        if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
                            const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
                            recognition = new SpeechRecognition();
                            
                            recognition.continuous = true;
                            recognition.interimResults = true;
                            recognition.lang = 'hi-IN';
                            
                            recognition.onstart = function() {
                                document.getElementById('status').innerHTML = '<p style="margin: 0; font-weight: bold; color: #155724;">🎤 सुन रहा हूं... बोलें</p>';
                            };
                            
                            recognition.onresult = function(event) {
                                let transcript = '';
                                for (let i = event.resultIndex; i < event.results.length; i++) {
                                    transcript += event.results[i][0].transcript;
                                }
                                
                                if (transcript.trim()) {
                                    document.getElementById('transcript').innerHTML = '<p style="margin: 0; color: #155724; font-weight: bold;">' + transcript + '</p>';
                                    
                                    // Update the Streamlit text area
                                    const textArea = document.querySelector('textarea[data-testid="stTextArea"]');
                                    if (textArea) {
                                        textArea.value = transcript;
                                        textArea.dispatchEvent(new Event('input', { bubbles: true }));
                                    }
                                }
                            };
                            
                            recognition.onerror = function(event) {
                                document.getElementById('status').innerHTML = '<p style="margin: 0; font-weight: bold; color: #dc3545;">❌ त्रुटि: ' + event.error + '</p>';
                            };
                            
                            recognition.onend = function() {
                                document.getElementById('status').innerHTML = '<p style="margin: 0; font-weight: bold; color: #6c757d;">⏸️ रिकॉर्डिंग बंद</p>';
                            };
                            
                            // Start recognition
                            recognition.start();
                        } else {
                            document.getElementById('status').innerHTML = '<p style="margin: 0; font-weight: bold; color: #dc3545;">❌ आपका ब्राउज़र वॉइस रिकॉर्डिंग सपोर्ट नहीं करता</p>';
                        }
                    }
                    </script>
                    """, unsafe_allow_html=True)
            
            with col2:
                if st.button("🔴 रिकॉर्डिंग बंद करें", use_container_width=True, key="stop_voice"):
                    st.info("🔴 वॉइस रिकॉर्डिंग बंद हो गई")
                    st.markdown("""
                    <script>
                    if (typeof recognition !== 'undefined' && recognition) {
                        recognition.stop();
                    }
                    </script>
                    """, unsafe_allow_html=True)
            
            with col3:
                if st.button("🤖 AI से पूछें", use_container_width=True, key="ask_ai_voice"):
                    if voice_input.strip():
                        with st.spinner("🤖 AI जवाब दे रहा है..."):
                            ai_response = get_ai_response(voice_input)
                            
                            # Add to conversation history
                            st.session_state.conversation_history.append({
                                'user': voice_input,
                                'ai': ai_response,
                                'timestamp': datetime.now().strftime("%H:%M")
                            })
                            
                            # Display conversation
                            st.markdown("### 💬 बातचीत")
                            for msg in st.session_state.conversation_history[-5:]:  # Show last 5 messages
                                st.markdown(f"""
                                <div style="background: #e3f2fd; padding: 1rem; border-radius: 10px; margin: 0.5rem 0; border-left: 4px solid #2196f3;">
                                    <strong>आप ({msg['timestamp']}):</strong> {msg['user']}
                                </div>
                                """, unsafe_allow_html=True)
                                
                                st.markdown(f"""
                                <div style="background: #e8f5e8; padding: 1rem; border-radius: 10px; margin: 0.5rem 0; border-left: 4px solid #28a745;">
                                    <strong>AI ({msg['timestamp']}):</strong> {msg['ai']}
                                </div>
                                """, unsafe_allow_html=True)
                            
                            # Voice output instructions
                            st.markdown("""
                            <div style="background: #f0f8ff; padding: 1rem; border-radius: 10px; margin: 1rem 0; border-left: 4px solid #007bff;">
                                <h5>🔊 AI का जवाब सुनने के लिए:</h5>
                                <p><strong>Chrome/Edge:</strong> ऊपर दिए गए जवाब को सेलेक्ट करें → राइट-क्लिक → "Read aloud" चुनें</p>
                                <p><strong>Mac:</strong> जवाब को सेलेक्ट करें → Cmd + Option + S</p>
                                <p><strong>Windows:</strong> जवाब को सेलेक्ट करें → Ctrl + Shift + S</p>
                            </div>
                            """, unsafe_allow_html=True)
                    else:
                        st.warning("कृपया पहले अपना सवाल लिखें या बोलें")
            
            # Clear conversation button
            if st.button("🗑️ बातचीत साफ करें", use_container_width=True, key="clear_conversation"):
                st.session_state.conversation_history = []
                st.success("बातचीत साफ हो गई!")
                st.rerun()
        else:
            st.markdown("""
            <div style="background: #f8f9fa; padding: 1.5rem; border-radius: 10px; margin: 1rem 0; border-left: 4px solid #6c757d;">
                <h4 style="color: #6c757d; margin: 0 0 1rem 0;">🔴 वॉइस मोड बंद है</h4>
                <p style="color: #6c757d; margin: 0;">वॉइस मोड चालू करने के लिए ऊपर दिए गए बटन को दबाएं</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Fallback text input
        with st.form("ai_voice_form"):
            voice_text = st.text_area(
                "📝 या टेक्स्ट में लिखें:",
                placeholder="उदाहरण: मुझे नींद नहीं आ रही, क्या करूं?",
                height=80,
                key="voice_text_input"
            )
            
            if st.form_submit_button("🤖 AI से पूछें (टेक्स्ट)", use_container_width=True):
                if voice_text.strip():
                    with st.spinner("🤖 AI आपके सवाल का जवाब दे रहा है..."):
                        ai_response = get_ai_response(voice_text)
                        
                        # Display AI response
                        st.markdown(f"""
                        <div style="background: #e8f5e8; padding: 1.5rem; border-radius: 10px; margin: 1rem 0; border-left: 4px solid #28a745;">
                            <h4 style="color: #28a745; margin: 0 0 1rem 0;">🤖 AI असिस्टेंट का जवाब:</h4>
                            <div style="font-size: 1.1rem; line-height: 1.6; color: #333;">
                                {ai_response}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.warning("कृपया अपना सवाल लिखें।")
        
        # Quick question buttons
        st.markdown("**⚡ त्वरित सवाल:**")
        col_q1, col_q2 = st.columns(2)
        
        with col_q1:
            if st.button("😴 नींद नहीं आ रही", use_container_width=True, key="quick_q1"):
                with st.spinner("🤖 AI जवाब दे रहा है..."):
                    ai_response = get_ai_response("मुझे नींद नहीं आ रही, क्या करूं?")
                    st.markdown(f"""
                    <div style="background: #e8f5e8; padding: 1rem; border-radius: 10px; margin: 0.5rem 0; border-left: 4px solid #28a745;">
                        <h5 style="color: #28a745; margin: 0 0 0.5rem 0;">🤖 AI का जवाब:</h5>
                        <div style="font-size: 0.9rem; line-height: 1.5; color: #333;">
                            {ai_response}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
        
        with col_q2:
            if st.button("🧠 CBT-I क्या है?", use_container_width=True, key="quick_q2"):
                with st.spinner("🤖 AI जवाब दे रहा है..."):
                    ai_response = get_ai_response("CBT-I थेरेपी क्या है?")
                    st.markdown(f"""
                    <div style="background: #e8f5e8; padding: 1rem; border-radius: 10px; margin: 0.5rem 0; border-left: 4px solid #28a745;">
                        <h5 style="color: #28a745; margin: 0 0 0.5rem 0;">🤖 AI का जवाब:</h5>
                        <div style="font-size: 0.9rem; line-height: 1.5; color: #333;">
                            {ai_response}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
    
    # AI Integration Info
    st.markdown("---")
    st.subheader("🔧 AI इंटीग्रेशन")
    
    with st.expander("AI वॉइस असिस्टेंट कैसे काम करता है?", expanded=False):
        st.markdown("""
        ### 🤖 AI वॉइस असिस्टेंट की कार्यप्रणाली:
        
        **1. वॉइस रिकॉर्डिंग:**
        - ब्राउज़र की Web Speech API का उपयोग
        - रियल-टाइम वॉइस टू टेक्स्ट कन्वर्जन
        - हिंदी भाषा का समर्थन
        
        **2. AI प्रोसेसिंग:**
        - OpenAI GPT-4 API इंटीग्रेशन
        - हिंदी में प्राकृतिक भाषा प्रसंस्करण
        - नींद चिकित्सा विशेषज्ञता
        
        **3. रिस्पॉन्स जेनरेशन:**
        - तुरंत हिंदी में जवाब
        - व्यक्तिगत सुझाव
        - चिकित्सा सलाह
        
        **4. वॉइस आउटपुट:**
        - टेक्स्ट टू स्पीच कन्वर्जन
        - हिंदी उच्चारण
        - प्राकृतिक आवाज
        """)
    
    # Implementation status
    st.success("""
    ✅ **AI वॉइस असिस्टेंट सक्रिय है!**
    
    **उपलब्ध सुविधाएं:**
    1. ✅ **OpenAI GPT-4** इंटीग्रेशन
    2. ✅ **हिंदी भाषा** समर्थन
    3. ✅ **नींद चिकित्सा** विशेषज्ञता
    4. ✅ **व्यक्तिगत सुझाव** और सलाह
    
    **कैसे उपयोग करें:**
    - अपना सवाल टाइप करें या बोलें
    - AI तुरंत हिंदी में जवाब देगा
    - नींद की समस्याओं के लिए विशेषज्ञ सलाह
    """)

if __name__ == "__main__":
    main()

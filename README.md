# 🌙 SleepMitra - Hindi Insomnia Management System

A comprehensive Hindi-first insomnia management web application built with Streamlit, featuring personalized therapy plans, doctor recommendations, sleep tracking, and intelligent chatbot assistance.

## ✨ Features

### 🏠 Dashboard
- Sleep quality overview with key metrics
- Quick access to all features
- Personalized recommendations

### 📝 Sleep Diary
- Daily sleep pattern tracking
- Sleep quality assessment
- Mood and energy level monitoring
- Visual sleep trend analysis

### 🧠 Sleep Assessment
- ISI (Insomnia Severity Index) questionnaire
- Personalized severity assessment
- Detailed recommendations based on results
- Progress tracking over time

### 👨‍⚕️ Doctor Appointments
- Smart doctor recommendations based on:
  - Assessment results
  - Language preferences
  - Location preferences
  - Specialty matching
- Multiple doctor profiles with detailed information
- Easy appointment booking system

### 🧠 Therapy Module
- **Progressive Therapy Plans**: Personalized plans based on assessment severity
- **Module Locking System**: Modules unlock sequentially as you complete them
- **Video-Based Learning**: Curated YouTube videos for different therapy techniques
- **Session Scheduling**: Schedule therapy sessions with reminders
- **Progress Tracking**: Monitor your therapy journey

### 📊 Analytics
- Sleep pattern visualization
- Trend analysis with interactive charts
- Progress tracking over time
- Export capabilities

### 🤖 Intelligent Chatbot
- Hindi language support
- Sleep-related Q&A
- Quick access from any page
- Contextual help and guidance

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/nitinaggarwal-12/sleepmitra.git
   cd sleepmitra
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   streamlit run streamlit_app.py --server.port 8501
   ```

4. **Open your browser**
   Navigate to `http://localhost:8501`

## 📋 Requirements

```
streamlit>=1.25.0
pandas>=2.0.0
numpy>=1.21.0
plotly>=5.0.0
requests>=2.25.0
```

## 🎯 Key Features Explained

### Progressive Therapy System
- **Assessment-Based Plans**: Therapy plans are created based on your ISI assessment results
- **Sequential Unlocking**: Complete modules in order to unlock advanced techniques
- **Personalized Content**: Different plans for mild, moderate, and severe insomnia
- **Video Integration**: Direct links to educational YouTube videos

### Smart Doctor Recommendations
- **Multi-Factor Scoring**: Considers rating, language, location, specialty, and experience
- **Dynamic Updates**: Recommendations change based on your preferences
- **Comprehensive Profiles**: Detailed doctor information including specialties and availability

### Sleep Tracking & Analytics
- **Comprehensive Diary**: Track sleep patterns, mood, and energy levels
- **Visual Analytics**: Interactive charts showing sleep trends
- **Progress Monitoring**: Track improvement over time

## 🏗️ Architecture

### Frontend
- **Streamlit**: Modern web app framework
- **Custom CSS**: Professional styling and responsive design
- **Interactive Components**: Charts, forms, and dynamic content

### Backend
- **Python**: Core application logic
- **Session State**: Persistent data management
- **Local Storage**: Client-side data persistence

### Data Management
- **Session State**: Temporary data during app usage
- **Local Storage**: Persistent user data
- **No Database Required**: Lightweight, self-contained application

## 📱 Usage Guide

### Getting Started
1. **Complete Assessment**: Take the ISI questionnaire to get your personalized plan
2. **Explore Dashboard**: Review your sleep metrics and recommendations
3. **Start Therapy**: Begin with the first unlocked module in your therapy plan
4. **Track Progress**: Use the sleep diary to monitor your improvement
5. **Get Help**: Use the chatbot for questions and guidance

### Therapy Module Workflow
1. **Assessment**: Complete ISI questionnaire
2. **Plan Creation**: System creates personalized therapy plan
3. **Module Unlocking**: Start with first module, unlock others sequentially
4. **Session Scheduling**: Schedule therapy sessions with reminders
5. **Progress Tracking**: Monitor completion and improvement

## 🔧 Customization

### Adding New Therapy Modules
Edit the `THERAPY_MODULES` list in `streamlit_app.py` to add new modules.

### Modifying Doctor Profiles
Update the `DOCTORS` list in `streamlit_app.py` with new doctor information.

### Styling Changes
Modify the CSS in the `st.markdown()` sections to customize the appearance.

## 📄 License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📞 Support

For support and questions, please open an issue in the GitHub repository.

## 🙏 Acknowledgments

- Sleep therapy techniques based on CBT-I (Cognitive Behavioral Therapy for Insomnia)
- ISI questionnaire based on established sleep research
- YouTube video content from verified sleep therapy sources

---

**SleepMitra** - Your companion for better sleep and improved well-being. 🌙✨
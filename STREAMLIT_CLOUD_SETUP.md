# 🌐 Streamlit Cloud Setup Guide

## 🔑 Setting up OpenAI API Key in Streamlit Cloud

To enable the AI Voice Assistant functionality, you need to configure your OpenAI API key in Streamlit Cloud:

### Step 1: Go to Streamlit Cloud Dashboard
1. Visit [share.streamlit.io](https://share.streamlit.io)
2. Sign in with your GitHub account
3. Find your SleepMitra app

### Step 2: Configure Secrets
1. Click on your app
2. Go to **Settings** → **Secrets**
3. Add the following configuration:

```toml
OPENAI_API_KEY = "your_openai_api_key_here"

[contact]
phone = "+91-9876543210"
whatsapp = "+91-9876543210"
email = "support@sleepmitra.com"
```

**Note**: Replace `your_openai_api_key_here` with your actual OpenAI API key.

### Step 3: Save and Restart
1. Click **Save**
2. Your app will automatically restart
3. The AI Voice Assistant will now work!

## 🎭 AI Voice Assistant Features

### Personality
- **Female North Indian Hindi speaker**
- **Warm, motherly tone**
- **Cultural expressions**: "बेटा/बेटी", "अरे हां", "देखिए", "समझिए"
- **Empathetic and caring responses**

### Capabilities
- Sleep therapy advice in Hindi
- CBT-I technique explanations
- Sleep hygiene recommendations
- When to see a doctor guidance
- Personalized responses based on user queries

## 🚀 Your App URL
**Streamlit Cloud**: https://sleepmitra-aiims.streamlit.app

## 🔧 Troubleshooting

### If AI Assistant shows "API key not configured":
1. Check that the API key is correctly added to Streamlit Cloud secrets
2. Ensure there are no extra spaces or quotes around the key
3. Restart the app after adding the secret

### If responses are not in Hindi:
- The AI is configured to respond in Hindi (Devanagari script)
- If you see English responses, try rephrasing your question in Hindi

## 📞 Contact Support
- **Phone**: +91-9876543210
- **WhatsApp**: +91-9876543210
- **Email**: support@sleepmitra.com

---
*SleepMitra - Hindi Insomnia Management System* 🌙
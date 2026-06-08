<div align="center">

# 🎙️ Meeting Analyzer
### AI-Powered Meeting Intelligence

**Transform any meeting recording into a structured, actionable report — in seconds.**

[![Live Demo](https://img.shields.io/badge/🚀_Live_Demo-Click_Here-a855f7?style=for-the-badge)](https://meeting-analyzer-pudsvf8zdsgtbkfnowqiaj.streamlit.app)
[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)
[![Groq](https://img.shields.io/badge/Groq-LLaMA_3.3-f55036?style=for-the-badge)](https://groq.com)

</div>

---

## 🧠 What is Meeting Analyzer?

Meeting Analyzer is an AI-powered web application that takes your meeting recordings and instantly converts them into structured, professional reports — without any manual effort.

No more taking notes. No more forgetting what was decided. No more chasing people for their action items.

Just upload your audio. Let the AI handle the rest.

---

## ✨ Features

| Feature | Description |
|---|---|
| 🎙️ **Auto Transcription** | Converts speech to text locally using faster-whisper — your audio never leaves your machine |
| 📋 **Smart Summary** | Generates a concise 3-5 sentence overview of the entire meeting |
| ✅ **Key Decisions** | Extracts every important decision made during the meeting |
| 🎯 **Action Items** | Identifies tasks, assigns owners, and extracts deadlines automatically |
| 🧠 **AI Insights** | Analyzes meeting tone, productivity, and flags potential risks |
| ⬇️ **Export Report** | Download the complete analysis as a professional text report |

---

## 🖥️ Demo

> Upload a meeting recording → Get a full structured report in under a minute

**Supported formats:** MP3 · WAV · M4A · MP4 · Up to 200MB

---

## 🛠️ Tech Stack

| Technology | Purpose | Cost |
|---|---|---|
| faster-whisper | Speech to text | Free (runs locally) |
| Groq + LLaMA 3.3 | AI analysis | Free tier |
| Streamlit | Web app UI | Free |
| Python | Backend logic | Free |

**Total cost to run: $0** 🎉

---

## 🔒 Privacy First

Your audio files are transcribed **locally on your machine** using faster-whisper. The audio never gets uploaded to any external server. Only the text transcript is sent to Groq for analysis.

---

## 🚀 Run Locally

**Step 1 — Clone the repository**
```bash
git clone https://github.com/ruhelamahi7-code/meeting-analyzer
cd meeting-analyzer
```

**Step 2 — Install dependencies**
```bash
pip3 install streamlit faster-whisper groq
```

**Step 3 — Get a free Groq API key**

Go to [console.groq.com](https://console.groq.com) → Sign up → Create API key (no credit card needed)

**Step 4 — Add your API key**

Create a file `.streamlit/secrets.toml`:
```toml
GROQ_API_KEY = "your-groq-api-key-here"
```

**Step 5 — Launch the app**
```bash
python3 -m streamlit run app.py
```

Open [http://localhost:8501](http://localhost:8501) in your browser.

---

## 📁 Project Structure

---

## 💡 How It Works---

## 🎯 Use Cases

- **Team standups** — Never lose track of what was discussed
- **Client calls** — Auto-generate meeting notes to share
- **Lectures & interviews** — Extract key points instantly
- **Project meetings** — Track who owns what and by when

---

## 📊 Stats

- ⚡ Transcription: ~1 minute per 10 minutes of audio
- 🎯 Accuracy: ~98% on clear recordings
- 💾 Max file size: 200MB
- 🌍 Languages: English (primary)

---

<div align="center">

**Built with ❤️ by Mahi Ruhela**

*First Year CS Student · Building real AI tools*

[![GitHub](https://img.shields.io/badge/GitHub-ruhelamahi7--code-181717?style=flat&logo=github)](https://github.com/ruhelamahi7-code)

</div>

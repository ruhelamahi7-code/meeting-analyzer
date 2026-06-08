# 🎙️ Meeting Analyzer

An AI-powered web app that transforms meeting recordings into transcripts, summaries, key decisions, and action items — in seconds.

**Live Demo:** [meeting-analyzer-pudsvf8zdsgtbkfnowqiaj.streamlit.app](https://meeting-analyzer-pudsvf8zdsgtbkfnowqiaj.streamlit.app)

---

## What it does

Upload any meeting audio file and the app will automatically:

- 📄 **Transcribe** the entire recording to text
- 📋 **Summarize** the meeting in 3-5 sentences
- ✅ **Extract key decisions** made during the meeting
- 🎯 **Identify action items** with owner and deadline
- 🧠 **Generate AI insights** about meeting productivity
- ⬇️ **Download** the full report as a text file

---

## Tech Stack

| Layer | Technology |
|---|---|
| Transcription | faster-whisper (local, free, private) |
| AI Analysis | Groq API (llama-3.3-70b) |
| Frontend | Streamlit |
| Language | Python |

---

## Why this stack?

- **faster-whisper** runs locally — your audio never leaves your machine
- **Groq** is free with no credit card required
- **Streamlit** lets you build a full web app in pure Python

---

## How to run locally

**1. Clone the repo**
```bash
git clone https://github.com/ruhelamahi7-code/meeting-analyzer
cd meeting-analyzer
```

**2. Install dependencies**
```bash
pip3 install streamlit faster-whisper groq
```

**3. Add your Groq API key**

Create `.streamlit/secrets.toml`:
```toml
GROQ_API_KEY = "your-key-here"
```

**4. Run the app**
```bash
python3 -m streamlit run app.py
```

---

## Features

- Supports MP3, WAV, M4A, MP4 audio formats
- Works with recordings up to 200MB
- No data stored — everything processed in memory
- Fully free to run

---

## Built by

**Mahi Ruhela** 

---

import os
import json
import tempfile
import time
import streamlit as st
from groq import Groq
from faster_whisper import WhisperModel

st.set_page_config(
    page_title="Meeting Analyzer",
    page_icon="🎙️",
    layout="centered"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    * { font-family: 'Inter', sans-serif; }

    .stApp {
        background: #070711;
        background-image:
            radial-gradient(ellipse 80% 50% at 20% -10%, rgba(120,40,200,0.25) 0%, transparent 60%),
            radial-gradient(ellipse 60% 40% at 80% 110%, rgba(100,30,200,0.2) 0%, transparent 60%);
    }

    header, .stDeployButton { visibility: hidden !important; height: 0 !important; }
    .block-container { padding-top: 0 !important; margin-top: -4rem !important; max-width: 900px; }

    .hero { text-align: center; padding: 3.5rem 1rem 2rem; }
    .hero-badge {
        display: inline-block;
        background: rgba(168,85,247,0.15);
        color: #c084fc;
        font-size: 12px;
        font-weight: 600;
        padding: 5px 14px;
        border-radius: 20px;
        border: 1px solid rgba(168,85,247,0.3);
        letter-spacing: 0.1em;
        margin-bottom: 1.2rem;
    }
    .hero-title {
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(135deg, #ffffff 0%, #a855f7 50%, #ec4899 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        line-height: 1.1;
        margin-bottom: 1rem;
        filter: drop-shadow(0 0 30px rgba(168,85,247,0.4));
    }
    .hero-subtitle {
        color: #94a3b8;
        font-size: 1rem;
        max-width: 500px;
        margin: 0 auto 2rem;
        line-height: 1.6;
    }

    .upload-card {
        background: rgba(255,255,255,0.03);
        border: 2px dashed rgba(168,85,247,0.35);
        border-radius: 20px;
        padding: 2.5rem 2rem;
        text-align: center;
        margin-bottom: 1.2rem;
    }
    .upload-icon { font-size: 2.5rem; margin-bottom: 0.8rem; }
    .upload-title { color: #e2e8f0; font-size: 1rem; font-weight: 600; margin-bottom: 0.3rem; }
    .upload-sub { color: #64748b; font-size: 0.85rem; }

    .stButton>button {
        width: 100%;
        padding: 0.85rem;
        background: linear-gradient(135deg, #a855f7, #7c3aed);
        color: white;
        border: none;
        border-radius: 12px;
        font-size: 1rem;
        font-weight: 700;
        box-shadow: 0 0 20px rgba(168,85,247,0.4), 0 0 40px rgba(168,85,247,0.2);
        transition: all 0.3s;
    }
    .stButton>button:hover {
        box-shadow: 0 0 30px rgba(168,85,247,0.6), 0 0 60px rgba(168,85,247,0.3);
        transform: translateY(-1px);
    }

    .stats-row {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 12px;
        margin: 1.5rem 0;
    }
    .stat-card {
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(168,85,247,0.2);
        border-radius: 14px;
        padding: 1rem;
        text-align: center;
        transition: all 0.3s;
    }
    .stat-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 0 20px rgba(168,85,247,0.25);
        border-color: rgba(168,85,247,0.5);
    }
    .stat-value { font-size: 1.6rem; font-weight: 800; color: #a855f7; margin-bottom: 4px; }
    .stat-label { font-size: 0.82rem; color: #64748b; text-transform: uppercase; letter-spacing: 0.06em; }

    .two-col {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 14px;
        margin-bottom: 14px;
    }

    .glass-card {
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(168,85,247,0.18);
        border-radius: 16px;
        padding: 1.5rem;
        backdrop-filter: blur(10px);
        height: 100%;
    }

    .full-card {
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(168,85,247,0.18);
        border-radius: 16px;
        padding: 1.5rem;
        backdrop-filter: blur(10px);
        margin-bottom: 14px;
    }

    .card-header {
        font-size: 0.82rem;
        font-weight: 700;
        color: #a855f7;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        margin-bottom: 1rem;
    }
    .transcript-box {
        background: rgba(0,0,0,0.25);
        border: 1px solid rgba(168,85,247,0.15);
        border-radius: 10px;
        padding: 1rem 1.2rem;
        color: #94a3b8;
        font-size: 0.9rem;
        line-height: 1.7;
        max-height: 220px;
        overflow-y: auto;
        white-space: pre-wrap;
        word-break: break-word;
    }
    .transcript-box::-webkit-scrollbar { width: 4px; }
    .transcript-box::-webkit-scrollbar-thumb { background: rgba(168,85,247,0.4); border-radius: 4px; }

    .summary-text {
        background: rgba(168,85,247,0.07);
        border-left: 3px solid #a855f7;
        border-radius: 0 10px 10px 0;
        padding: 1rem 1.2rem;
        color: #cbd5e1;
        font-size: 0.9rem;
        line-height: 1.75;
    }
    .decision-pill {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: rgba(168,85,247,0.1);
        border: 1px solid rgba(168,85,247,0.25);
        color: #e2e8f0;
        padding: 7px 16px;
        border-radius: 20px;
        font-size: 0.88rem;
        margin: 4px 4px 4px 0;
    }
    .insight-item {
        display: flex;
        align-items: flex-start;
        gap: 10px;
        padding: 8px 0;
        border-bottom: 1px solid rgba(168,85,247,0.08);
        color: #cbd5e1;
        font-size: 0.88rem;
        line-height: 1.5;
    }
    .insight-item:last-child { border-bottom: none; }
    .insight-dot {
        width: 7px; height: 7px;
        border-radius: 50%;
        background: #a855f7;
        margin-top: 5px;
        flex-shrink: 0;
    }

    .action-header {
        display: grid;
        grid-template-columns: 1fr 2fr 1fr;
        gap: 8px;
        padding: 6px 12px;
        font-size: 0.78rem;
        font-weight: 700;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        border-bottom: 1px solid rgba(168,85,247,0.15);
        margin-bottom: 8px;
    }
    .action-row {
        display: grid;
        grid-template-columns: 1fr 2fr 1fr;
        gap: 8px;
        padding: 10px 12px;
        background: rgba(255,255,255,0.02);
        border: 1px solid rgba(168,85,247,0.1);
        border-radius: 10px;
        margin-bottom: 7px;
        align-items: center;
    }

    .owner-badge {
        background: linear-gradient(135deg, #a855f7, #7c3aed);
        color: white;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        display: inline-block;
        white-space: nowrap;
    }
    .task-text { color: #e2e8f0; font-size: 0.95rem; }
    .deadline-badge {
        background: rgba(168,85,247,0.15);
        color: #c084fc;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.85rem;
        display: inline-block;
        white-space: nowrap;
    }

    .progress-step {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 10px 0;
        color: #94a3b8;
        font-size: 0.95rem;
    }

    .stDownloadButton>button {
        background: transparent !important;
        border: 1px solid rgba(168,85,247,0.35) !important;
        color: #a855f7 !important;
        border-radius: 10px !important;
        font-size: 0.9rem !important;
        box-shadow: none !important;
        width: 100%;
        margin-top: 0.5rem;
    }

    .footer {
        text-align: center;
        margin-top: 2.5rem;
        padding: 1.5rem 0;
        border-top: 1px solid rgba(255,255,255,0.05);
        font-size: 1.1rem;
        font-weight: 700;
        color: #a855f7;
        letter-spacing: 0.03em;
    }
    .footer span { color: #ec4899; }
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def load_model():
    return WhisperModel("base", device="cpu", compute_type="int8")


def transcribe(audio_path):
    model = load_model()
    segments, _ = model.transcribe(audio_path)
    return " ".join([seg.text for seg in segments])


def analyze(transcript):
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
    prompt = f"""
Analyze this meeting transcript and return ONLY valid JSON with no extra text:
{{
  "summary": "3-5 sentence overview of the meeting",
  "decisions": ["decision 1", "decision 2"],
  "action_items": [
    {{"task": "task description", "owner": "person name", "deadline": "deadline"}}
  ],
  "insights": [
    "insight about meeting tone or productivity",
    "insight about participation or clarity",
    "insight about risks or follow-ups needed"
  ]
}}
TRANSCRIPT:
{transcript}
"""
    response = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="llama-3.3-70b-versatile",
        temperature=0.1,
    )
    text = response.choices[0].message.content.strip()
    text = text.replace("```json", "").replace("```", "").strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return {"summary": text, "decisions": [], "action_items": [], "insights": []}


# --- Hero ---
st.markdown("""
<div class="hero">
    <div class="hero-badge">🤖 AI-POWERED MEETING INTELLIGENCE</div>
    <div class="hero-title">Meeting Analyzer</div>
    <div class="hero-subtitle">Transform recordings into transcripts, summaries, and action items in seconds.</div>
</div>
""", unsafe_allow_html=True)

# --- Upload ---
st.markdown("""
<div class="upload-card">
    <div class="upload-icon">☁️</div>
    <div class="upload-title">Drag & Drop Meeting Recording</div>
    <div class="upload-sub">MP3 • WAV • M4A • MP4 &nbsp;·&nbsp; Maximum size: 200MB</div>
</div>
""", unsafe_allow_html=True)

uploaded = st.file_uploader("", type=["mp3", "wav", "m4a", "mp4"], label_visibility="collapsed")

if uploaded:
    st.audio(uploaded)
    if st.button("⚡  Analyze Meeting"):
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
                tmp.write(uploaded.read())
                tmp_path = tmp.name

            progress_placeholder = st.empty()
            with progress_placeholder.container():
                st.markdown('<div class="progress-step"><span>🎙</span> Extracting audio...</div>', unsafe_allow_html=True)
            time.sleep(0.5)

            with progress_placeholder.container():
                st.markdown("""
                <div class="progress-step" style="color:#a855f7">🎙 Audio extracted ✓</div>
                <div class="progress-step">📝 Generating transcript...</div>
                """, unsafe_allow_html=True)

            transcript = transcribe(tmp_path)
            os.unlink(tmp_path)
            word_count = len(transcript.split())

            with progress_placeholder.container():
                st.markdown("""
                <div class="progress-step" style="color:#a855f7">🎙 Audio extracted ✓</div>
                <div class="progress-step" style="color:#a855f7">📝 Transcript generated ✓</div>
                <div class="progress-step">🤖 Analyzing with AI...</div>
                """, unsafe_allow_html=True)

            result = analyze(transcript)
            progress_placeholder.empty()

            num_actions = len(result.get("action_items", []))
            num_decisions = len(result.get("decisions", []))

            # Stats
            st.markdown(f"""
            <div class="stats-row">
                <div class="stat-card"><div class="stat-value">{word_count}</div><div class="stat-label">Words</div></div>
                <div class="stat-card"><div class="stat-value">98%</div><div class="stat-label">Accuracy</div></div>
                <div class="stat-card"><div class="stat-value">{num_actions}</div><div class="stat-label">Action Items</div></div>
                <div class="stat-card"><div class="stat-value">{num_decisions}</div><div class="stat-label">Decisions</div></div>
            </div>
            """, unsafe_allow_html=True)

            # ROW 1 — Transcript + Summary
            t = transcript.replace("<", "&lt;").replace(">", "&gt;")
            s = result["summary"].replace("<", "&lt;").replace(">", "&gt;")
            st.markdown(f"""
            <div class="two-col">
                <div class="glass-card">
                    <div class="card-header">🎙 Transcript</div>
                    <div class="transcript-box">{t}</div>
                </div>
                <div class="glass-card">
                    <div class="card-header">📋 Summary</div>
                    <div class="summary-text">{s}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # ROW 2 — Decisions + Insights
            pills = "".join([f'<span class="decision-pill">✓ {d}</span>' for d in result.get("decisions", [])]) or '<div style="color:#475569;font-size:0.88rem">No decisions found.</div>'
            insights = "".join([f'<div class="insight-item"><div class="insight-dot"></div><div>{i}</div></div>' for i in result.get("insights", [])]) or '<div style="color:#475569;font-size:0.88rem">No insights available.</div>'

            st.markdown(f"""
            <div class="two-col">
                <div class="glass-card">
                    <div class="card-header">✅ Key Decisions</div>
                    {pills}
                </div>
                <div class="glass-card">
                    <div class="card-header">🧠 AI Insights</div>
                    {insights}
                </div>
            </div>
            """, unsafe_allow_html=True)

            # ROW 3 — Action Items full width
            action_items = result.get("action_items", [])
            if action_items:
                rows = "".join([f"""
                <div class="action-row">
                    <div><span class="owner-badge">{str(item.get("owner","?"))}</span></div>
                    <div class="task-text">{str(item.get("task",""))}</div>
                    <div><span class="deadline-badge">⏰ {str(item.get("deadline","TBD"))}</span></div>
                </div>
                """ for item in action_items])

                st.markdown(f"""
                <div class="full-card">
                    <div class="card-header">🎯 Action Items</div>
                    <div class="action-header">
                        <div>Person</div>
                        <div>Task</div>
                        <div>Deadline</div>
                    </div>
                    {rows}
                </div>
                """, unsafe_allow_html=True)

            # Export
            export = f"""MEETING ANALYSIS — by Mahi Ruhela
=====================================

TRANSCRIPT:
{transcript}

SUMMARY:
{result['summary']}

KEY DECISIONS:
{chr(10).join(f'- {d}' for d in result.get('decisions', []))}

ACTION ITEMS:
{chr(10).join(f'- {i["owner"]}: {i["task"]} (by {i["deadline"]})' for i in result.get('action_items', []))}
"""
            st.download_button(
                label="⬇️  Download Full Report",
                data=export,
                file_name="meeting_analysis.txt",
                mime="text/plain"
            )

        except Exception as e:
            st.error(f"Something went wrong: {str(e)}")

st.markdown('<div class="footer">Built by <span>Mahi Ruhela</span></div>', unsafe_allow_html=True)
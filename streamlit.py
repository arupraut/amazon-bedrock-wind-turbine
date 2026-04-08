import streamlit as st
import requests
import json

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Chat",
    page_icon="✦",
    layout="centered",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Syne:wght@400;600;700&display=swap');

/* Root theme */
:root {
    --bg: #0e0e11;
    --surface: #16161a;
    --border: #2a2a32;
    --accent: #7c6aff;
    --accent-soft: rgba(124,106,255,0.12);
    --text-primary: #f0eff6;
    --text-muted: #7a798a;
    --success: #4ade80;
    --mono: 'DM Mono', monospace;
    --display: 'Syne', sans-serif;
}

/* Global overrides */
html, body, [class*="css"] {
    font-family: var(--display);
    background-color: var(--bg) !important;
    color: var(--text-primary);
}

.stApp { background-color: var(--bg) !important; }

/* Hide default Streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }

/* Main container */
.block-container {
    max-width: 760px !important;
    padding: 3rem 2rem 2rem !important;
}

/* ── Header ── */
.app-header {
    text-align: center;
    margin-bottom: 3rem;
    padding-bottom: 2rem;
    border-bottom: 1px solid var(--border);
}
.app-header .badge {
    display: inline-block;
    font-family: var(--mono);
    font-size: 11px;
    letter-spacing: 0.15em;
    color: var(--accent);
    background: var(--accent-soft);
    border: 1px solid rgba(124,106,255,0.3);
    border-radius: 100px;
    padding: 4px 14px;
    margin-bottom: 16px;
}
.app-header h1 {
    font-size: 2.4rem;
    font-weight: 700;
    color: var(--text-primary);
    letter-spacing: -0.03em;
    margin: 0 0 8px;
    line-height: 1.1;
}
.app-header p {
    color: var(--text-muted);
    font-size: 0.95rem;
    margin: 0;
    font-weight: 400;
}

/* ── Textarea ── */
.stTextArea label {
    font-family: var(--mono);
    font-size: 11px;
    letter-spacing: 0.12em;
    color: var(--text-muted) !important;
    text-transform: uppercase;
    margin-bottom: 8px !important;
}
.stTextArea textarea {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
    color: var(--text-primary) !important;
    font-family: var(--display) !important;
    font-size: 0.97rem !important;
    padding: 16px !important;
    transition: border-color 0.2s;
    resize: none !important;
    min-height: 120px !important;
}
.stTextArea textarea:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px rgba(124,106,255,0.15) !important;
}

/* ── Button ── */
.stButton > button {
    background: var(--accent) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: var(--display) !important;
    font-weight: 600 !important;
    font-size: 0.92rem !important;
    padding: 0.65rem 2.2rem !important;
    letter-spacing: 0.02em;
    cursor: pointer;
    transition: opacity 0.2s, transform 0.15s !important;
    width: 100%;
}
.stButton > button:hover {
    opacity: 0.88 !important;
    transform: translateY(-1px) !important;
}
.stButton > button:active {
    transform: translateY(0) !important;
}

/* ── Response card ── */
.response-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-left: 3px solid var(--accent);
    border-radius: 12px;
    padding: 1.6rem;
    margin-top: 1.8rem;
    animation: fadeSlide 0.35s ease;
}
.response-label {
    font-family: var(--mono);
    font-size: 10px;
    letter-spacing: 0.14em;
    color: var(--accent);
    text-transform: uppercase;
    margin-bottom: 10px;
}
.response-text {
    color: var(--text-primary);
    font-size: 0.97rem;
    line-height: 1.75;
    white-space: pre-wrap;
    word-break: break-word;
}

/* ── Error card ── */
.error-card {
    background: rgba(239,68,68,0.08);
    border: 1px solid rgba(239,68,68,0.3);
    border-radius: 12px;
    padding: 1.2rem 1.6rem;
    margin-top: 1.5rem;
    color: #fca5a5;
    font-family: var(--mono);
    font-size: 0.87rem;
}

/* ── Spinner ── */
.stSpinner > div {
    border-top-color: var(--accent) !important;
}

/* ── Footer ── */
.app-footer {
    text-align: center;
    margin-top: 4rem;
    padding-top: 1.5rem;
    border-top: 1px solid var(--border);
    font-family: var(--mono);
    font-size: 11px;
    color: var(--text-muted);
    letter-spacing: 0.05em;
}

@keyframes fadeSlide {
    from { opacity: 0; transform: translateY(10px); }
    to   { opacity: 1; transform: translateY(0); }
}
</style>
""", unsafe_allow_html=True)

# ── API config ────────────────────────────────────────────────────────────────
API_URL     = "https://<ID>.execute-api.us-east-1.amazonaws.com/Prod/sme_assistant"   # 🔁 replace with your API
API_KEY     = "your-api-key-here"                    # 🔁 replace with your key
API_TIMEOUT = 30                                     # seconds

def call_api(prompt: str) -> str:
    """Send prompt to API and return the response text."""
    headers = {
        "Content-Type": "application/json",
        # "Authorization": f"Bearer {API_KEY}",
    }
    payload = {
        "prompt": prompt,
        "max_tokens": 1024,
    }
    response = requests.post(
        API_URL,
        headers=headers,
        data=json.dumps(payload),
        timeout=API_TIMEOUT,
    )
    response.raise_for_status()
    data = response.json()

    # 🔁 Adjust the key path to match your API's response shape
    return data.get("body") or data.get("output") or data.get("text") or str(data)

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="app-header">
    <div class="badge">✦ AI Assistant</div>
    <h1>Ask anything</h1>
    <p>Type your question below and get an instant AI-powered response.</p>
</div>
""", unsafe_allow_html=True)

# ── Input form ────────────────────────────────────────────────────────────────
user_input = st.text_area(
    "Your prompt",
    placeholder="e.g.  Explain how Amazon Bedrock works in simple terms...",
    height=130,
    label_visibility="visible",
)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    send_clicked = st.button("Send →", use_container_width=True)

# ── API call + response ───────────────────────────────────────────────────────
if send_clicked:
    if not user_input.strip():
        st.markdown('<div class="error-card">⚠ Please enter a prompt before sending.</div>', unsafe_allow_html=True)
    else:
        with st.spinner("Thinking..."):
            try:
                result = call_api(user_input.strip())
                st.markdown(f"""
                <div class="response-card">
                    <div class="response-label">✦ Response</div>
                    <div class="response-text">{result}</div>
                </div>
                """, unsafe_allow_html=True)
            except requests.exceptions.ConnectionError:
                st.markdown('<div class="error-card">✕ Connection error — check your API URL or network.</div>', unsafe_allow_html=True)
            except requests.exceptions.Timeout:
                st.markdown('<div class="error-card">✕ Request timed out — the API took too long to respond.</div>', unsafe_allow_html=True)
            except requests.exceptions.HTTPError as e:
                st.markdown(f'<div class="error-card">✕ HTTP {e.response.status_code} — {e.response.text}</div>', unsafe_allow_html=True)
            except Exception as e:
                st.markdown(f'<div class="error-card">✕ Unexpected error: {e}</div>', unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown('<div class="app-footer">built with streamlit · requests</div>', unsafe_allow_html=True)

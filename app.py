import streamlit as st
import requests
import os

# ── API base URL ──────────────────────────────────────────────────────────────
API_URL = st.secrets.get("API_URL", os.getenv("API_URL", "http://localhost:8000"))

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ResearchMind",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@300;400;500&display=swap');

    :root {
        --bg:       #0a0a0f;
        --surface:  #111118;
        --border:   #1e1e2e;
        --accent:   #e8ff47;
        --accent2:  #47d9ff;
        --muted:    #4a4a6a;
        --text:     #e8e8f0;
        --text-dim: #8888aa;
    }

    html, body, [class*="css"] {
        font-family: 'DM Mono', monospace;
        background-color: var(--bg);
        color: var(--text);
    }
    .stApp { background-color: var(--bg); }
    #MainMenu, footer, header { visibility: hidden; }

    /* Full-width layout */
    .block-container {
        padding-top: 0 !important;
        padding-left: 2.5rem !important;
        padding-right: 2.5rem !important;
        max-width: 100% !important;
    }

    /* ── Centered header ── */
    .rm-header {
        text-align: center;
        padding: 2rem 0 1.2rem 0;
        border-bottom: 1px solid var(--border);
        margin-bottom: 2rem;
    }
    .rm-logo {
        font-family: 'Syne', sans-serif;
        font-weight: 800;
        font-size: 2.8rem;
        color: var(--accent);
        letter-spacing: -1px;
        line-height: 1;
        margin: 0;
    }
    .rm-tag {
        font-size: 0.72rem;
        color: var(--muted);
        letter-spacing: 0.18em;
        text-transform: uppercase;
        margin-top: 0.5rem;
    }

    /* ── Text area ── */
    .stTextArea > div > div > textarea {
        background: var(--surface) !important;
        border: 1px solid var(--border) !important;
        border-radius: 6px !important;
        color: var(--text) !important;
        font-family: 'DM Mono', monospace !important;
        font-size: 0.9rem !important;
        padding: 0.75rem 1rem !important;
        transition: border-color 0.2s;
    }
    .stTextArea > div > div > textarea:focus {
        border-color: var(--accent) !important;
        box-shadow: 0 0 0 2px rgba(232,255,71,0.08) !important;
    }
    .stTextArea label {
        color: var(--text-dim) !important;
        font-size: 0.75rem !important;
        letter-spacing: 0.12em;
        text-transform: uppercase;
    }

    /* ── ALL buttons default to accent yellow (Run button) ── */
    .stButton > button {
        background: var(--accent) !important;
        color: #0a0a0f !important;
        border: none !important;
        border-radius: 4px !important;
        font-family: 'Syne', sans-serif !important;
        font-weight: 700 !important;
        font-size: 0.9rem !important;
        letter-spacing: 0.06em !important;
        padding: 0.65rem 1.8rem !important;
        transition: opacity 0.15s, transform 0.15s !important;
    }
    .stButton > button:hover {
        opacity: 0.88 !important;
        transform: translateY(-1px) !important;
    }

    /* ── Example chip buttons — override yellow style ── */
    .chip-col .stButton > button {
        background: var(--surface) !important;
        color: var(--text-dim) !important;
        border: 1px solid var(--border) !important;
        border-radius: 6px !important;
        font-family: 'DM Mono', monospace !important;
        font-size: 0.72rem !important;
        font-weight: 400 !important;
        letter-spacing: 0 !important;
        padding: 0.35rem 0.7rem !important;
        white-space: nowrap !important;
        height: auto !important;
        line-height: 1.4 !important;
        transform: none !important;
        transition: border-color 0.2s, color 0.2s !important;
    }
    .chip-col .stButton > button:hover {
        border-color: var(--accent) !important;
        color: var(--text) !important;
        background: var(--surface) !important;
        opacity: 1 !important;
        transform: none !important;
    }

    /* ── Pipeline step card ── */
    .step-card {
        background: var(--surface);
        border: 1px solid var(--border);
        border-left: 3px solid var(--accent2);
        border-radius: 6px;
        padding: 1.1rem 1.4rem;
        margin-bottom: 0.85rem;
    }
    .step-card.done   { border-left-color: var(--accent); }
    .step-card.active { border-left-color: #ff9447; }
    .step-label {
        font-size: 0.65rem;
        letter-spacing: 0.2em;
        text-transform: uppercase;
        color: var(--muted);
        margin-bottom: 0.25rem;
    }
    .step-title {
        font-family: 'Syne', sans-serif;
        font-weight: 700;
        font-size: 1rem;
        color: var(--text);
    }
    .step-desc {
        font-size: 0.76rem;
        color: var(--muted);
        margin-top: 3px;
    }

    /* ── Status pill ── */
    .status-pill {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: rgba(71,217,255,0.08);
        border: 1px solid rgba(71,217,255,0.25);
        border-radius: 20px;
        font-size: 0.72rem;
        color: var(--accent2);
        letter-spacing: 0.1em;
        text-transform: uppercase;
        padding: 0.25rem 0.8rem;
        margin-bottom: 1rem;
    }
    .dot {
        width: 6px; height: 6px;
        border-radius: 50%;
        background: var(--accent2);
        animation: pulse 1.4s ease-in-out infinite;
    }
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50%       { opacity: 0.3; }
    }

    /* ── Output panels ── */
    .output-panel {
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: 8px;
        padding: 1.6rem 1.8rem;
        margin-top: 0.8rem;
    }
    .panel-header {
        display: flex;
        align-items: center;
        gap: 10px;
        margin-bottom: 1rem;
        padding-bottom: 0.75rem;
        border-bottom: 1px solid var(--border);
    }
    .panel-title {
        font-family: 'Syne', sans-serif;
        font-weight: 700;
        font-size: 1rem;
        color: var(--accent);
    }
    .output-panel p, .output-panel li,
    .output-panel h1, .output-panel h2, .output-panel h3 {
        color: var(--text);
    }
    .output-panel h2, .output-panel h3 {
        font-family: 'Syne', sans-serif;
        border-bottom: 1px solid var(--border);
        padding-bottom: 4px;
    }

    /* ── Score badge ── */
    .score-badge {
        display: inline-block;
        background: rgba(232,255,71,0.12);
        border: 1px solid var(--accent);
        border-radius: 4px;
        color: var(--accent);
        font-family: 'Syne', sans-serif;
        font-weight: 800;
        font-size: 1.4rem;
        padding: 0.2rem 0.9rem;
        margin-bottom: 1rem;
    }

    /* ── Divider ── */
    hr { border-color: var(--border) !important; margin: 2rem 0 !important; }

    /* ── Expander ── */
    .streamlit-expanderHeader {
        background: var(--surface) !important;
        border: 1px solid var(--border) !important;
        border-radius: 6px !important;
        color: var(--text-dim) !important;
        font-size: 0.78rem !important;
        font-family: 'DM Mono', monospace !important;
    }

    /* ── Download button ── */
    div[data-testid="stDownloadButton"] > button {
        background: var(--surface) !important;
        color: var(--accent) !important;
        border: 1px solid var(--accent) !important;
        border-radius: 4px !important;
        font-family: 'Syne', sans-serif !important;
        font-weight: 700 !important;
        font-size: 0.88rem !important;
        padding: 0.6rem 1.8rem !important;
        width: 100% !important;
        transform: none !important;
    }
    div[data-testid="stDownloadButton"] > button:hover {
        background: rgba(232,255,71,0.08) !important;
        opacity: 1 !important;
        transform: none !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ── Centered header ───────────────────────────────────────────────────────────
st.markdown(
    """
    <div class="rm-header">
        <div class="rm-logo">ResearchMind</div>
        <div class="rm-tag">Multi-Agent Research System</div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ── Session state ─────────────────────────────────────────────────────────────
defaults = {
    "running": False,
    "search_done": False,
    "read_done": False,
    "report": "",
    "critique": "",
    "selected_topic": "",
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ── Two-column main layout ────────────────────────────────────────────────────
col_left, col_right = st.columns([1, 1], gap="large")

# ─────────────────────────── LEFT COLUMN ─────────────────────────────────────
with col_left:

    st.markdown(
        '<p style="font-size:0.72rem;letter-spacing:0.18em;text-transform:uppercase;'
        'color:#4a4a6a;margin-bottom:0.4rem;">Research Topic</p>',
        unsafe_allow_html=True,
    )

    topic_input = st.text_area(
        label="topic_hidden",
        label_visibility="collapsed",
        value=st.session_state.selected_topic,
        placeholder="e.g.  The impact of large language models on scientific discovery",
        height=110,
        key="topic_area",
    )
    topic = topic_input.strip()

    if st.session_state.selected_topic:
        st.session_state.selected_topic = ""

    run_btn = st.button("⚡  Run Research Pipeline", use_container_width=True, key="run_main")

    # ── Example topics ────────────────────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        '<p style="font-size:0.72rem;letter-spacing:0.18em;text-transform:uppercase;'
        'color:#4a4a6a;margin-bottom:0.6rem;">Try an Example</p>',
        unsafe_allow_html=True,
    )

    example_topics = [
        "Quantum computing in 2025",
        "AI in healthcare",
        "Climate & renewable energy",
        "Future of space exploration",
        "Cybersecurity threats 2025",
    ]

    # Render chips as tight auto-width columns
    chip_cols = st.columns(len(example_topics))
    for col, example in zip(chip_cols, example_topics):
        with col:
            st.markdown('<div class="chip-col">', unsafe_allow_html=True)
            if st.button(example, key=f"ex_{example}"):
                st.session_state.selected_topic = example
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

# ─────────────────────────── RIGHT COLUMN ────────────────────────────────────
with col_right:

    st.markdown(
        '<p style="font-size:0.72rem;letter-spacing:0.18em;text-transform:uppercase;'
        'color:#4a4a6a;margin-bottom:0.5rem;">Pipeline Status</p>',
        unsafe_allow_html=True,
    )

    steps = [
        ("01", "Search Agent",  "Discovers relevant URLs via web search",   "search_done"),
        ("02", "Reader Agent",  "Scrapes & extracts content from pages",     "read_done"),
        ("03", "Writer Chain",  "Synthesises a structured research report",  "report"),
        ("04", "Critic Chain",  "Scores and reviews the final report",       "critique"),
    ]

    for num, title, desc, key in steps:
        if st.session_state.running and not st.session_state[key]:
            card_cls = "active"
        elif st.session_state[key]:
            card_cls = "done"
        else:
            card_cls = ""
        icon = "✓ " if st.session_state[key] else ("⟳ " if card_cls == "active" else "")
        st.markdown(
            f"""
            <div class="step-card {card_cls}">
                <div class="step-label">Step {num}</div>
                <div class="step-title">{icon}{title}</div>
                <div class="step-desc">{desc}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

# ── Pipeline trigger ──────────────────────────────────────────────────────────
if run_btn:
    if not topic:
        st.warning("Please enter a research topic before running.")
    else:
        for k in ("search_done", "read_done", "report", "critique"):
            st.session_state[k] = False if k not in ("report", "critique") else ""
        st.session_state.running = True
        st.rerun()

# ── Pipeline execution ────────────────────────────────────────────────────────
if st.session_state.running and topic:
    st.markdown(
        '<div class="status-pill"><div class="dot"></div>Pipeline running…</div>',
        unsafe_allow_html=True,
    )
    with st.spinner("Running all 4 agents — this may take 30–60 seconds…"):
        try:
            response = requests.post(
                f"{API_URL}/research",
                json={"topic": topic},
                timeout=180,
            )
            if response.status_code == 200:
                data = response.json()
                st.session_state.search_done = True
                st.session_state.read_done   = True
                st.session_state.report      = data["report"]
                st.session_state.critique    = data["critique"]
                with st.expander("🔍  Search Agent output", expanded=False):
                    out = data["search_output"]
                    st.text(out[:2000] + ("…" if len(out) > 2000 else ""))
                with st.expander("📄  Reader Agent output", expanded=False):
                    out = data["reader_output"]
                    st.text(out[:2000] + ("…" if len(out) > 2000 else ""))
            else:
                detail = response.json().get("detail", response.text)
                st.error(f"API error {response.status_code}: {detail}")
                st.session_state.running = False
                st.stop()
        except requests.exceptions.ConnectionError:
            st.error(f"Could not connect to the API at `{API_URL}`. Is the Render service running?")
            st.session_state.running = False
            st.stop()
        except requests.exceptions.Timeout:
            st.error("Request timed out after 3 minutes. The pipeline may still be running — try again.")
            st.session_state.running = False
            st.stop()
        except Exception as e:
            st.error(f"Unexpected error: {e}")
            st.session_state.running = False
            st.stop()

    st.session_state.running = False
    st.rerun()

# ── Results — full width below main UI ───────────────────────────────────────
if st.session_state.report:
    st.markdown("<hr>", unsafe_allow_html=True)

    score_line = ""
    for line in st.session_state.critique.splitlines():
        if line.strip().lower().startswith("score"):
            score_line = line.split(":", 1)[-1].strip()
            break
    if score_line:
        st.markdown(
            f'<div style="margin-bottom:0.4rem;font-size:0.7rem;letter-spacing:0.18em;'
            f'text-transform:uppercase;color:#4a4a6a;">Critic Score</div>'
            f'<div class="score-badge">{score_line}</div>',
            unsafe_allow_html=True,
        )

    st.markdown(
        '<div class="output-panel"><div class="panel-header">'
        '<span style="font-size:1.1rem">📝</span>'
        '<span class="panel-title">Research Report</span>'
        '</div>',
        unsafe_allow_html=True,
    )
    st.markdown(st.session_state.report)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown(
        '<div class="output-panel"><div class="panel-header">'
        '<span style="font-size:1.1rem">🔬</span>'
        '<span class="panel-title">Critic Review</span>'
        '</div>',
        unsafe_allow_html=True,
    )
    st.markdown(st.session_state.critique)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    combined = (
        f"# Research Report\n\n{st.session_state.report}"
        f"\n\n---\n\n# Critic Review\n\n{st.session_state.critique}"
    )
    st.download_button(
        label="⬇  Download Report (.md)",
        data=combined,
        file_name=f"research_{topic[:40].replace(' ', '_')}.md",
        mime="text/markdown",
        use_container_width=True,
    )
# streamlit_app.py — Enhanced UI Version

import streamlit as st
from agent_core import run_research, memory

st.set_page_config(
    page_title="AI Research Agent",
    layout="wide",
    page_icon="🌐",
)

# ----------- Custom CSS for beautiful UI -------------
st.markdown("""
<style>

body {
    font-family: 'Inter', sans-serif;
}

.report-container {
    background-color: #1e1e1e;
    padding: 25px;
    border-radius: 16px;
    margin-top: 20px;
}

.card {
    padding: 15px;
    border-radius: 14px;
    background: #262626;
    margin-bottom: 18px;
    border: 1px solid #444;
}

.source-card {
    padding: 12px;
    border-radius: 12px;
    background: #2f2f2f;
    margin-bottom: 10px;
    border-left: 4px solid #5e81ac;
}

h2, h3 {
    color: #ededed !important;
}

</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------

st.title("🌐 AI Web Research Agent (Gemini + Tavily)")
st.markdown("### Ask anything and get reliable research reports with citations.")

query = st.text_area(
    "🔍 **Enter your research query**", 
    height=120,
    placeholder="e.g., Latest advancements in renewable energy storage"
)

col1, col2, col3 = st.columns(3)

with col1:
    max_sources = st.number_input("Max sources", min_value=1, max_value=15, value=5)

with col2:
    export_pdf = st.checkbox("Export PDF", value=False)

with col3:
    use_memory = st.checkbox("Save to memory", value=True)

pdf_filename = st.text_input("PDF filename", value="report.pdf") if export_pdf else None

# ------------------------------ Run Button ------------------------------
run_button = st.button("🚀 Run Research", use_container_width=True)

# ------------------------------ Process Output --------------------------
if run_button:

    if not query.strip():
        st.error("❗ Please enter a research query.")
        st.stop()

    with st.spinner("🔎 Researching the web, analyzing sources, building report…"):
        result = run_research(query, max_sources, export_pdf, pdf_filename, use_memory)

    st.success("🎉 Research complete!")

    # -------------------------- Summary Section --------------------------
    st.markdown("<h2>📘 Summary</h2>", unsafe_allow_html=True)
    st.markdown(f"""
    <div class="card">
        {result["structured"]["full_summary"]}
    </div>
    """, unsafe_allow_html=True)

    # -------------------------- Sources Section --------------------------
    st.markdown("<h2>🔗 Sources</h2>", unsafe_allow_html=True)

    for i, s in enumerate(result["sources"]):
        st.markdown(f"""
        <div class="source-card">
            <b>[{i+1}] {s['title']}</b><br>
            <a href="{s['url']}" target="_blank">{s['url']}</a><br>
            <i>{s['snippet']}</i>
        </div>
        """, unsafe_allow_html=True)

    # -------------------------- PDF Download -----------------------------
    if export_pdf and result["pdf"]:
        with open(result["pdf"], "rb") as f:
            st.download_button("📄 Download Research PDF", f, file_name=pdf_filename)

    # -------------------------- Raw Output -------------------------------
    st.markdown("<h2>🛠 Raw Output (Debug)</h2>", unsafe_allow_html=True)
    st.text_area("Raw Agent Output", result["raw_agent_output"], height=200)


# -------------------------- Sidebar Memory -------------------------------
st.sidebar.header("🕒 Past Queries")
past_runs = memory.list_runs(15)

if past_runs:
    for r in past_runs:
        st.sidebar.write(f"- {r['query']}")
else:
    st.sidebar.write("No past history yet.")

# -------------------------- Footer -------------------------------
st.markdown("""
<style>
.footer {
    position: fixed;
    left: 0;
    bottom: 0;
    width: 100%;
    background-color: #111111;
    color: #cccccc;
    text-align: center;
    padding: 12px 0;
    font-size: 15px;
    border-top: 1px solid #333;
    z-index: 9999;
}

.footer a {
    color: #5e81ac;
    font-weight: bold;
    text-decoration: none;
    margin: 0 8px;
}

.footer a:hover {
    color: #88c0d0;
    text-decoration: underline;
}
</style>

<div class="footer">
    Made with ❤️ by <b>Oushnik Banerjee</b> |
    <a href="https://www.linkedin.com/in/oushnik-banerjee-58b0a524a/" target="_blank">LinkedIn</a> |
    <a href="https://github.com/Oushnik20" target="_blank">GitHub</a>
</div>
""", unsafe_allow_html=True)

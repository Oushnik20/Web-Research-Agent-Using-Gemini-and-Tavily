# 🌐 Web Research Agent — Powered by Gemini + Tavily

A fully-automated **AI Research Assistant** built using **Google Gemini**, **Tavily Search API**, and **Streamlit**.
It performs deep web research, extracts verified information, summarizes insights, and generates PDF reports.

**🚀 Live App:**
[https://web-research-agent-oushnik.streamlit.app/](https://web-research-agent-oushnik.streamlit.app/)

---

## ⭐ Features

* Smart Web Search using Tavily
* AI-powered Research Summaries (Gemini 2.x Models)
* Automatic PDF Report Generation
* Local Research Memory (SQLite)
* Modern UI with Streamlit
* Citations and Sources Extracted Automatically

---

## 🧰 Tech Stack

| Component     | Technology     |
| ------------- | -------------- |
| Web UI        | Streamlit      |
| LLM           | Google Gemini  |
| Search Engine | Tavily         |
| Database      | SQLite         |
| PDF Engine    | ReportLab      |
| Web Scraping  | BeautifulSoup4 |

---

## 📦 Installation

### 1. Clone the repository

```
git clone https://github.com/Oushnik20/Web-Research-Agent-Using-Gemini-and-Tavily.git
cd Web-Research-Agent-Using-Gemini-and-Tavily
```

### 2. Install dependencies

```
pip install -r requirements.txt
```

### 3. Create `.env` file

```
GEMINI_API_KEY=your_gemini_api_key
TAVILY_API_KEY=your_tavily_api_key
```

### 4. Run the app

```
streamlit run streamlit_app.py
```

---

## 📁 Project Structure

```
├── streamlit_app.py        # Main UI
├── agent_core.py           # Research logic
├── utils.py                # PDF + helper functions
├── agent_memory.db         # SQLite memory
├── requirements.txt
└── README.md
```

---

## 📝 How It Works

1. User enters a query
2. Tavily performs real-time web search
3. Gemini analyzes + summarizes results
4. Structured research report is generated
5. PDF export (optional)
6. Recent queries stored in sidebar memory

---

## 👤 Author

**Oushnik Banerjee**
LinkedIn:[ *(https://www.linkedin.com/in/oushnik-banerjee-58b0a524a/)*]
GitHub: [https://github.com/Oushnik20](https://github.com/Oushnik20)




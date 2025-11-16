# agent_core.py — FINAL (Gemini + Tavily FREE VERSION)

import os
import json
import requests
import google.generativeai as genai
from tavily import TavilyClient
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from utils import save_pdf_report, MemoryStore

# ------------------------- LOAD API KEYS -------------------------
load_dotenv()
GEMINI_KEY = os.getenv("GEMINI_API_KEY")
TAVILY_KEY = os.getenv("TAVILY_API_KEY")

genai.configure(api_key=GEMINI_KEY)
tavily = TavilyClient(api_key=TAVILY_KEY)

MODEL = "models/gemini-2.5-flash"

# Memory (sqlite)
memory = MemoryStore("agent_memory.db")


# --------------------- SCRAPE FALLBACK --------------------------------
def quick_fetch_text(url, max_chars=30000):
    """Fetch readable text from the webpage."""
    try:
        r = requests.get(url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(r.text, "html.parser")
        for s in soup(["script", "style", "noscript"]):
            s.extract()
        text = soup.get_text(separator="\n")
        text = "\n".join([line.strip() for line in text.splitlines() if line.strip()])
        return text[:max_chars]
    except:
        return ""


# --------------------- MAIN FREE RESEARCH AGENT ------------------------
def run_research(query, max_sources=5, export_pdf=False, pdf_path="report.pdf", use_memory=True):

    # 1) 🔍 Tavily Web Search
    search = tavily.search(query=query, max_results=max_sources)

    sources = []
    scraped_texts = []

    for i, r in enumerate(search["results"]):
        url = r.get("url", "")
        title = r.get("title", "")
        snippet = r.get("content", "")

        scraped = quick_fetch_text(url)

        sources.append({
            "url": url,
            "title": title,
            "snippet": snippet
        })

        scraped_texts.append(f"📝 Source {i+1}: {url}\n\n{scraped}\n\n")

    # 2) 🧠 Gemini — Summarize
    prompt = f"""
You are a research agent.

User query:
"{query}"

Below are search results and webpage contents from Tavily:

SEARCH RESULTS:
{json.dumps(sources, indent=2)}

SCRAPED CONTENT:
{json.dumps(scraped_texts, indent=2)}

Write a research report in **markdown format** containing:

# Title  
## Overview (4–6 lines)  
## Key Points (10 bullets with citations like [1], [2])  
## Comparison Table (3–6 rows)  
## Summary  
## Sources  
List all URLs as numbered items.

Make the report clean, structured, clear.
"""

    model = genai.GenerativeModel(MODEL)
    ai_response = model.generate_content(prompt)
    final_text = ai_response.text

    # 3) Save memory
    if use_memory:
        memory.save_run({
            "query": query,
            "summary": final_text[:300],
            "sources": sources
        })

    # 4) PDF export
    pdf_file = None
    if export_pdf:
        pdf_file = save_pdf_report(
            pdf_path,
            title=f"Research Report: {query}",
            summary_text=final_text,
            sources=sources
        )

    # 5) Return consistent structure for Streamlit
    return {
        "structured": {
            "full_summary": final_text,
            "short_summary": final_text[:300],
        },
        "sources": sources,
        "pdf": pdf_file,
        "raw_agent_output": final_text
    }


# --------------------- Legacy helper functions -------------------------
def extract_sources_from_text(text):
    """Simple fallback source extractor (kept for compatibility)."""
    import re
    sources = []
    urls = re.findall(r'(https?://[^\s\)\]\}]+)', text)
    for u in urls:
        sources.append({"url": u.strip(), "title": "", "snippet": ""})
    return sources


def fallback_search_links(query, max_results=5):
    """DDG fallback if Tavily fails (rare)."""
    try:
        r = requests.get(
            "https://html.duckduckgo.com/html/",
            params={"q": query},
            timeout=8,
            headers={"User-Agent": "Mozilla/5.0"}
        )
        soup = BeautifulSoup(r.text, "html.parser")
        links = []
        for a in soup.find_all("a", {"class": "result__a"}, href=True):
            if a["href"].startswith("http"):
                links.append(a["href"])
            if len(links) >= max_results:
                break
        return links
    except:
        return []


def create_structured_summary(raw_text, sources, query):
    """Not used (OpenAI version). Kept for compatibility."""
    return {
        "short_summary": raw_text[:300],
        "bullets": [],
        "table": [],
        "full_summary": raw_text
    }

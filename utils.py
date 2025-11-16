# utils.py
import sqlite3
import json
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

class MemoryStore:
    def __init__(self, db_path="agent_memory.db"):
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self._init_tables()

    def _init_tables(self):
        c = self.conn.cursor()
        c.execute("""
        CREATE TABLE IF NOT EXISTS runs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ts INTEGER,
            query TEXT,
            data TEXT
        )
        """)
        c.execute("""
        CREATE TABLE IF NOT EXISTS prefs (
            key TEXT PRIMARY KEY,
            value TEXT
        )
        """)
        self.conn.commit()

    def save_run(self, record):
        c = self.conn.cursor()
        c.execute("INSERT INTO runs (ts, query, data) VALUES (?, ?, ?)",
                  (record.get("timestamp"), record.get("query"), json.dumps(record)))
        self.conn.commit()

    def list_runs(self, limit=20):
        c = self.conn.cursor()
        rows = c.execute("SELECT id, ts, query, data FROM runs ORDER BY ts DESC LIMIT ?", (limit,)).fetchall()
        return [{"id":r[0], "ts":r[1], "query":r[2], "data":json.loads(r[3])} for r in rows]

    def store_preference(self, key, value):
        c = self.conn.cursor()
        c.execute("REPLACE INTO prefs (key, value) VALUES (?, ?)", (key, value))
        self.conn.commit()

    def get_preference(self, key, default=None):
        c = self.conn.cursor()
        r = c.execute("SELECT value FROM prefs WHERE key=?", (key,)).fetchone()
        return r[0] if r else default

# PDF export
def save_pdf_report(path, title, summary_text, sources):
    doc = SimpleDocTemplate(path, pagesize=A4)
    styles = getSampleStyleSheet()
    flow = []
    flow.append(Paragraph(title, styles['Title']))
    flow.append(Spacer(1, 8))
    for line in summary_text.splitlines():
        flow.append(Paragraph(line, styles['Normal']))
        flow.append(Spacer(1,4))
    flow.append(Spacer(1, 12))
    flow.append(Paragraph("Sources:", styles['Heading2']))
    for i,s in enumerate(sources):
        flow.append(Paragraph(f"[{i+1}] {s.get('title','') or s.get('url')}", styles['Normal']))
        flow.append(Paragraph(f"{s.get('url')}", styles['Normal']))
        flow.append(Spacer(1,4))
    doc.build(flow)
    return path

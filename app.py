import streamlit as st
import fitz  # PyMuPDF for PDF parsing
from sentence_transformers import SentenceTransformer
import faiss
import sqlite3
import datetime

# -----------------------------
# Setup
# -----------------------------
st.set_page_config(page_title="AI Candidate Screening", layout="wide")
model = SentenceTransformer("all-MiniLM-L6-v2")

# Simple SQLite persistence
conn = sqlite3.connect("interview.db", check_same_thread=False)
c = conn.cursor()
c.execute("""CREATE TABLE IF NOT EXISTS sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    candidate_name TEXT,
    role TEXT,
    resume_text TEXT,
    start_time TIMESTAMP
)""")
c.execute("""CREATE TABLE IF NOT EXISTS qa (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id INTEGER,
    question TEXT,
    answer TEXT
)""")
conn.commit()

# -----------------------------
# Helper functions
# -----------------------------
def parse_resume(uploaded_file):
    text = ""
    if uploaded_file.name.endswith(".pdf"):
        pdf = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        for page in pdf:
            text += page.get_text()
    else:
        text = uploaded_file.read().decode("utf-8")
    return text

def embed_chunks(chunks):
    embeddings = model.encode(chunks)
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)
    return index, embeddings

def retrieve(query, index, chunks, k=3):
    q_emb = model.encode([query])
    D, I = index.search(q_emb, k)
    return [chunks[i] for i in I[0]]

def generate_question(role, skills, context):
    # Simplified question

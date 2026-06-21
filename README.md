# 📚 Sihah Hadith Search Engine

An AI-powered Hadith search engine using semantic search (FAISS + Sentence Transformers).

---

## 🚀 Features

- Semantic Hadith search (AI-powered)
- FastAPI backend
- FAISS vector similarity search
- Clean web interface (HTML/CSS/JS)
- REST API support

---

## 🧠 Tech Stack

- FastAPI
- FAISS
- Sentence Transformers
- Python (Pandas, Pickle)
- HTML / CSS / JavaScript

---

## 📁 Project Structure

- `app.py` → Main FastAPI backend
- `models/` → FAISS index + dataset
- `static/` → Frontend JS/CSS
- `templates/` → HTML UI
- `data/` → Raw dataset

---

## ▶️ Run Locally

```bash
pip install -r requirements.txt
uvicorn app:app --reload

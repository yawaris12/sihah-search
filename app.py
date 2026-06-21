import os
import pickle
import faiss
import pandas as pd
import re

from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from sentence_transformers import SentenceTransformer

# ----------------------------
# BASE DIRECTORY (IMPORTANT FOR DEPLOYMENT)
# ----------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

print("================================")
print("RUNNING FILE:", BASE_DIR)
print("================================")

app = FastAPI(title="Sihah Hadith AI Search")

# ----------------------------
# STATIC FILES
# ----------------------------
app.mount(
    "/static",
    StaticFiles(directory=os.path.join(BASE_DIR, "static")),
    name="static"
)

# ----------------------------
# LOAD MODEL + DATA
# ----------------------------
print("⚡ Loading model...")
model = SentenceTransformer("all-MiniLM-L6-v2")

print("📦 Loading FAISS index...")
index = faiss.read_index(
    os.path.join(BASE_DIR, "models", "hadith.index")
)

print("📚 Loading dataset...")
with open(os.path.join(BASE_DIR, "models", "hadith_df.pkl"), "rb") as f:
    df = pickle.load(f)

print("🚀 API READY")


# ----------------------------
# HYBRID SEARCH (SEMANTIC + KEYWORD)
# ----------------------------
def search_hadith(query: str, k: int = 10):

    # -------------------------
    # 1. SEMANTIC SEARCH (FAISS)
    # -------------------------
    q_vec = model.encode([query]).astype("float32")
    distances, indices = index.search(q_vec, k)

    semantic_results = df.iloc[indices[0]].copy()
    semantic_results["score"] = 1 / (1 + distances[0])

    # -------------------------
    # 2. KEYWORD SEARCH (Arabic + English)
    # -------------------------
    pattern = re.compile(re.escape(query), re.IGNORECASE)

    if "Arabic_Txt" in df.columns:
        keyword_results = df[
            df["English_Txt"].str.contains(pattern, na=False) |
            df["Arabic_Txt"].str.contains(pattern, na=False)
        ].copy()
    else:
        keyword_results = df[
            df["English_Txt"].str.contains(pattern, na=False)
        ].copy()

    keyword_results = keyword_results.head(k)
    keyword_results["score"] = 1.0  # boost keyword matches

    # -------------------------
    # 3. MERGE + CLEAN
    # -------------------------
    combined = pd.concat([keyword_results, semantic_results])
    combined = combined.drop_duplicates().head(k)

    return combined


# ----------------------------
# HOME PAGE
# ----------------------------
@app.get("/", response_class=HTMLResponse)
def home():
    return """
<!DOCTYPE html>
<html>
<head>
    <title>Sihah Hadith AI Search</title>
    <link rel="stylesheet" href="/static/style.css">
</head>
<body>

<div class="container">
    <h1>📚 Sihah Hadith AI Search</h1>

    <input id="query" placeholder="Search hadith (English or Arabic)..." />
    <button onclick="searchHadith()">Search</button>

    <div id="results"></div>
</div>

<script src="/static/script.js"></script>

</body>
</html>
"""


# ----------------------------
# SEARCH API
# ----------------------------
@app.get("/search")
def search_api(q: str = Query(...), k: int = 10):

    results = search_hadith(q, k)

    return JSONResponse({
        "query": q,
        "results": [
            {
                "hadith_number": int(row["Hadith_Number"]),
                "book": row["Source_Book"],
                "chapter": row["Chapter"],
                "text": str(row["English_Txt"])[:400],
                "score": float(row["score"])
            }
            for _, row in results.iterrows()
        ]
    })
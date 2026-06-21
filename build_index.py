import pandas as pd
import numpy as np
import faiss
import pickle
from sentence_transformers import SentenceTransformer
import os

print("📚 Loading dataset...")

df = pd.read_csv("data/Sihah-Sitta.csv", encoding="utf-8")

df["search_text"] = (
    df["English_Txt"].fillna("") + " " +
    df["Chapter"].fillna("") + " " +
    df["Source_Book"].fillna("")
)

print("🧠 Loading model...")
model = SentenceTransformer("all-MiniLM-L6-v2")

print("⚙️ Creating embeddings...")
embeddings = model.encode(df["search_text"].tolist(), show_progress_bar=True)

embeddings = np.array(embeddings).astype("float32")

dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(embeddings)

# create folder if not exists
os.makedirs("models", exist_ok=True)

print("💾 Saving everything...")

# ✅ SAVE FAISS INDEX
faiss.write_index(index, "models/hadith.index")

# ✅ SAVE DATAFRAME (THIS WAS MISSING!)
with open("models/data.pkl", "wb") as f:
    pickle.dump(df, f)

print("🚀 DONE: index + data saved successfully!")
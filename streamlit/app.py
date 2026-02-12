import os
import streamlit as st
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# -----------------------------
# Load files relative to app.py
# -----------------------------
BASE_DIR = os.path.dirname(__file__)
EMB_PATH = os.path.join(BASE_DIR, "embeddings.npy")
DOC_PATH = os.path.join(BASE_DIR, "documents.txt")

embeddings = np.load(EMB_PATH)

with open(DOC_PATH, "r", encoding="utf-8") as f:
    documents = f.readlines()


# -----------------------------
# Retrieval
# -----------------------------
def retrieve_top_k(query_embedding, embeddings, k=10):
    """Retrieve top-k most similar documents using cosine similarity."""
    similarities = cosine_similarity(
        query_embedding.reshape(1, -1),
        embeddings
    )[0]

    top_k_indices = similarities.argsort()[-k:][::-1]
    return [(documents[i], similarities[i]) for i in top_k_indices]


# -----------------------------
# Query embedding (placeholder)
# -----------------------------
def get_query_embedding(query):
    # Placeholder: random embedding (matches assignment setup)
    return np.random.rand(embeddings.shape[1]).astype(np.float32)


# -----------------------------
# Streamlit UI
# -----------------------------
st.title("Information Retrieval using Document Embeddings")

query = st.text_input("Enter your query:")

if st.button("Search") and query.strip():
    query_embedding = get_query_embedding(query)
    results = retrieve_top_k(query_embedding, embeddings, k=10)

    st.write("### Top 10 Relevant Documents:")
    for doc, score in results:
        st.write(f"- **{doc.strip()}** (Score: {score:.4f})")

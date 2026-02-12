import numpy as np

# Load documents (must match the order used later)
with open("documents.txt", "r", encoding="utf-8") as f:
    documents = [line.strip() for line in f if line.strip()]

embedding_dim = 512
num_documents = len(documents)

document_embeddings = np.random.rand(num_documents, embedding_dim).astype(np.float32)

np.save("embeddings.npy", document_embeddings)

print("embeddings.npy created successfully.")
print("Shape:", document_embeddings.shape)

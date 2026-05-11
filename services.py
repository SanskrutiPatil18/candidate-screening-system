from sentence_transformers import SentenceTransformer
import faiss

model = SentenceTransformer("all-MiniLM-L6-v2")

def embed_chunks(chunks):
    embeddings = model.encode(chunks)
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)
    return index

def retrieve(query, index, chunks, k=3):
    q_emb = model.encode([query])
    D, I = index.search(q_emb, k)
    return [chunks[i] for i in I[0]]

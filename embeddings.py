from sentence_transformers import SentenceTransformer

model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

def embed_text(texts):
    return model.encode(texts, show_progress_bar=False)
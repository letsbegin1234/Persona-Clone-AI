from config import TOP_K


def retrieve_examples(vector_db, embed_text, user_input):
    """
    Retrieve the top-K most similar conversation examples.
    
    Always returns top-K results — no threshold filtering.
    The old threshold (0.15) was filtering out EVERYTHING because
    L2 distances for multilingual text are naturally high.
    Now using cosine similarity (0-1 range) from the vector store.
    """
    query_emb = embed_text([user_input])
    results = vector_db.search(query_emb, k=TOP_K)

    examples = []
    for (user_msg, reply), score in results:
        examples.append((user_msg, reply, score))

    return examples
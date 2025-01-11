from Vectorization.TextVectorizer import TextVectorizer
from Tokenization.TextTokenizer import TextTokenizer

if __name__ == "__main__":
    # Sample texts
    texts = [
        "the quick brown fox jumps over the lazy dog",
        "pack my box with five dozen liquor jugs",
        "how vexingly quick daft zebras jump"
    ]
    
    # Tokenization example
    tokenizer = TextTokenizer(min_freq=1)
    tokenizer.build_vocab(texts)
    token_ids = tokenizer.tokenize(texts[0])
    reconstructed = tokenizer.decode(token_ids)
    print(f"Original: {texts[0]}")
    print(f"Tokenized and reconstructed: {reconstructed}")
    
    # Vectorization example
    vectorizer = TextVectorizer(max_features=100)
    vectorizer.fit(texts)
    vectors = vectorizer.transform(texts)
    print(f"\nVector shape: {vectors.shape}")
    
    # Get top terms for first text
    top_terms = vectorizer.get_top_terms(texts[0])
    print(f"\nTop terms: {top_terms}")
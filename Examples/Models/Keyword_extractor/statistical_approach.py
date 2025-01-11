if __name__ == "__main__":
    # Sample domain vocabulary
    domain_vocab = {
        'machine learning', 'neural network', 'deep learning',
        'algorithm', 'data', 'model', 'training'
    }
    
    # Initialize extractor
    extractor = KeywordExtractor(
        domain_vocab=domain_vocab,
        embedding_path='path/to/embeddings.bin'  # Optional
    )
    
    # Sample text
    text = """
    Machine learning is a subset of artificial intelligence that focuses on developing
    systems that can learn from and make decisions based on data. Deep learning models,
    particularly neural networks, have revolutionized the field by enabling complex
    pattern recognition in various domains.
    """
    
    # Extract keywords
    keywords = extractor.extract_keywords(text, num_keywords=5)
    
    # Print results
    print("\nExtracted Keywords:")
    for kw in keywords:
        print(f"\nKeyword: {kw['keyword']}")
        print(f"Overall Score: {kw['score']:.3f}")
        print("Individual Scores:")
        for method, score in kw['scores'].items():
            print(f"  - {method}: {score:.3f}")
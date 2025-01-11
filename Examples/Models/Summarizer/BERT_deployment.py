if __name__ == "__main__":
    # Initialize summarizer
    summarizer = BertSummarizer()
    
    # Example text
    text = """
    Natural language processing (NLP) is a subfield of linguistics, computer science, and artificial intelligence 
    concerned with the interactions between computers and human language, in particular how to program computers to 
    process and analyze large amounts of natural language data. The goal is a computer capable of understanding the 
    contents of documents, including the contextual nuances of the language within them. The technology can then 
    accurately extract information and insights contained in the documents as well as categorize and organize the 
    documents themselves.
    """
    
    # Generate summary
    result = summarizer.summarize(text, compression_ratio=0.3)
    print("Original text length:", len(text))
    print("Summary length:", len(result['summary']))
    print("\nSummary:", result['summary'])
    print("\nMetadata:", result['metadata'])
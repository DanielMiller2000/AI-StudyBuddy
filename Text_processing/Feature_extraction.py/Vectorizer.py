import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from typing import List, Tuple, Dict
import pickle

class TextVectorizer:
    def __init__(self, max_features: int = 5000, ngram_range: Tuple[int, int] = (1, 1)):
        """
        Initialize the vectorizer.
        
        Args:
            max_features (int): Maximum number of features for TF-IDF
            ngram_range (Tuple[int, int]): Range of n-gram sizes
        """
        self.tfidf = TfidfVectorizer(
            max_features=max_features,
            ngram_range=ngram_range,
            lowercase=False  # Text should already be cleaned
        )
        self.feature_names = None
        self.vocab_size = 0
        
    def fit(self, texts: List[str]) -> None:
        """
        Fit the vectorizer on a list of texts.
        
        Args:
            texts (List[str]): List of cleaned text strings
        """
        self.tfidf.fit(texts)
        self.feature_names = self.tfidf.get_feature_names_out()
        self.vocab_size = len(self.feature_names)
        
    def transform(self, texts: List[str]) -> np.ndarray:
        """
        Transform texts to TF-IDF vectors.
        
        Args:
            texts (List[str]): List of cleaned text strings
            
        Returns:
            np.ndarray: TF-IDF matrix
        """
        return self.tfidf.transform(texts).toarray()
    
    def get_top_terms(self, text: str, n: int = 5) -> List[Tuple[str, float]]:
        """
        Get top n terms with highest TF-IDF scores for a text.
        
        Args:
            text (str): Input text
            n (int): Number of top terms to return
            
        Returns:
            List[Tuple[str, float]]: List of (term, score) pairs
        """
        vector = self.transform([text])[0]
        top_indices = vector.argsort()[-n:][::-1]
        return [
            (self.feature_names[i], vector[i])
            for i in top_indices if vector[i] > 0
        ]
    
    def save(self, filepath: str) -> None:
        """Save vectorizer to file"""
        with open(filepath, 'wb') as f:
            pickle.dump(self, f)
    
    @classmethod
    def load(cls, filepath: str) -> 'TextVectorizer':
        """Load vectorizer from file"""
        with open(filepath, 'rb') as f:
            return pickle.load(f)
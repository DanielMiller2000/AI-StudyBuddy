from collections import Counter
import re
from typing import List, Set, Dict
import nltk
from nltk.tokenize import word_tokenize
nltk.download('punkt')

class TextTokenizer:
    def __init__(self, min_freq: int = 2, max_vocab: int = 10000, stop_words: Set[str] = None):
        """
        Initialize the tokenizer with vocabulary settings.
        
        Args:
            min_freq (int): Minimum frequency for a token to be included in vocabulary
            max_vocab (int): Maximum vocabulary size
            stop_words (Set[str]): Set of words to exclude from tokenization
        """
        self.min_freq = min_freq
        self.max_vocab = max_vocab
        self.stop_words = stop_words or set()
        self.vocab = {}  # word -> index
        self.rev_vocab = {}  # index -> word
        self.word_freqs = Counter()
        
    def build_vocab(self, texts: List[str]) -> None:
        """
        Build vocabulary from a list of texts.
        
        Args:
            texts (List[str]): List of cleaned text strings
        """
        # Count word frequencies
        for text in texts:
            tokens = word_tokenize(text)
            self.word_freqs.update(tokens)
        
        # Filter by frequency and stop words
        filtered_words = [
            word for word, freq in self.word_freqs.most_common()
            if freq >= self.min_freq and word not in self.stop_words
        ]
        
        # Limit vocabulary size
        vocab_words = filtered_words[:self.max_vocab]
        
        # Create vocabulary mappings
        self.vocab = {word: idx for idx, word in enumerate(vocab_words, start=1)}
        self.vocab['<UNK>'] = 0  # Unknown token
        self.rev_vocab = {idx: word for word, idx in self.vocab.items()}
        
    def tokenize(self, text: str) -> List[int]:
        """
        Convert text to sequence of token indices.
        
        Args:
            text (str): Cleaned text string
            
        Returns:
            List[int]: List of token indices
        """
        tokens = word_tokenize(text)
        return [self.vocab.get(token, 0) for token in tokens]  # 0 is <UNK>
    
    def decode(self, token_ids: List[int]) -> str:
        """
        Convert token indices back to text.
        
        Args:
            token_ids (List[int]): List of token indices
            
        Returns:
            str: Reconstructed text
        """
        return ' '.join(self.rev_vocab.get(idx, '<UNK>') for idx in token_ids)
    
    def get_vocab_size(self) -> int:
        """Returns the size of the vocabulary"""
        return len(self.vocab)
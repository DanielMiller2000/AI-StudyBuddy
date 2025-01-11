import torch
from transformers import AutoTokenizer, AutoModel, pipeline
from sklearn.cluster import KMeans
import numpy as np
from typing import List, Dict, Tuple
import logging
from torch.nn.functional import cosine_similarity

class BertSummarizer:
    def __init__(self, model_name: str = 'bert-base-uncased', 
                 max_length: int = 130, 
                 min_length: int = 30,
                 device: str = None):
        """
        Initialize the BERT-based summarizer.
        
        Args:
            model_name (str): Name of the BERT model to use
            max_length (int): Maximum length of the summary
            min_length (int): Minimum length of the summary
            device (str): Device to use for computation ('cuda' or 'cpu')
        """
        self.device = device or ('cuda' if torch.cuda.is_available() else 'cpu')
        self.max_length = max_length
        self.min_length = min_length
        
        # Initialize BERT model and tokenizer
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.bert_model = AutoModel.from_pretrained(model_name).to(self.device)
        
        # Initialize summarization pipeline
        self.summarizer = pipeline("summarization", device=self.device)
        
        # Initialize logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    def _get_sentence_embeddings(self, sentences: List[str]) -> torch.Tensor:
        """
        Generate BERT embeddings for a list of sentences.
        
        Args:
            sentences (List[str]): List of sentences to embed
            
        Returns:
            torch.Tensor: Tensor of sentence embeddings
        """
        embeddings = []
        
        for sentence in sentences:
            # Tokenize and encode sentence
            inputs = self.tokenizer(sentence, 
                                  return_tensors='pt',
                                  padding=True, 
                                  truncation=True, 
                                  max_length=512).to(self.device)
            
            # Generate BERT embeddings
            with torch.no_grad():
                outputs = self.bert_model(**inputs)
                # Use [CLS] token embedding as sentence representation
                sentence_embedding = outputs.last_hidden_state[:, 0, :]
                embeddings.append(sentence_embedding)
        
        return torch.cat(embeddings, dim=0)

    def _select_important_sentences(self, 
                                  sentences: List[str], 
                                  embeddings: torch.Tensor, 
                                  num_sentences: int) -> List[str]:
        """
        Select the most important sentences using clustering.
        
        Args:
            sentences (List[str]): List of sentences
            embeddings (torch.Tensor): Tensor of sentence embeddings
            num_sentences (int): Number of sentences to select
            
        Returns:
            List[str]: Selected important sentences
        """
        if len(sentences) <= num_sentences:
            return sentences
            
        # Convert embeddings to numpy for clustering
        embeddings_np = embeddings.cpu().numpy()
        
        # Perform K-means clustering
        kmeans = KMeans(n_clusters=num_sentences, random_state=42)
        clusters = kmeans.fit_predict(embeddings_np)
        
        # Select sentences closest to cluster centers
        important_sentences = []
        for i in range(num_sentences):
            cluster_sentences = [s for j, s in enumerate(sentences) if clusters[j] == i]
            cluster_embeddings = embeddings[clusters == i]
            
            if len(cluster_sentences) > 0:
                # Find sentence closest to cluster center
                center_distances = cosine_similarity(
                    kmeans.cluster_centers_[i].reshape(1, -1),
                    cluster_embeddings
                )
                best_idx = center_distances.argmax()
                important_sentences.append(cluster_sentences[best_idx])
        
        return important_sentences

    def _chunk_text(self, text: str, max_chunk_size: int = 512) -> List[str]:
        """
        Split text into smaller chunks while preserving sentence boundaries.
        
        Args:
            text (str): Text to split
            max_chunk_size (int): Maximum chunk size in characters
            
        Returns:
            List[str]: List of text chunks
        """
        sentences = text.split('. ')
        chunks = []
        current_chunk = []
        current_length = 0
        
        for sentence in sentences:
            sentence_length = len(sentence)
            
            if current_length + sentence_length > max_chunk_size:
                if current_chunk:
                    chunks.append('. '.join(current_chunk) + '.')
                    current_chunk = [sentence]
                    current_length = sentence_length
                else:
                    # Handle case where single sentence exceeds max_chunk_size
                    chunks.append(sentence + '.')
            else:
                current_chunk.append(sentence)
                current_length += sentence_length
        
        if current_chunk:
            chunks.append('. '.join(current_chunk) + '.')
            
        return chunks

    def summarize(self, text: str, compression_ratio: float = 0.3) -> Dict:
        """
        Generate a summary using BERT embeddings and extractive+abstractive summarization.
        
        Args:
            text (str): Text to summarize
            compression_ratio (float): Target summary length as fraction of original
            
        Returns:
            Dict: Contains 'summary' and 'metadata'
        """
        try:
            # Split text into chunks
            chunks = self._chunk_text(text)
            
            all_summaries = []
            for chunk in chunks:
                # Split into sentences
                sentences = chunk.split('. ')
                
                # Generate embeddings
                embeddings = self._get_sentence_embeddings(sentences)
                
                # Select important sentences
                num_sentences = max(1, int(len(sentences) * compression_ratio))
                important_sentences = self._select_important_sentences(
                    sentences, embeddings, num_sentences
                )
                
                # Join selected sentences and generate abstractive summary
                extractive_summary = ' '.join(important_sentences)
                abstractive_summary = self.summarizer(
                    extractive_summary,
                    max_length=self.max_length,
                    min_length=self.min_length,
                    do_sample=False
                )[0]['summary_text']
                
                all_summaries.append(abstractive_summary)
            
            # Combine summaries
            final_summary = ' '.join(all_summaries)
            
            return {
                'summary': final_summary,
                'metadata': {
                    'original_length': len(text),
                    'summary_length': len(final_summary),
                    'compression_ratio': len(final_summary) / len(text),
                    'num_chunks': len(chunks)
                }
            }
            
        except Exception as e:
            self.logger.error(f"Error during summarization: {str(e)}")
            return {
                'summary': '',
                'metadata': {
                    'error': str(e)
                }
            }
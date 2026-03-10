import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from typing import Dict, List
import os

# Download NLTK data (only needed once)
try:
    nltk.data.find('tokenizers/punkt')
    nltk.data.find('corpora/stopwords')
    nltk.data.find('corpora/wordnet')
    nltk.data.find('taggers/averaged_perceptron_tagger')
except LookupError:
    nltk.download('punkt')
    nltk.download('stopwords')
    nltk.download('wordnet')
    nltk.download('averaged_perceptron_tagger')

class NLPService:
    def __init__(self):
        self.stop_words = set(stopwords.words('english'))
        self.lemmatizer = WordNetLemmatizer()
        self.vectorizer = TfidfVectorizer(
            stop_words='english',
            max_features=5000,
            ngram_range=(1, 2),
            min_df=1,
            max_df=0.9
        )
    
    def preprocess_text(self, text: str) -> str:
        """Preprocess text for NLP analysis"""
        # Convert to lowercase
        text = text.lower()
        
        # Tokenize
        tokens = word_tokenize(text)
        
        # Remove stopwords and punctuation, lemmatize
        filtered_tokens = []
        for token in tokens:
            if (token.isalpha() and 
                token not in self.stop_words and 
                len(token) > 2):
                lemmatized = self.lemmatizer.lemmatize(token)
                filtered_tokens.append(lemmatized)
        
        return ' '.join(filtered_tokens)
    
    def calculate_similarity(self, resume_text: str, job_text: str) -> float:
        """Calculate cosine similarity between resume and job description"""
        try:
            # Preprocess texts
            clean_resume = self.preprocess_text(resume_text)
            clean_job = self.preprocess_text(job_text)
            
            # Create TF-IDF vectors
            tfidf_matrix = self.vectorizer.fit_transform([clean_resume, clean_job])
            
            # Calculate cosine similarity
            similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
            
            # Convert to percentage and round to 2 decimal places
            similarity_score = float(similarity[0][0]) * 100
            
            return round(similarity_score, 2)
            
        except Exception as e:
            print(f"Error calculating similarity: {e}")
            return 0.0
    
    def extract_keywords(self, text: str, top_k: int = 20) -> List[str]:
        """Extract top keywords from text using TF-IDF"""
        try:
            # Preprocess text
            clean_text = self.preprocess_text(text)
            
            # Create TF-IDF vector for single document
            tfidf_matrix = self.vectorizer.fit_transform([clean_text])
            feature_names = self.vectorizer.get_feature_names_out()
            tfidf_scores = tfidf_matrix.toarray()[0]
            
            # Get top keywords
            keyword_scores = list(zip(feature_names, tfidf_scores))
            keyword_scores.sort(key=lambda x: x[1], reverse=True)
            
            top_keywords = [keyword for keyword, score in keyword_scores[:top_k] if score > 0]
            
            return top_keywords
            
        except Exception as e:
            print(f"Error extracting keywords: {e}")
            return []

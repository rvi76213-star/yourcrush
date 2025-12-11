#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
📝 Text Processing Utilities
Text cleaning, normalization, and processing
"""

import re
import string
import unicodedata
from typing import List, Dict, Optional, Tuple
import emoji
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import nltk

# Download NLTK data if needed
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', quiet=True)

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords', quiet=True)


class TextProcessor:
    """📝 Text Processing and Cleaning"""
    
    def __init__(self):
        # Bangla stopwords
        self.bangla_stopwords = set([
            'এবং', 'ও', 'থেকে', 'কে', 'কি', 'কিছু', 'কিন্তু', 'যে', 'এই',
            'তা', 'তাই', 'তিনি', 'তুমি', 'তোমার', 'দিয়ে', 'নেই', 'পরে',
            'বা', 'বার', 'ভালো', 'মনে', 'যখন', 'র', 'লাগে', 'সব', 'সে',
            'হয়', 'হয়ে', 'হয়েছে', 'হল', 'হলে', 'হলো', 'আমি', 'আমার',
            'আপনি', 'আপনার', 'তুই', 'তোর', 'আছে', 'নেই', 'করে', 'করেছে'
        ])
        
        # English stopwords from NLTK
        self.english_stopwords = set(stopwords.words('english'))
        
        # Combined stopwords
        self.stopwords = self.bangla_stopwords.union(self.english_stopwords)
        
        # Common abbreviations
        self.abbreviations = {
            'u': 'you',
            'r': 'are',
            'y': 'why',
            'ur': 'your',
            'btw': 'by the way',
            'lol': 'laughing out loud',
            'omg': 'oh my god',
            'wtf': 'what the fuck',
            'brb': 'be right back',
            'tbh': 'to be honest',
            'idk': 'i don\'t know',
            'ily': 'i love you',
            'im': 'i am',
            'dont': 'don\'t',
            'wont': 'won\'t',
            'cant': 'can\'t',
            'shouldnt': 'shouldn\'t',
            'isnt': 'isn\'t',
            'wasnt': 'wasn\'t'
        }
    
    def clean_text(self, text: str, remove_stopwords: bool = False) -> str:
        """
        Clean and normalize text
        
        Args:
            text: Input text
            remove_stopwords: Whether to remove stopwords
        
        Returns:
            Cleaned text
        """
        try:
            if not text or not isinstance(text, str):
                return ""
            
            # Convert to lowercase
            text = text.lower()
            
            # Normalize unicode
            text = unicodedata.normalize('NFKC', text)
            
            # Remove URLs
            text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
            
            # Remove mentions (@username)
            text = re.sub(r'@\w+', '', text)
            
            # Remove hashtags
            text = re.sub(r'#\w+', '', text)
            
            # Replace abbreviations
            for abbr, full in self.abbreviations.items():
                text = re.sub(r'\b' + re.escape(abbr) + r'\b', full, text)
            
            # Remove extra whitespace
            text = re.sub(r'\s+', ' ', text).strip()
            
            # Remove punctuation (keep Bengali punctuation for now)
            # Remove English punctuation
            text = text.translate(str.maketrans('', '', string.punctuation))
            
            # Remove numbers
            text = re.sub(r'\d+', '', text)
            
            # Remove emojis (optional - you might want to keep them)
            text = self.remove_emojis(text)
            
            # Remove stopwords if requested
            if remove_stopwords:
                words = text.split()
                words = [word for word in words if word not in self.stopwords]
                text = ' '.join(words)
            
            return text.strip()
            
        except Exception as e:
            print(f"Error cleaning text: {e}")
            return text
    
    def remove_emojis(self, text: str) -> str:
        """Remove emojis from text"""
        try:
            # Remove emojis using emoji library
            return emoji.replace_emoji(text, replace='')
        except:
            # Fallback regex method
            emoji_pattern = re.compile("["
                u"\U0001F600-\U0001F64F"  # emoticons
                u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                u"\U0001F680-\U0001F6FF"  # transport & map symbols
                u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                u"\U00002500-\U00002BEF"  # chinese char
                u"\U00002702-\U000027B0"
                u"\U00002702-\U000027B0"
                u"\U000024C2-\U0001F251"
                u"\U0001f926-\U0001f937"
                u"\U00010000-\U0010ffff"
                u"\u2640-\u2642"
                u"\u2600-\u2B55"
                u"\u200d"
                u"\u23cf"
                u"\u23e9"
                u"\u231a"
                u"\ufe0f"  # dingbats
                u"\u3030"
                "]+", flags=re.UNICODE)
            return emoji_pattern.sub(r'', text)
    
    def extract_emojis(self, text: str) -> List[str]:
        """Extract emojis from text"""
        try:
            return [c for c in text if c in emoji.EMOJI_DATA]
        except:
            return []
    
    def tokenize(self, text: str, language: str = 'english') -> List[str]:
        """
        Tokenize text into words
        
        Args:
            text: Input text
            language: Language for tokenization
        
        Returns:
            List of tokens
        """
        try:
            if language == 'bengali':
                # Simple Bengali tokenization (split by spaces)
                return text.split()
            else:
                # Use NLTK for English
                return word_tokenize(text)
        except:
            # Fallback to simple split
            return text.split()
    
    def get_word_frequency(self, text: str, top_n: int = 10) -> Dict[str, int]:
        """
        Get word frequency in text
        
        Args:
            text: Input text
            top_n: Number of top words to return
        
        Returns:
            Dictionary of word frequencies
        """
        try:
            # Clean text
            cleaned_text = self.clean_text(text, remove_stopwords=True)
            
            # Tokenize
            tokens = self.tokenize(cleaned_text)
            
            # Count frequencies
            freq = {}
            for token in tokens:
                if token not in self.stopwords and len(token) > 1:
                    freq[token] = freq.get(token, 0) + 1
            
            # Get top N words
            sorted_freq = sorted(freq.items(), key=lambda x: x[1], reverse=True)
            return dict(sorted_freq[:top_n])
            
        except Exception as e:
            print(f"Error getting word frequency: {e}")
            return {}
    
    def detect_language(self, text: str) -> str:
        """
        Detect language of text (Bengali/English)
        
        Args:
            text: Input text
        
        Returns:
            'bengali', 'english', or 'mixed'
        """
        try:
            if not text:
                return 'unknown'
            
            # Count Bengali and English characters
            bengali_chars = 0
            english_chars = 0
            total_chars = len(text)
            
            for char in text:
                # Bengali Unicode range: 0980-09FF
                if '\u0980' <= char <= '\u09FF':
                    bengali_chars += 1
                # English letters
                elif 'a' <= char.lower() <= 'z':
                    english_chars += 1
            
            # Calculate ratios
            bengali_ratio = bengali_chars / total_chars if total_chars > 0 else 0
            english_ratio = english_chars / total_chars if total_chars > 0 else 0
            
            # Determine language
            if bengali_ratio > 0.7:
                return 'bengali'
            elif english_ratio > 0.7:
                return 'english'
            elif bengali_ratio > 0.3 and english_ratio > 0.3:
                return 'mixed'
            else:
                return 'unknown'
                
        except Exception as e:
            print(f"Error detecting language: {e}")
            return 'unknown'
    
    def translate_banglish_to_bangla(self, text: str) -> str:
        """
        Convert Banglish (Bengali written in English) to Bangla
        
        Args:
            text: Banglish text
        
        Returns:
            Converted Bangla text
        """
        # Simple Banglish to Bangla mapping
        banglish_map = {
            'a': 'আ', 'b': 'ব', 'c': 'ক', 'd': 'ড', 'e': 'ই',
            'f': 'ফ', 'g': 'গ', 'h': 'হ', 'i': 'ই', 'j': 'জ',
            'k': 'ক', 'l': 'ল', 'm': 'ম', 'n': 'ন', 'o': 'ও',
            'p': 'প', 'q': 'ক', 'r': 'র', 's': 'স', 't': 'ট',
            'u': 'উ', 'v': 'ভ', 'w': 'ও', 'x': 'এক্স', 'y': 'ই',
            'z': 'জ', 'oi': 'ঐ', 'ou': 'ঔ'
        }
        
        try:
            result = []
            i = 0
            while i < len(text):
                # Check for two-character combinations first
                if i + 1 < len(text):
                    two_chars = text[i:i+2].lower()
                    if two_chars in banglish_map:
                        result.append(banglish_map[two_chars])
                        i += 2
                        continue
                
                # Check for single character
                char = text[i].lower()
                if char in banglish_map:
                    result.append(banglish_map[char])
                else:
                    result.append(char)
                i += 1
            
            return ''.join(result)
            
        except Exception as e:
            print(f"Error converting Banglish: {e}")
            return text
    
    def sentiment_analysis(self, text: str) -> Dict[str, float]:
        """
        Simple sentiment analysis
        
        Args:
            text: Input text
        
        Returns:
            Dictionary with sentiment scores
        """
        try:
            # Positive and negative word lists
            positive_words = [
                'good', 'great', 'excellent', 'awesome', 'happy', 'joy',
                'love', 'like', 'best', 'beautiful', 'nice', 'wonderful',
                'ভালো', 'সুন্দর', 'চমৎকার', 'অসাধারণ', 'খুশি', 'আনন্দ',
                'ভালোবাসা', 'প্রেম', 'পছন্দ'
            ]
            
            negative_words = [
                'bad', 'terrible', 'awful', 'sad', 'angry', 'hate',
                'dislike', 'worst', 'ugly', 'horrible', 'pain',
                'খারাপ', 'ভয়ঙ্কর', 'দুঃখ', 'রাগ', 'ঘৃণা', 'অপছন্দ',
                'যন্ত্রণা', 'বেদনা', 'কষ্ট'
            ]
            
            cleaned_text = self.clean_text(text).lower()
            tokens = self.tokenize(cleaned_text)
            
            positive_count = sum(1 for token in tokens if token in positive_words)
            negative_count = sum(1 for token in tokens if token in negative_words)
            total_words = len(tokens)
            
            if total_words == 0:
                return {'positive': 0, 'negative': 0, 'neutral': 1, 'score': 0}
            
            positive_score = positive_count / total_words
            negative_score = negative_count / total_words
            neutral_score = 1 - positive_score - negative_score
            
            # Overall sentiment score (-1 to 1)
            sentiment_score = positive_score - negative_score
            
            return {
                'positive': round(positive_score, 3),
                'negative': round(negative_score, 3),
                'neutral': round(neutral_score, 3),
                'score': round(sentiment_score, 3),
                'detected_words': {
                    'positive': positive_count,
                    'negative': negative_count,
                    'total': total_words
                }
            }
            
        except Exception as e:
            print(f"Error in sentiment analysis: {e}")
            return {'positive': 0, 'negative': 0, 'neutral': 1, 'score': 0}
    
    def extract_keywords(self, text: str, num_keywords: int = 5) -> List[str]:
        """
        Extract keywords from text
        
        Args:
            text: Input text
            num_keywords: Number of keywords to extract
        
        Returns:
            List of keywords
        """
        try:
            # Get word frequencies
            freq = self.get_word_frequency(text, top_n=num_keywords * 2)
            
            # Filter out very short words and common words
            keywords = []
            for word, count in freq.items():
                if len(word) > 2 and word not in self.stopwords:
                    keywords.append(word)
                    if len(keywords) >= num_keywords:
                        break
            
            return keywords
            
        except Exception as e:
            print(f"Error extracting keywords: {e}")
            return []
    
    def calculate_similarity(self, text1: str, text2: str) -> float:
        """
        Calculate similarity between two texts
        
        Args:
            text1: First text
            text2: Second text
        
        Returns:
            Similarity score (0 to 1)
        """
        try:
            # Clean and tokenize
            tokens1 = set(self.tokenize(self.clean_text(text1, remove_stopwords=True)))
            tokens2 = set(self.tokenize(self.clean_text(text2, remove_stopwords=True)))
            
            if not tokens1 or not tokens2:
                return 0.0
            
            # Calculate Jaccard similarity
            intersection = len(tokens1.intersection(tokens2))
            union = len(tokens1.union(tokens2))
            
            return intersection / union if union > 0 else 0.0
            
        except Exception as e:
            print(f"Error calculating similarity: {e}")
            return 0.0
    
    def summarize_text(self, text: str, max_sentences: int = 3) -> str:
        """
        Simple text summarization
        
        Args:
            text: Input text
            max_sentences: Maximum sentences in summary
        
        Returns:
            Summarized text
        """
        try:
            # Split into sentences
            sentences = re.split(r'[.!?]+', text)
            sentences = [s.strip() for s in sentences if s.strip()]
            
            if len(sentences) <= max_sentences:
                return text
            
            # Simple ranking by length (can be improved)
            ranked_sentences = sorted(
                sentences,
                key=lambda s: len(s),
                reverse=True
            )
            
            # Take top sentences
            summary_sentences = ranked_sentences[:max_sentences]
            
            # Sort back to original order
            summary_sentences = [
                s for s in sentences 
                if s in summary_sentences
            ]
            
            return '. '.join(summary_sentences) + '.'
            
        except Exception as e:
            print(f"Error summarizing text: {e}")
            return text[:500] + '...' if len(text) > 500 else text
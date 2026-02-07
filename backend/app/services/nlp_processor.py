import re
import json
from typing import List, Dict, Set
import spacy
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

class NLPProcessor:
    """Classical NLP processing for resume and job text"""
    
    def __init__(self):
        # Load small spaCy model (CPU-friendly)
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except:
            raise Exception("spaCy model not found. Run: python -m spacy download en_core_web_sm")
        
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words('english'))
        
        # Common skills database (expandable)
        self.skill_patterns = self._build_skill_patterns()
    
    def _build_skill_patterns(self) -> List[str]:
        """Build regex patterns for common skills"""
        skills = [
            # Programming Languages
            r'\bpython\b', r'\bjava\b', r'\bjavascript\b', r'\btypescript\b',
            r'\bc\+\+\b', r'\bc#\b', r'\bruby\b', r'\bphp\b', r'\bswift\b',
            r'\bkotlin\b', r'\bgo\b', r'\brust\b', r'\br\b', r'\bscala\b',
            
            # Web Technologies
            r'\breact\b', r'\bangular\b', r'\bvue\.?js\b', r'\bnode\.?js\b',
            r'\bexpress\b', r'\bdjango\b', r'\bflask\b', r'\bfastapi\b',
            r'\bhtml5?\b', r'\bcss3?\b', r'\bsass\b', r'\btailwind\b',
            
            # Databases
            r'\bmysql\b', r'\bpostgresql\b', r'\bmongodb\b', r'\bredis\b',
            r'\bsqlite\b', r'\boracle\b', r'\bsql\b', r'\bnosql\b',
            
            # Cloud & DevOps
            r'\baws\b', r'\bazure\b', r'\bgcp\b', r'\bdocker\b', r'\bkubernetes\b',
            r'\bjenkins\b', r'\bgit\b', r'\bgithub\b', r'\bgitlab\b', r'\bci/cd\b',
            
            # Data Science & ML
            r'\bmachine\s+learning\b', r'\bdeep\s+learning\b', r'\bdata\s+science\b',
            r'\bpandas\b', r'\bnumpy\b', r'\bscikit-learn\b', r'\btensorflow\b',
            r'\bpytorch\b', r'\btableau\b', r'\bpower\s+bi\b',
            
            # Other
            r'\bagile\b', r'\bscrum\b', r'\bjira\b', r'\bapi\b', r'\brest\b',
            r'\bgraphql\b', r'\bmicroservices\b', r'\btdd\b', r'\btest\s+automation\b'
        ]
        return skills
    
    def preprocess_text(self, text: str) -> str:
        """
        Clean and preprocess text
        - Lowercase
        - Remove special characters
        - Remove extra whitespace
        """
        # Lowercase
        text = text.lower()
        
        # Remove URLs
        text = re.sub(r'http\S+|www\S+', '', text)
        
        # Remove email addresses
        text = re.sub(r'\S+@\S+', '', text)
        
        # Remove special characters but keep spaces
        text = re.sub(r'[^a-zA-Z0-9\s\+#\.]', ' ', text)
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    def extract_skills(self, text: str) -> List[str]:
        """
        Extract skills using regex patterns
        """
        text_lower = text.lower()
        skills_found = set()
        
        for pattern in self.skill_patterns:
            matches = re.finditer(pattern, text_lower)
            for match in matches:
                skill = match.group().strip()
                # Clean up the skill name
                skill = re.sub(r'[^\w\s\+#\.]', '', skill)
                if len(skill) > 1:  # Avoid single characters
                    skills_found.add(skill)
        
        return sorted(list(skills_found))
    
    def extract_keywords(self, text: str, top_n: int = 20) -> List[str]:
        """
        Extract important keywords using:
        1. Tokenization
        2. Stop word removal
        3. Lemmatization
        4. Frequency analysis
        """
        # Preprocess
        processed_text = self.preprocess_text(text)
        
        # Tokenize
        tokens = word_tokenize(processed_text)
        
        # Remove stop words and short words
        filtered_tokens = [
            token for token in tokens 
            if token not in self.stop_words and len(token) > 2
        ]
        
        # Lemmatize
        lemmatized = [self.lemmatizer.lemmatize(token) for token in filtered_tokens]
        
        # Count frequency
        word_freq = {}
        for word in lemmatized:
            word_freq[word] = word_freq.get(word, 0) + 1
        
        # Sort by frequency and get top N
        sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
        keywords = [word for word, freq in sorted_words[:top_n]]
        
        return keywords
    
    def extract_entities(self, text: str) -> Dict[str, List[str]]:
        """
        Extract named entities using spaCy
        Returns: organizations, locations, etc.
        """
        doc = self.nlp(text[:1000000])  # Limit for performance
        
        entities = {
            'organizations': [],
            'locations': [],
            'persons': []
        }
        
        for ent in doc.ents:
            if ent.label_ == 'ORG':
                entities['organizations'].append(ent.text)
            elif ent.label_ == 'GPE':
                entities['locations'].append(ent.text)
            elif ent.label_ == 'PERSON':
                entities['persons'].append(ent.text)
        
        return entities
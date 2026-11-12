import re
import string
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer, PorterStemmer

# Ensure NLTK datasets are ready
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', quiet=True)
    nltk.download('punkt_tab', quiet=True)

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords', quiet=True)

try:
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('wordnet', quiet=True)

# Standard and Legal specific stopwords
try:
    STANDARD_STOPWORDS = set(stopwords.words('english'))
except:
    STANDARD_STOPWORDS = {
        'the', 'a', 'an', 'and', 'or', 'but', 'if', 'then', 'so', 'because', 'as', 'until', 'while',
        'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during',
        'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off',
        'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why',
        'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no',
        'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will',
        'just', 'don', 'should', 'now'
    }

# Stopwords to filter out boilerplate legal noise while preserving substantive terms
LEGAL_BOILERPLATE_STOPWORDS = {
    'page', 'date', 'dated', 'signed', 'witnesseth', 'whereas', 'hereof', 'thereto', 'wherein',
    'thereof', 'wherefore', 'hereto', 'thereunder', 'therein', 'aforesaid', 'hereinabove',
    'hereinafter', 'hereinbefore', 'duly', 'party_of_first_part', 'party_of_second_part'
}

CUSTOM_STOPWORDS = STANDARD_STOPWORDS.union(LEGAL_BOILERPLATE_STOPWORDS)

class LegalNLPPreprocessor:
    def __init__(self):
        self.lemmatizer = WordNetLemmatizer()
        self.stemmer = PorterStemmer()
        self.stopwords = CUSTOM_STOPWORDS
        
        # Regex patterns to protect legal citations during sentence boundary segmentation
        self.abbr_patterns = [
            (r'\bSec\.\s*', 'Sec_DOT_ '),
            (r'\bv\.\s*', 'v_DOT_ '),
            (r'\bvs\.\s*', 'vs_DOT_ '),
            (r'\bArt\.\s*', 'Art_DOT_ '),
            (r'\bNo\.\s*', 'No_DOT_ '),
            (r'\bNos\.\s*', 'Nos_DOT_ '),
            (r'\bHon\'ble\s*', 'Honble_DOT_ '),
            (r'\bPara\.\s*', 'Para_DOT_ '),
            (r'\bLtd\.\s*', 'Ltd_DOT_ '),
            (r'\bPvt\.\s*', 'Pvt_DOT_ '),
            (r'\bInc\.\s*', 'Inc_DOT_ '),
            (r'\bCo\.\s*', 'Co_DOT_ '),
            (r'\bet\s+al\.\s*', 'et_al_DOT_ '),
            (r'\bi\.e\.\s*', 'ie_DOT_ '),
            (r'\be\.g\.\s*', 'eg_DOT_ '),
            (r'\bU/S\.\s*', 'US_DOT_ '),
            (r'\bVol\.\s*', 'Vol_DOT_ '),
            (r'\bcl\.\s*', 'cl_DOT_ '),
        ]

    def protect_legal_abbreviations(self, text):
        """Replaces dots in common legal abbreviations to prevent premature sentence splitting."""
        protected = text
        for pat, repl in self.abbr_patterns:
            protected = re.sub(pat, repl, protected, flags=re.IGNORECASE)
        # Protect decimal numbers e.g., Section 420.1 or Rs. 10.50
        protected = re.sub(r'(\d+)\.(\d+)', r'\1_DECIMAL_\2', protected)
        return protected

    def restore_legal_abbreviations(self, text):
        """Restores protected legal abbreviations back to their original form."""
        restored = text
        for pat, repl in self.abbr_patterns:
            clean_repl = repl.strip()
            orig = pat.replace(r'\b', '').replace(r'\s*', '').replace('\\', '')
            restored = restored.replace(clean_repl, orig)
        restored = restored.replace('_DECIMAL_', '.')
        return restored

    def clean_text(self, text):
        """Cleans artifacts, excessive whitespace, page headers/footers, and unprintable characters."""
        if not text:
            return ""
        # Remove null bytes and non-printable characters
        text = text.replace('\x00', ' ')
        # Normalize carriage returns and tabs
        text = text.replace('\r\n', '\n').replace('\r', '\n')
        # Remove repetitive header/footer page lines e.g. "Page 1 of 12"
        text = re.sub(r'(?i)page\s+\d+\s+(of\s+\d+)?', ' ', text)
        # Remove document stamps/dates markers
        text = re.sub(r'[-_=]{3,}', ' ', text)
        # Replace multiple spaces with single space
        text = re.sub(r'[ \t]+', ' ', text)
        # Normalize newlines
        text = re.sub(r'\n{2,}', '\n\n', text)
        return text.strip()

    def segment_sentences(self, text):
        """Splits legal text into distinct meaningful sentences while respecting citations and clauses."""
        cleaned = self.clean_text(text)
        if not cleaned:
            return []
        
        # Protect abbreviations
        protected = self.protect_legal_abbreviations(cleaned)
        
        # First split by paragraph / numbered clauses if structured like 1., (a), Clause 2:
        raw_sentences = []
        try:
            raw_sentences = sent_tokenize(protected)
        except Exception:
            # Fallback regex split
            raw_sentences = re.split(r'(?<=[.!?])\s+', protected)
        
        final_sentences = []
        for s in raw_sentences:
            s_restored = self.restore_legal_abbreviations(s).strip()
            # Clean leading dashes or list symbols
            s_restored = re.sub(r'^[\s\-\*\•\d+\.\)]+', '', s_restored).strip()
            # Filter out very short noisy fragments (< 4 words)
            if len(s_restored.split()) >= 4:
                final_sentences.append(s_restored)
                
        return final_sentences

    def tokenize_and_normalize(self, text, remove_stops=True, lemmatize=True):
        """Tokenizes text, strips punctuation/digits, removes stopwords, and lemmatizes."""
        text_lower = text.lower()
        # Remove punctuation
        tokens = re.findall(r'\b[a-zA-Z]{3,}\b', text_lower)
        
        processed_tokens = []
        for tok in tokens:
            if remove_stops and tok in self.stopwords:
                continue
            if lemmatize:
                try:
                    tok = self.lemmatizer.lemmatize(tok)
                except:
                    tok = self.stemmer.stem(tok)
            processed_tokens.append(tok)
            
        return processed_tokens

    def get_word_count(self, text):
        """Returns clean word count of a given text."""
        return len(re.findall(r'\b\w+\b', text))

import re
import nltk
from nltk.corpus   import stopwords
from nltk.stem     import PorterStemmer
from nltk.tokenize import word_tokenize

# Download NLTK data on first run
nltk.download('punkt', quiet=True)
nltk.download('punkt_tab', quiet=True)
nltk.download('stopwords', quiet=True)
nltk.download('averaged_perceptron_tagger', quiet=True)
nltk.download('wordnet', quiet=True)

_stemmer   = PorterStemmer()
_stopwords = set(stopwords.words('english'))

_RESUME_STOPWORDS = {
    'experience', 'work', 'project', 'projects', 'using', 'used',
    'developed', 'built', 'responsible', 'team', 'company', 'role',
    'including', 'also', 'etc', 'years', 'year', 'month', 'months',
}
_stopwords |= _RESUME_STOPWORDS

def preprocess(text: str, stem: bool = True) -> str:
    text = text.lower()
    text = re.sub(r'http\S+|www\S+', ' ', text)
    text = re.sub(r'\S+@\S+', ' ', text)
    text = re.sub(r'\d+', ' ', text)
    text = re.sub(r'[^a-z\s]', ' ', text)
    tokens = word_tokenize(text)
    tokens = [t for t in tokens if t not in _stopwords and len(t) > 2]
    if stem:
        tokens = [_stemmer.stem(t) for t in tokens]
    return ' '.join(tokens)

def extract_skills(text: str) -> list[str]:
    SKILL_KEYWORDS = [
        'python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'go',
        'rust', 'kotlin', 'swift', 'r', 'scala', 'php', 'ruby',
        'react', 'angular', 'vue', 'node', 'express', 'django', 'flask',
        'spring', 'springboot', 'fastapi', 'html', 'css', 'bootstrap',
        'machine learning', 'deep learning', 'nlp', 'tensorflow', 'pytorch',
        'scikit-learn', 'pandas', 'numpy', 'lightgbm', 'xgboost', 'keras',
        'computer vision', 'opencv',
        'sql', 'mysql', 'postgresql', 'mongodb', 'firebase', 'redis',
        'kafka', 'spark', 'hadoop', 'hive', 'airflow',
        'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'jenkins',
        'git', 'github', 'ci/cd', 'terraform', 'ansible',
        'rest api', 'graphql', 'microservices', 'agile', 'scrum',
        'android', 'ios', 'flutter', 'react native',
    ]
    text_lower = text.lower()
    found = [s for s in SKILL_KEYWORDS if s in text_lower]
    return sorted(set(found))

def extract_education(text: str) -> str:
    text_lower = text.lower()
    if any(k in text_lower for k in ('phd', 'doctorate', 'ph.d')):
        return 'PhD'
    if any(k in text_lower for k in ('master', 'm.tech', 'mba', 'msc', 'm.e')):
        return 'Masters'
    if any(k in text_lower for k in ('bachelor', 'b.tech', 'b.e', 'bsc', 'b.sc', 'b.com', 'bca')):
        return 'Bachelors'
    if any(k in text_lower for k in ('diploma', 'polytechnic')):
        return 'Diploma'
    return 'Not Detected'

def extract_experience_years(text: str) -> float:
    patterns = [
        r'(\d+\.?\d*)\s*\+?\s*years?\s+of\s+experience',
        r'(\d+\.?\d*)\s*\+?\s*years?\s+experience',
        r'experience\s+of\s+(\d+\.?\d*)\s*\+?\s*years?',
        r'(\d+\.?\d*)\s*\+?\s*yrs?',
    ]
    found = []
    for pat in patterns:
        matches = re.findall(pat, text.lower())
        found.extend(float(m) for m in matches)
    return max(found) if found else 0.0

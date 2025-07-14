import re

try:
    from nltk.stem.snowball import SnowballStemmer
    stemmer = SnowballStemmer("english")
except ImportError:
    stemmer = None

try:
    from bs4 import BeautifulSoup
except ImportError:
    BeautifulSoup = None

try:
    import PyPDF2
except ImportError:
    PyPDF2 = None

def tokenize(text):
    """
    Splits text into tokens (words).
    """
    return re.findall(r'\b\w+\b', text.lower())

def normalize(token):
    """
    Converts a token to its normalized form (lowercase + stemming if available).
    """
    token = token.lower()
    if stemmer:
        return stemmer.stem(token)
    return token

def extract_text_from_html(html):
    """
    Extracts text from an HTML file.
    """
    if not BeautifulSoup:
        raise ImportError("To work with HTML, install the beautifulsoup4 package")
    soup = BeautifulSoup(html, "html.parser")
    return soup.get_text(separator=" ", strip=True)

def extract_text_from_pdf(pdf_path):
    """
    Extracts text from a PDF file.
    """
    if not PyPDF2:
        raise ImportError("To work with PDF, install the PyPDF2 package")
    text = ""
    with open(pdf_path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            text += page.extract_text() or ""
    return text
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import re
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Download NLTK resources (run once)
nltk.download('punkt')
nltk.download('stopwords')

# Initialize stop words and SBERT model
stop_words = set(stopwords.words('english'))
model = SentenceTransformer('all-MiniLM-L6-v2')  # Lightweight SBERT model for English

reference ="""A compassionate intermediate college teacher, Shiva, recounts the tragic
    story of his best friend Ramu and his girlfriend Asha, who, as teenagers,
    faced the devastating consequences of an unplanned pregnancy,
    highlighting the importance of parental guidance and open
    communication during adolescence."""


def tokenize_text(text):
    # Convert to lowercase
    text = text.lower()
    # Tokenize
    tokens = word_tokenize(text)
    return tokens

ref_words = tokenize_text(reference)
embeddings = model.encode(ref_words, convert_to_numpy=True)

print(embeddings)
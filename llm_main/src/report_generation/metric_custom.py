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
# model = SentenceTransformer('all-MiniLM-L6-v2')  # Lightweight SBERT model for English
# model = SentenceTransformer('Alibaba-NLP/gte-large-en-v1.5')  # GTE model for English
model = SentenceTransformer('Alibaba-NLP/gte-large-en-v1.5', trust_remote_code=True)

# Function to tokenize text
def tokenize_text(text):
    # Convert to lowercase
    text = text.lower()
    # Tokenize
    tokens = word_tokenize(text)
    return tokens

# Function to filter content words
def filter_content_words(word_vector_pairs):
    # Filter out stopwords and words with special characters/digits
    content_pairs = [
        (id_, word, vec) for id_, word, vec in word_vector_pairs
        if word not in stop_words and re.match(r'^[a-z]+$', word)
    ]
    return content_pairs

# Function to get word embeddings with unique IDs
def get_word_embeddings(words, prefix):
    # Generate embeddings for all words
    embeddings = model.encode(words, convert_to_numpy=True)
    # Create unique IDs and return list of (id, word, vector)
    return [(f"{prefix}_{i+1}", word, emb) for i, (word, emb) in enumerate(zip(words, embeddings))]

# Function to compute custom similarity score with best word pairs
def custom_similarity_score(reference, llm_response):
    # Step 1: Tokenize both texts
    ref_words = tokenize_text(reference)
    llm_words = tokenize_text(llm_response)
    
    if not ref_words or not llm_words:
        return 0.0, []  # Return 0 score and empty pairs if no words
    
    # Step 2: Get embeddings for all words
    ref_word_vectors = get_word_embeddings(ref_words, "ref")
    llm_word_vectors = get_word_embeddings(llm_words, "llm")
    
    # Step 3: Filter content words
    ref_content_vectors = filter_content_words(ref_word_vectors)
    llm_content_vectors = filter_content_words(llm_word_vectors)
    
    if not ref_content_vectors or not llm_content_vectors:
        return 0.0, []  # Return 0 score and empty pairs if no content words
    
    # Step 4: Compute pairwise similarities
    similarity_dict = {}
    for ref_id, ref_word, ref_vec in ref_content_vectors:
        similarities = []
        for llm_id, llm_word, llm_vec in llm_content_vectors:
            sim = cosine_similarity([ref_vec], [llm_vec])[0][0]
            similarities.append((llm_id, llm_word, sim))
        # Sort similarities in descending order
        similarities.sort(key=lambda x: x[2], reverse=True)
        similarity_dict[ref_id] = similarities
    print(similarity_dict)
    # Step 5: Find best non-overlapping pairs
    best_pairs = []
    used_llm_ids = set()
    
    while similarity_dict:
        # Collect top pairs for each reference word
        top_pairs = []
        for ref_id, similarities in similarity_dict.items():
            if similarities:  # If there are still LLM words available
                llm_id, llm_word, sim = similarities[0]  # Top similarity
                top_pairs.append((ref_id, llm_id, llm_word, sim))
        
        if not top_pairs:
            break
        
        # Sort top pairs by similarity (descending)
        top_pairs.sort(key=lambda x: x[3], reverse=True)
        
        # Select the best pair
        best_ref_id, best_llm_id, best_llm_word, best_sim = top_pairs[0]
        best_ref_word = next(word for id_, word, _ in ref_content_vectors if id_ == best_ref_id)
        best_pairs.append((best_ref_id, best_ref_word, best_llm_id, best_llm_word, best_sim))
        
        # Remove the used LLM word from all similarity lists
        used_llm_ids.add(best_llm_id)
        for ref_id in similarity_dict:
            similarity_dict[ref_id] = [(llm_id, llm_word, sim) for llm_id, llm_word, sim in similarity_dict[ref_id] if llm_id not in used_llm_ids]
        
        # Remove reference ID if it has no more valid similarities
        if not similarity_dict[best_ref_id]:
            del similarity_dict[best_ref_id]
    
    # Step 6: Handle unpaired reference words (assign similarity 0)
    for ref_id, ref_word, _ in ref_content_vectors:
        if ref_id not in [pair[0] for pair in best_pairs]:
            best_pairs.append((ref_id, ref_word, None, None, 0.0))
    
    # Step 7: Compute final score
    if best_pairs:
        final_score = np.mean([pair[4] for pair in best_pairs])
    else:
        final_score = 0.0
    
    return final_score, best_pairs

if __name__ == "__main__":
    # Example usage
    # Example usage
    Logline_reference = """A compassionate intermediate college teacher, Shiva, recounts the tragic
    story of his best friend Ramu and his girlfriend Asha, who, as teenagers,
    faced the devastating consequences of an unplanned pregnancy,
    highlighting the importance of parental guidance and open
    communication during adolescence."""

    Logline_llm = """In an innocent intermediate college romance framed by a poignant life lesson, a spirited
    young man's lighthearted attempts to win his beloved lead to an unforeseen teenage
    pregnancy, triggering a cascade of desperate choices, family sacrifices, and ultimately,
    a tragic double suicide, leaving their loyal friend to carry forward their devastating
    legacy."""

    # Compute custom similarity score and get best pairs
    score, pairs = custom_similarity_score(Logline_reference, Logline_llm)

    # Print results
    print(f"Custom Similarity Score: {score:.4f}")
    print("\nBest Word Pairs:")
    for ref_id, ref_word, llm_id, llm_word, sim in pairs:
        if llm_id:
            print(f"Reference: {ref_id} ({ref_word}) -> LLM: {llm_id} ({llm_word}), Similarity: {sim:.4f}")
        else:
            print(f"Reference: {ref_id} ({ref_word}) -> No match, Similarity: 0.0000")

    # # Optional: Print content words for debugging
    # ref_content_words = [word for _, word, _ in filter_content_words(get_word_embeddings(tokenize_text(Logline_reference), "ref"))]
    # llm_content_words = [word for _, word, _ in filter_content_words(get_word_embeddings(tokenize_text(Logline_llm), "llm"))]
    # print("\nReference Content Words:", ref_content_words)
    # print("LLM Content Words:", llm_content_words)
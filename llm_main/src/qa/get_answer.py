import chromadb
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import logging
import google.generativeai as genai

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
import openai
import os

from dotenv import load_dotenv
load_dotenv()
openai.api_key = os.getenv("open_ai_key")


class ChromaDBQA:
    def __init__(self, collection_name="pdf_embeddings", db_path="./chroma_db", api_key="your-gemini-api-key-here"):
        """Initialize ChromaDB QA system with Telugu sentence similarity model."""
        self.client = chromadb.PersistentClient(path=db_path)
        # self.collection = self.client.get_or_create_collection(
        #     name=collection_name,
        #     embedding_function=chromadb.utils.embedding_functions.SentenceTransformerEmbeddingFunction(
        #         model_name="l3cube-pune/telugu-sentence-similarity-sbert"
        #     )
        # )
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            embedding_function=None  # Don't use SentenceTransformer inside Chroma
        )
        # self.model = SentenceTransformer('l3cube-pune/telugu-sentence-similarity-sbert')
        genai.configure(api_key=api_key)
        self.llm_model = genai.GenerativeModel("gemini-2.5-flash-preview-05-20")

    def llm_response(self, prompt, sys_prompt="You are a helpful assistant"):
        """Generate response using the LLM."""
        chat = self.llm_model.start_chat(history=[])
        response = chat.send_message(f"{sys_prompt}\n\n{prompt}")
        return response.text

    def search(self, query, top_k=1, source_filter=None):
        """
        Search for relevant chunks in ChromaDB using cosine similarity.
        
        Args:
            query: Search query
            top_k: Number of results to return (default 1 for most relevant)
            source_filter: Optional filter by source file
        
        Returns:
            Dictionary with documents, metadata, and distances
        """
        try:
            # Encode the query
            # query_embedding = self.model.encode([query])[0]
            response = openai.embeddings.create(
                model="text-embedding-3-small",
                input=query
            )

            # Extract embedding vector
            query_embedding = response.data[0].embedding

            # Fetch all documents and their embeddings from the collection
            collection_data = self.collection.get(include=['documents', 'metadatas', 'embeddings'])

            documents = collection_data['documents']
            metadatas = collection_data['metadatas']
            embeddings = collection_data['embeddings']

            if not documents:
                return {'documents': [], 'metadatas': [], 'distances': []}

            # Apply source filter if provided
            if source_filter:
                filtered_indices = [
                    i for i, meta in enumerate(metadatas)
                    if meta.get('source_file') == source_filter
                ]
                if not filtered_indices:
                    return {'documents': [], 'metadatas': [], 'distances': []}
                documents = [documents[i] for i in filtered_indices]
                metadatas = [metadatas[i] for i in filtered_indices]
                embeddings = [embeddings[i] for i in filtered_indices]

            # Calculate cosine similarity between query and document embeddings
            similarities = cosine_similarity([query_embedding], embeddings)[0]

            # Get indices of top-k most similar documents
            top_k_indices = np.argsort(similarities)[::-1][:top_k]

            # Collect top-k results
            top_documents = [documents[i] for i in top_k_indices]
            top_metadatas = [metadatas[i] for i in top_k_indices]
            top_distances = [float(1 - similarities[i]) for i in top_k_indices]  # Convert to distance (1 - similarity)

            return {
                'documents': top_documents,
                'metadatas': top_metadatas,
                'distances': top_distances
            }
        except Exception as e:
            logger.error(f"Error during search: {str(e)}")
            return {'documents': [], 'metadatas': [], 'distances': []}

    def ask(self, question, top_k=1, source_filter=None):
        """
        Ask a question and get an answer based on the most relevant chunks.
        
        Args:
            question: Question to ask
            top_k: Number of relevant chunks to retrieve (default 1)
            source_filter: Optional filter by source file
        
        Returns:
            Dictionary with question, answer, and relevant passages
        """
        search_results = self.search(question, top_k=top_k, source_filter=source_filter)
        relevant_chunks = search_results['documents']
        print('$$$$$$$$$$$$$$$$$$$$$$')
        print('$$$$$$$$$$$$$$$$$$$$$$')
        print(relevant_chunks)
        print('$$$$$$$$$$$$$$$$$$$$$$')
        
        if not relevant_chunks:
            return {
                "question": question,
                "answer": "No relevant information found in the database to answer the question.",
                "relevant_passages": []
            }
        
        # Combine all relevant chunks into the prompt
        context = "\n\n".join([f"Passage {i+1}:\n{chunk}" for i, chunk in enumerate(relevant_chunks)])
        
        # Prepare prompt for LLM
        prompt = f"""
        Based on the following passages from a PDF document, answer the question accurately.
        
        Context:
        {context}
        
        Question: {question}
        
        Instructions:
        - Provide an answer only if the passages contain sufficient information to answer the question.
        - If the passages do not contain enough information to answer the question, respond with: "The information needed to answer this question is not available in the provided passages."
        - Be specific and cite relevant details from the passages.
        - If multiple passages are provided, synthesize the information to provide a comprehensive answer.
        
        Answer:
        """
        
        try:
            answer = self.llm_response(prompt)
        except Exception as e:
            logger.error(f"Error generating answer: {str(e)}")
            answer = f"Error generating response: {str(e)}"
        
        return {
            "question": question,
            "answer": answer,
            "relevant_passages": relevant_chunks
        }


if __name__ == "__main__":

    # Initialize the QA system
    qa_system = ChromaDBQA(
        collection_name="telugu_pdf_embeddings",
        db_path="./chroma_db",
        api_key=os.getenv("api_key_ge")
    )
    
    # Ask a question
    question = "1st year class room ki evaru vacharu , valla peru enti"
    result = qa_system.ask(question, top_k=1)
    
    # Print results
    print(f"Question: {result['question']}")
    print(f"Answer: {result['answer']}")
    print(f"Relevant Passage: {result.get('relevant_passage', '')}")
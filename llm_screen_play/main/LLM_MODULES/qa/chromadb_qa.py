import chromadb
from sentence_transformers import SentenceTransformer
# import google.generativeai as genai
from llama_index.core import SimpleDirectoryReader
import logging
import os

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PDFChromaQASystem:
    def __init__(self, collection_name="pdf_qa", api_key="your-api-key"):
        """Initialize the PDF QA System with ChromaDB"""
        self.client = chromadb.PersistentClient(path="./chroma_db")
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            embedding_function=chromadb.utils.embedding_functions.SentenceTransformerEmbeddingFunction(
                model_name="all-MiniLM-L6-v2"
            )
        )
        # genai.configure(api_key=api_key)
        # self.gemini_model = genai.GenerativeModel('gemini-pro')
        self.processed_files = set()
    
    def chunk_documents(self, documents, chunk_size=1000, overlap=200):
        """
        Chunk documents into smaller pieces for better retrieval.
        
        Args:
            documents: List of documents from SimpleDirectoryReader
            chunk_size: Maximum characters per chunk
            overlap: Characters to overlap between chunks
        
        Returns:
            List of text chunks
        """
        chunks = []
        
        for doc_idx, doc in enumerate(documents):
            text = doc.text
            doc_metadata = getattr(doc, 'metadata', {})
            
            # Split text into chunks
            start = 0
            chunk_idx = 0
            
            while start < len(text):
                end = start + chunk_size
                chunk_text = text[start:end]
                
                # Try to break at sentence boundary
                if end < len(text):
                    last_period = chunk_text.rfind('.')
                    last_newline = chunk_text.rfind('\n')
                    break_point = max(last_period, last_newline)
                    
                    if break_point > chunk_size * 0.7:  # Don't break too early
                        end = start + break_point + 1
                        chunk_text = text[start:end]
                
                if chunk_text.strip():  # Only add non-empty chunks
                    chunk_metadata = {
                        'doc_index': doc_idx,
                        'chunk_index': chunk_idx,
                        'start_char': start,
                        'end_char': end,
                        **doc_metadata
                    }
                    
                    chunks.append({
                        'text': chunk_text.strip(),
                        'metadata': chunk_metadata
                    })
                    chunk_idx += 1
                
                start = end - overlap
        
        return chunks
    
    def load_pdf(self, pdf_file_path):
        """
        Load PDF and add to ChromaDB collection
        
        Args:
            pdf_file_path: Path to the PDF file
        """
        if not os.path.exists(pdf_file_path):
            raise FileNotFoundError(f"PDF file not found: {pdf_file_path}")
        
        # Check if already processed
        file_key = os.path.abspath(pdf_file_path)
        if file_key in self.processed_files:
            logger.info(f"PDF already processed: {pdf_file_path}")
            return
        
        logger.info("Loading PDF...")
        try:
            documents = SimpleDirectoryReader(input_files=[pdf_file_path]).load_data()
            logger.info(f"Loaded {len(documents)} documents")
        except Exception as e:
            logger.error(f"Error loading PDF: {str(e)}")
            raise
        
        # Chunk documents
        logger.info("Chunking documents...")
        chunks = self.chunk_documents(documents)
        logger.info(f"Created {len(chunks)} chunks")
        
        # Add to ChromaDB
        self.add_chunks_to_db(chunks, pdf_file_path)
        self.processed_files.add(file_key)
    
    def add_chunks_to_db(self, chunks, source_file):
        """Add chunks to ChromaDB collection"""
        if not chunks:
            logger.warning("No chunks to add to database")
            return
        
        texts = []
        metadatas = []
        ids = []
        
        for i, chunk in enumerate(chunks):
            chunk_id = f"{os.path.basename(source_file)}_chunk_{i}"
            
            texts.append(chunk['text'])
            
            # Prepare metadata for ChromaDB
            metadata = chunk.get('metadata', {})
            metadata['source_file'] = source_file
            metadata['chunk_id'] = chunk_id
            metadatas.append(metadata)
            
            ids.append(chunk_id)
        
        try:
            # Add to ChromaDB collection
            self.collection.add(
                documents=texts,
                metadatas=metadatas,
                ids=ids
            )
            logger.info(f"Added {len(texts)} chunks to ChromaDB from {source_file}")
        except Exception as e:
            logger.error(f"Error adding chunks to database: {str(e)}")
            raise
    
    def search(self, query, top_k=5, source_filter=None):
        """
        Search for relevant chunks
        
        Args:
            query: Search query
            top_k: Number of results to return
            source_filter: Optional filter by source file
        
        Returns:
            List of relevant text chunks
        """
        try:
            # Build where clause for filtering
            where_clause = {}
            if source_filter:
                where_clause["source_file"] = {"$eq": source_filter}
            
            # Query ChromaDB
            if where_clause:
                results = self.collection.query(
                    query_texts=[query],
                    n_results=top_k,
                    where=where_clause
                )
            else:
                results = self.collection.query(
                    query_texts=[query],
                    n_results=top_k
                )
            
            return {
                'documents': results['documents'][0] if results['documents'] else [],
                'metadatas': results['metadatas'][0] if results['metadatas'] else [],
                'distances': results['distances'][0] if results['distances'] else []
            }
        
        except Exception as e:
            logger.error(f"Error during search: {str(e)}")
            return {'documents': [], 'metadatas': [], 'distances': []}
    
    def ask(self, question, top_k=5, source_filter=None, include_metadata=False):
        """
        Ask a question and get an answer based on the PDF content
        
        Args:
            question: Question to ask
            top_k: Number of relevant chunks to retrieve
            source_filter: Optional filter by source file
            include_metadata: Whether to include chunk metadata in response
        
        Returns:
            Dictionary with answer and relevant passages
        """
        search_results = self.search(question, top_k=top_k, source_filter=source_filter)
        print(search_results['documents'])
        print(search_results['distances'])
        exit('PLLLLLLLLLLLLLLLLLLLLL')
        relevant_chunks = search_results['documents']
        
        if not relevant_chunks:
            return {
                "question": question,
                "answer": "I couldn't find any relevant information in the PDF to answer your question.",
                "relevant_passages": [],
                "metadata": []
            }
        
        # Create context from relevant chunks
        context = "\n\n".join([f"Passage {i+1}:\n{chunk}" 
                              for i, chunk in enumerate(relevant_chunks)])
        
        prompt = f"""
        Based on the following passages from a PDF document, answer the question accurately and comprehensively.
        
        Context:
        {context}
        
        Question: {question}
        
        Instructions:
        - Provide a detailed answer based only on the information in the context
        - If the answer cannot be found in the context, say "The information needed to answer this question is not available in the provided text"
        - Be specific and cite relevant details from the passages
        - If multiple passages contain relevant information, synthesize them in your answer
        
        Answer:
        """
        
        try:
            response = self.gemini_model.generate_content(prompt)
            answer = response.text
        except Exception as e:
            logger.error(f"Error generating answer: {str(e)}")
            answer = f"Error generating response: {str(e)}"
        
        result = {
            "question": question,
            "answer": answer,
            "relevant_passages": relevant_chunks
        }
        
        if include_metadata:
            result["metadata"] = search_results['metadatas']
            result["similarity_scores"] = search_results['distances']
        
        return result
    
    def get_collection_info(self):
        """Get information about the current collection"""
        try:
            count = self.collection.count()
            return {
                "total_chunks": count,
                "processed_files": list(self.processed_files)
            }
        except Exception as e:
            logger.error(f"Error getting collection info: {str(e)}")
            return {"total_chunks": 0, "processed_files": []}
    
    def clear_collection(self):
        """Clear all data from the collection"""
        try:
            # Delete the collection and recreate it
            self.client.delete_collection(self.collection.name)
            self.collection = self.client.get_or_create_collection(
                name=self.collection.name,
                embedding_function=chromadb.utils.embedding_functions.SentenceTransformerEmbeddingFunction(
                    model_name="all-MiniLM-L6-v2"
                )
            )
            self.processed_files.clear()
            logger.info("Collection cleared successfully")
        except Exception as e:
            logger.error(f"Error clearing collection: {str(e)}")

# Usage Example
if __name__ == "__main__":
    # Initialize the QA system
    qa_system = PDFChromaQASystem(
        collection_name="my_pdf_qa",
        api_key="your-gemini-api-key-here"
    )
    
    # Load a PDF
    pdf_path = "/home/ntlpt19/Downloads/Thella Kaagitham Full Script.pdf"
    qa_system.load_pdf(pdf_path)
    
    # Check collection info
    info = qa_system.get_collection_info()
    print(f"Collection info: {info}")
    
    # Ask questions
    questions = [
        "MURTHY uncle Eammaa…?, Anagaane Asha shock ayyi slip enduku kindha padesindhi. ??",
    ]
    
    for question in questions:
        result = qa_system.ask(question, top_k=5, include_metadata=True)
        print(f"\nQ: {result['question']}")
        print(f"A: {result['answer']}")
        print(f"Sources: {len(result['relevant_passages'])} passages found")
        print("-" * 80)
    
    # You can also filter by source file if you have multiple PDFs
    # result = qa_system.ask("Your question", source_filter="path/to/specific/file.pdf")
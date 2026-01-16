import chromadb
from sentence_transformers import SentenceTransformer
from llama_index.core import SimpleDirectoryReader
import logging
import os
import uuid

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
import openai

from dotenv import load_dotenv
load_dotenv()
openai.api_key = os.getenv("open_ai_key")



class PDFToChromaDB:
    def __init__(self, collection_name="pdf_embeddings", db_path="./chroma_db"):
        """Initialize ChromaDB with Telugu sentence similarity model."""
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
            
            start = 0
            chunk_idx = 0
            while start < len(text):
                end = start + chunk_size
                chunk_text = text[start:end]
                
                if end < len(text):
                    last_period = chunk_text.rfind('.')
                    last_newline = chunk_text.rfind('\n')
                    break_point = max(last_period, last_newline)
                    if break_point > chunk_size * 0.7:
                        end = start + break_point + 1
                        chunk_text = text[start:end]
                
                if chunk_text.strip():
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
        Load PDF and add embeddings to ChromaDB collection.
        
        Args:
            pdf_file_path: Path to the PDF file
        """
        if not os.path.exists(pdf_file_path):
            raise FileNotFoundError(f"PDF file not found: {pdf_file_path}")
        
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
        
        logger.info("Chunking documents...")
        chunks = self.chunk_documents(documents)
        logger.info(f"Created {len(chunks)} chunks")
        
        self.add_chunks_to_db(chunks, pdf_file_path)
        self.processed_files.add(file_key)

    def add_chunks_to_db(self, chunks, source_file):
        """Add chunks and their embeddings to ChromaDB collection."""
        if not chunks:
            logger.warning("No chunks to add to database")
            return
        
        texts = []
        metadatas = []
        ids = []
        
        for i, chunk in enumerate(chunks):
            chunk_id = f"{os.path.basename(source_file)}_chunk_{i}"
            texts.append(chunk['text'])
            metadata = chunk.get('metadata', {})
            metadata['source_file'] = source_file
            metadata['chunk_id'] = chunk_id
            metadatas.append(metadata)
            ids.append(chunk_id)
        
        try:
            response = openai.embeddings.create(
                model="text-embedding-3-small",
                input=texts  # batch of chunk texts
            )
            openai_embeddings = [item.embedding for item in response.data]

            # self.collection.add(
            #     documents=texts,
            #     metadatas=metadatas,
            #     ids=ids
            # )
            self.collection.add(
                documents=texts,
                metadatas=metadatas,
                ids=ids,
                embeddings=openai_embeddings  # <--- Provide your own embeddings
            )
            logger.info(f"Added {len(texts)} chunks to ChromaDB from {source_file}")
        except Exception as e:
            logger.error(f"Error adding chunks to database: {str(e)}")
            raise

    def get_collection_info(self):
        """Get information about the current collection."""
        try:
            count = self.collection.count()
            return {
                "total_chunks": count,
                "processed_files": list(self.processed_files)
            }
        except Exception as e:
            logger.error(f"Error getting collection info: {str(e)}")
            return {"total_chunks": 0, "processed_files": []}

if __name__ == "__main__":
    # Initialize the PDF to ChromaDB processor
    pdf_processor = PDFToChromaDB(collection_name="telugu_pdf_embeddings")
    # Load a PDF
    pdf_path = "/home/ntlpt19/Downloads/Thella Kaagitham Full Script.pdf"
    pdf_processor.load_pdf(pdf_path)
    
    # Check collection info
    info = pdf_processor.get_collection_info()
    print(f"Collection info: {info}")
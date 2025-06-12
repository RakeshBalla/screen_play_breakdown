import streamlit as st
import os
import shutil
from get_answer import ChromaDBQA
from dump_data import PDFToChromaDB

# Set page configuration
st.set_page_config(page_title="STORY QA SYSTEM", page_icon="📚", layout="wide")

# Streamlit UI
st.title("STORY Question Answering System")
st.markdown("Upload a PDF to process into the database and ask questions about the story.")

# PDF Upload Section
st.subheader("Upload PDF")
uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])

# Initialize session state for QA system
if 'qa_system' not in st.session_state:
    st.session_state.qa_system = None

# Button to process PDF
if st.button("Process PDF"):
    if uploaded_file is not None:
        try:
            # Save uploaded file temporarily
            pdf_path = os.path.join("temp_pdf", uploaded_file.name)
            os.makedirs("temp_pdf", exist_ok=True)
            with open(pdf_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            # Delete existing chroma_db folder
            db_path = "./chroma_db"
            if os.path.exists(db_path):
                shutil.rmtree(db_path)
                st.info("Existing chroma_db folder deleted.")
            
            # Initialize PDF processor and load PDF
            pdf_processor = PDFToChromaDB(collection_name="telugu_pdf_embeddings")
            pdf_processor.load_pdf(pdf_path)
            
            # Check collection info
            info = pdf_processor.get_collection_info()
            st.success(f"PDF processed successfully! Collection info: {info}")
            
            # Initialize QA system
            st.session_state.qa_system = ChromaDBQA(
                collection_name="telugu_pdf_embeddings",
                db_path="./chroma_db",
                api_key=os.getenv("api_key_ge")
            )
            
            # Clean up temporary file
            os.remove(pdf_path)
            
        except Exception as e:
            st.error(f"Error processing PDF: {str(e)}")
    else:
        st.warning("Please upload a PDF file.")

# Question Answering Section
st.subheader("Ask a Question")
question = st.text_input("Your Question:", placeholder="E.g., 1st year class room ki evaru vacharu, valla peru enti")

# Button to submit question
if st.button("Get Answer"):
    if question.strip():
        if st.session_state.qa_system:
            try:
                # Call the QA system
                result = st.session_state.qa_system.ask(question, top_k=1)
                
                # Display results
                st.subheader("Results")
                st.write(f"**Question:** {result['question']}")
                st.write(f"**Answer:** {result['answer']}")
                st.write(f"**Relevant Passage:** {result.get('relevant_passage', 'No passage available')}")
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
        else:
            st.error("QA system not initialized. Please process a PDF first.")
    else:
        st.warning("Please enter a valid question.")

# Add some styling
st.markdown("""
    <style>
    .stTextInput > div > div > input {
        border-radius: 8px;
        padding: 10px;
    }
    .stButton > button {
        background-color: #4CAF50;
        color: white;
        border-radius: 8px;
        padding: 10px 20px;
    }
    .stButton > button:hover {
        background-color: #45a049;
    }
    .stFileUploader > div > div {
        border-radius: 8px;
        padding: 10px;
    }
    </style>
""", unsafe_allow_html=True)
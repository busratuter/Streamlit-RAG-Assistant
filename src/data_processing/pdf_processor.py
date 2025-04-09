import glob
import streamlit as st
from pathlib import Path
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.embeddings import HuggingFaceEmbeddings

from src.config.settings import (
    PDF_DIRECTORY, 
    CHUNK_SIZE, 
    CHUNK_OVERLAP, 
    VECTOR_DB_PATH,
    EMBEDDING_MODEL_NAME
)

def get_pdf_files():
    """PDF dosyalarını bul ve listele"""
    return glob.glob(f"{PDF_DIRECTORY}/*.pdf")

def load_documents(pdf_files):
    """PDF dosyalarını yükle ve belgeleri döndür"""
    documents = []
    file_names = []
    
    for pdf_path in pdf_files:
        try:
            loader = PyPDFLoader(pdf_path)
            pdf_documents = loader.load()
            documents.extend(pdf_documents)
            file_name = Path(pdf_path).name
            file_names.append(file_name)
            # İşlenen dosya adlarını kaydet
            if "processed_files" not in st.session_state:
                st.session_state.processed_files = set()
            st.session_state.processed_files.add(file_name)
        except Exception as e:
            st.error(f"PDF yüklenirken hata oluştu {pdf_path}: {str(e)}")
    
    return documents, file_names

def split_documents(documents):
    """Belgeleri küçük parçalara böl"""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        length_function=len
    )
    return text_splitter.split_documents(documents)

def create_vectorstore(chunks):
    """Metin parçalarından vektör veritabanı oluştur"""
    embedding_model = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME)
    
    return Chroma.from_documents(
        documents=chunks,
        embedding=embedding_model,
        persist_directory=VECTOR_DB_PATH
    )

def process_pdfs():
    """PDF dosyalarını işle ve vektör veritabanını döndür"""
    pdf_files = get_pdf_files()
    
    if not pdf_files:
        st.warning(f"'{PDF_DIRECTORY}' klasöründe hiç PDF dosyası bulunamadı. Lütfen PDF dosyalarınızı yükleyin.")
        return None, []
    
    documents, file_names = load_documents(pdf_files)
    chunks = split_documents(documents)
    vectorstore = create_vectorstore(chunks)
    
    return vectorstore, file_names 
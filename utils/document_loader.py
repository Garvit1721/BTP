import os
from typing import List
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

def load_and_split_pdfs(pdf_paths: List[str]):
    documents = []
    for path in pdf_paths:
        if not os.path.exists(path):
            print(f"Warning: File not found at {path}")
            continue
        loader = PyPDFLoader(path)
        documents.extend(loader.load())

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    split_docs = text_splitter.split_documents(documents)
    return split_docs

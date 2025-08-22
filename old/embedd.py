# embedd.py
import os
from typing import List
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores.pgvector import PGVector
from langchain_core.documents import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter

def embed_documents(file_paths: List[str]):
    CONNECTION_STRING = "postgresql://lovemeplease@localhost:5432/embedding"
    COLLECTION_NAME = "long_paragraphs"
    MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    embeddings = HuggingFaceEmbeddings(model_name=MODEL_NAME)
    vectorstore = PGVector(
        connection_string=CONNECTION_STRING,
        collection_name=COLLECTION_NAME,
        embedding_function=embeddings
    )

    documents = []
    for path in file_paths:
        if not path.endswith(".txt") or not os.path.exists(path):
            print(f"Skipping invalid file: {path}")
            continue

        with open(path, "r") as f:
            content = f.read()
        filename = os.path.basename(path)
        chunks = splitter.split_text(content)
        print(filename)
        docs = [Document(page_content=c, metadata={"source": filename, "chunk": i}) for i, c in enumerate(chunks)]
        documents.extend(docs)

    if not documents:
        print("No valid documents to insert.")
        return

    existing = vectorstore.similarity_search("artificial intelligence", k=1)
    if existing and any(e.metadata.get("source") in [doc.metadata["source"] for doc in documents] for e in existing):
        print("Some documents already embedded. Skipping insertion.")
    else:
        print(f" Inserting {len(documents)} chunks...")
        PGVector.from_documents(
            documents=documents,
            embedding=embeddings,
            connection_string=CONNECTION_STRING,
            collection_name=COLLECTION_NAME
        )
        print("Embedding complete.")

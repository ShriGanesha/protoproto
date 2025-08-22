import os
from typing import List
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores.pgvector import PGVector
from langchain_core.documents import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
import psycopg2

from model.constants import CONNECTION_STRING, EMBEDDING_MODEL, DB_NAME, DB_USER, DB_HOST, DB_PORT


def embed_documents(file_paths: List[str]):
    COLLECTION_NAME = "long_paragraphs"

    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
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

def execute_query(target_file_name: str, sql_file_name: str):
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        host=DB_HOST,
        port=DB_PORT
    )
    cur = conn.cursor()

    with open(sql_file_name, "r") as f:
        sql_script = f.read()

    try:
        print("here")
        cur.execute(sql_script)

        res = []

        if sql_script.strip().lower().startswith("select"):
            rows = cur.fetchall()
            print("Query result:")
            for row in rows:
                print(row[3])
                if target_file_name == row[3]["source"]:
                    res.append(row)
                elif target_file_name == "":
                    res.append(row)

        else:
            conn.commit()
            print("Script executed successfully.")

        return res

    except Exception as e:
        print("Error executing SQL:", e)

    finally:
        cur.close()
        conn.close()

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores.pgvector import PGVector

CONNECTION_STRING = "postgresql://lovemeplease@localhost:5432/embedding"
COLLECTION_NAME = "long_paragraphs"
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

embeddings = HuggingFaceEmbeddings(model_name=MODEL_NAME)

vectorstore = PGVector(
    connection_string=CONNECTION_STRING,
    collection_name=COLLECTION_NAME,
    embedding_function=embeddings
)

query = "How has artificial intelligence evolved?"
results = vectorstore.similarity_search(query, k=1)

print(results)
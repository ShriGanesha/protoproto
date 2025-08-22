# main.py
from old.embedd import embed_documents
from summarize import summarize_documents

if __name__ == "__main__":
    folder = "documents"
    embed_documents([
        "documents/tom_case.txt"
    ])
    summarize_documents("tom_case.txt")
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores.pgvector import PGVector
from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

def summarize_documents(source_filenames: list[str]) -> list[dict[str, str]]:
    CONNECTION_STRING = "postgresql://lovemeplease@localhost:5432/embedding"
    COLLECTION_NAME = "long_paragraphs"
    EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
    LLM_MODEL = "llama3"

    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    vectorstore = PGVector(
        connection_string=CONNECTION_STRING,
        collection_name=COLLECTION_NAME,
        embedding_function=embeddings
    )

    prompt_template = PromptTemplate.from_template("""
You are a clinical summarizer.

Based on the following patient notes, write a clear and medically accurate case summary:

{context}

Summary:
""")

    llm = Ollama(model=LLM_MODEL, temperature=0)
    chain = LLMChain(llm=llm, prompt=prompt_template)

    summaries: list[dict[str, str]] = []

    for source_filename in source_filenames:
        print(f"Searching for document: {source_filename}")

        retrieved_docs = []
        try:
            retrieved_docs = vectorstore.similarity_search_with_score(
                "summarize the patient",
                k=50,
                filter={"source": source_filename}
            )
        except TypeError:
            retrieved = vectorstore.similarity_search("summarize the patient", k=1000)
            retrieved_docs = [(doc, 0.0) for doc in retrieved if doc.metadata.get("source") == source_filename]

        target_docs = [doc for doc, _ in retrieved_docs if doc.metadata.get("source") == source_filename]

        if not target_docs:
            print(f"No chunks found for {source_filename}")
            summaries.append({"name": source_filename, "summary": ""})
            continue

        context = "\n\n".join(doc.page_content for doc in target_docs)
        summary_text = chain.run(context=context).strip()

        summaries.append({
            "name": source_filename,
            "summary": summary_text
        })

    return summaries
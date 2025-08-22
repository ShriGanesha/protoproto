from fastapi import FastAPI, HTTPException

from model.models import EmbedRequest, SummarizeRequest, ViewEmbedRequest, EmbedAndSummarizeRequest
from services.bioBart_service import bio_bart_summarize
from services.embed_service import embed_documents, execute_query
from services.summarize_service import summarize_documents

app = FastAPI(title="Medical Embedding & Summarization API")

@app.post("/embed")
def embed_endpoint(request: EmbedRequest):
    try:
        embed_documents(request.files)
        return {"status": f"Embedded {len(request.files)} file(s)."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Embedding failed: {str(e)}")

@app.post("/summarize")
def summarize_endpoint(request: SummarizeRequest):
    try:
        summary = summarize_documents(request.files)
        return summary
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Embedding failed: {str(e)}")

@app.post("/view-embed")
def view_embed(request: ViewEmbedRequest):
    result = execute_query(request.fileName, "script/view_embed.sql")
    return {
        "results": result
    }

@app.delete("/delete-embed")
def view_embed():
    result = execute_query("", "script/delete_embed.sql")
    return {
        "results": result
    }

@app.post("/embed-summarize")
def view_embed(request: EmbedAndSummarizeRequest):
    embed_documents(request.files)

    file_list = []

    for file in request.files:
        file_list.append(file.split("/")[1])

    summary = summarize_documents(file_list)
    return summary

@app.post("/bio-bart-summarize")
def bio_bart_summarizee(request: EmbedAndSummarizeRequest):
    return bio_bart_summarize(request.files)

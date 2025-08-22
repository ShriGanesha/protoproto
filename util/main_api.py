from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from old.embedd import embed_documents
from summarize import summarize_documents
from old.execute_script import delete
from old.execute_script import viewEmbed
from old.execute_script import viewEmbedForFile
app = FastAPI(title="Medical Embedding & Summarization API")


class EmbedRequest(BaseModel):
    files: list[str]

class MultiFileRequest(BaseModel):
    files: list[str]

@app.post("/embed")
def embed_endpoint(request: EmbedRequest):
    try:
        embed_documents(request.files)
        return {"status": f"Embedded {len(request.files)} file(s)."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Embedding failed: {str(e)}")


@app.get("/summarize/{filename}")
def summarize_endpoint(filename: str):
    try:
        print(filename)
        summary = summarize_documents(filename)
        # summary = clean_summary_text(summary)
        print(summary)
        # if summary is None:
        #     raise HTTPException(status_code=404, detail="Document not found or not embedded.")
        return {
            "source": filename,
            "summary": summary
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Summarization failed: {str(e)}")







@app.post("/embed-and-summarize")
def embed_and_summarize_endpoint(request: EmbedRequest):
    embed_documents(request.files)
    summary = summarize_documents(request.files[0])
    return {
        "source": request.files[0],
        "summary": summary
    }

@app.delete("/delete-embed")
def embed_and_summarize_endpoint():
    delete()

@app.get("/view-embed")
def viewEmbed():
    result = viewEmbed()
    return {
        "results": result
    }

@app.get("/view-embed/{filename}")
def viewembedForFile(filename: str):
    result = viewEmbedForFile(filename)
    return {
        "result": result
    }
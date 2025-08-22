from pydantic import BaseModel

class EmbedRequest(BaseModel):
    files: list[str]

class ViewEmbedRequest(BaseModel):
    fileName: str

class SummarizeRequest(BaseModel):
    files: list[str]

class MultiFileRequest(BaseModel):
    files: list[str]

class EmbedAndSummarizeRequest(BaseModel):
    files: list[str]
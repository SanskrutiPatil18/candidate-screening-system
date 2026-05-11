from fastapi import APIRouter, UploadFile
import fitz  # PyMuPDF for PDF parsing

router = APIRouter()

@router.post("/upload")
async def upload_resume(file: UploadFile):
    text = ""
    if file.filename.endswith(".pdf"):
        pdf = fitz.open(stream=await file.read(), filetype="pdf")
        for page in pdf:
            text += page.get_text()
    return {"resume_text": text}


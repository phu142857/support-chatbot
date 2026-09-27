import shutil
from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, File, HTTPException, UploadFile

from app.services.embedding.embedding_service import EmbeddingService
from app.services.extraction.extraction_service import ExtractionService
from app.services.milvus.milvus_service import MilvusService
from app.services.milvus.retrieval_service import RetrievalService
from app.services.ocr.ocr_service import OCRService


router = APIRouter(
    prefix="/api/chat",
    tags=["Chat"],
)

ocr_service = OCRService()
extraction_service = ExtractionService()

embedding_service = EmbeddingService()
milvus_service = MilvusService()

retrieval_service = RetrievalService(
    embedding_service=embedding_service,
    milvus_service=milvus_service,
)

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

ALLOWED_CONTENT_TYPES = {
    "image/png",
    "image/jpeg",
    "image/webp",
}


@router.post("/screenshot")
async def upload_screenshot(
    file: UploadFile = File(...),
):
    if file.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(
            status_code=400,
            detail="Only PNG, JPEG, and WebP images are supported.",
        )

    extension = Path(file.filename or "").suffix.lower()

    if not extension:
        extension = ".png"

    file_name = f"{uuid4()}{extension}"
    file_path = UPLOAD_DIR / file_name

    try:
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        extracted_text = ocr_service.extract_text(
            str(file_path)
        )

        extracted_information = extraction_service.extract(
            extracted_text
        )

        knowledge_results = retrieval_service.search(
            error_code=extracted_information["error_code"],
            error_message=extracted_information["error_message"],
        )

        return {
            "file_name": file.filename,
            "extracted_text": extracted_text,
            "extracted_information": extracted_information,
            "knowledge_results": knowledge_results,
        }

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Screenshot processing failed: {exc}",
        ) from exc

    finally:
        file.file.close()
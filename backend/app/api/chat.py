import shutil
from pathlib import Path
from uuid import uuid4

from app.services.extraction.extraction_service import ExtractionService

from fastapi import APIRouter, File, HTTPException, UploadFile

from app.services.ocr.ocr_service import OCRService


router = APIRouter(
    prefix="/api/chat",
    tags=["Chat"],
)

ocr_service = OCRService()
extraction_service = ExtractionService()

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

        return {
            "file_name": file.filename,
            "extracted_text": extracted_text,
            "extracted_information": extracted_information,
        }

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"OCR processing failed: {exc}",
        ) from exc

    finally:
        file.file.close()
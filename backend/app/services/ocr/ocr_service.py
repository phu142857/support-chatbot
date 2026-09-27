from pathlib import Path

from paddleocr import PaddleOCR


class OCRService:
    def __init__(self) -> None:
        self._ocr = PaddleOCR(
            lang="en",
            enable_mkldnn=False,
        )

    def extract_text(self, image_path: str) -> str:
        path = Path(image_path)

        if not path.exists():
            raise FileNotFoundError(
                f"Image not found: {image_path}"
            )

        result = self._ocr.predict(str(path))

        extracted_lines: list[str] = []

        for page in result:
            data = page.json

            if not data:
                continue

            res = data.get("res", {})
            texts = res.get("rec_texts", [])

            for text in texts:
                if text and text.strip():
                    extracted_lines.append(text.strip())

        return "\n".join(extracted_lines)
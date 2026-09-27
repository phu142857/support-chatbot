import re


class ExtractionService:
    ERROR_CODE_PATTERNS = [
        re.compile(
            r"\b(?:error\s*(?:code)?|code)\s*[:#-]?\s*([A-Z0-9_-]+)\b",
            re.IGNORECASE,
        ),
        re.compile(
            r"\b(HTTP\s*)?(4\d{2}|5\d{2})\b",
            re.IGNORECASE,
        ),
    ]

    ERROR_MESSAGE_PATTERNS = [
        re.compile(
            r"\b(?:error|message)\s*[:#-]\s*(.+)",
            re.IGNORECASE,
        ),
    ]

    def extract(self, text: str) -> dict[str, str | None]:
        normalized_text = self._normalize_text(text)

        error_code = self._extract_error_code(normalized_text)
        error_message = self._extract_error_message(
            normalized_text,
            error_code,
        )

        return {
            "error_code": error_code,
            "error_message": error_message,
            "raw_text": normalized_text,
        }

    @staticmethod
    def _normalize_text(text: str) -> str:
        lines = []

        for line in text.splitlines():
            line = line.strip()

            if line:
                lines.append(line)

        return "\n".join(lines)

    def _extract_error_code(self, text: str) -> str | None:
        for pattern in self.ERROR_CODE_PATTERNS:
            match = pattern.search(text)

            if match:
                groups = match.groups()

                for group in reversed(groups):
                    if group:
                        return group.strip()

        return None

    def _extract_error_message(
        self,
        text: str,
        error_code: str | None,
    ) -> str | None:
        for pattern in self.ERROR_MESSAGE_PATTERNS:
            match = pattern.search(text)

            if match:
                return match.group(1).strip()

        lines = text.splitlines()

        for line in lines:
            if error_code and error_code in line:
                continue

            if line.lower().startswith((">", "{", "}", '"')):
                continue

            if line.strip():
                return line.strip()

        return None
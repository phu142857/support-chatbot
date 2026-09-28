from openai import OpenAI

from app.config.settings import settings


class OpenAIClient:
    def __init__(self) -> None:
        endpoint = settings.azure_openai_endpoint.rstrip("/")

        if not endpoint.endswith("/openai/v1"):
            endpoint = f"{endpoint}/openai/v1"

        self.client = OpenAI(
            api_key=settings.azure_openai_api_key,
            base_url=f"{endpoint}/",
        )

        self.chat_deployment = (
            settings.azure_openai_chat_deployment
        )

        self.embedding_deployment = (
            settings.azure_openai_embedding_deployment
        )


openai_client = OpenAIClient()
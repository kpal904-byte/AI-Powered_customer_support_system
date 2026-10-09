from groq import Groq

from src.config.settings import settings


class LLMClient:
    """
    Client for interacting with a Groq-hosted LLM.
    """

    def __init__(self):
        if not settings.GROQ_API_KEY:
            raise ValueError(
                "GROQ_API_KEY is missing. "
                "Add it to the .env file."
            )

        self.client = Groq(
            api_key=settings.GROQ_API_KEY
        )

        self.model = settings.GROQ_MODEL

    def generate(
        self,
        prompt: str,
        temperature: float = 0.1,
        max_tokens: int = 500
    ) -> str:
        """
        Generate a response from the LLM.
        """

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a professional customer "
                        "support assistant."
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=temperature,
            max_completion_tokens=max_tokens,
        )

        return response.choices[0].message.content.strip()


if __name__ == "__main__":

    llm = LLMClient()

    response = llm.generate(
        "Explain what a refund is in one sentence."
    )

    print("\nModel:", llm.model)
    print("LLM Response:")
    print(response)
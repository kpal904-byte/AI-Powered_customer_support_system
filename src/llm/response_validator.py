import re


class ResponseValidator:
    """
    Basic validation layer for LLM-generated answers.
    """

    def __init__(
        self,
        min_context_words: int = 2
    ):
        self.min_context_words = min_context_words

    @staticmethod
    def _normalize(text: str) -> list[str]:
        """
        Convert text into normalized words.
        """

        text = text.lower()

        words = re.findall(
            r"\b[a-zA-Z0-9]+\b",
            text
        )

        return words

    def validate(
        self,
        answer: str,
        context: str
    ) -> dict:
        """
        Perform a basic groundedness check.
        """

        answer_words = set(
            self._normalize(answer)
        )

        context_words = set(
            self._normalize(context)
        )

        overlap = answer_words.intersection(
            context_words
        )

        overlap_count = len(overlap)

        passed = (
            overlap_count >= self.min_context_words
        )

        return {
            "passed": passed,
            "overlap_count": overlap_count,
            "overlap_words": sorted(overlap),
        }


if __name__ == "__main__":

    validator = ResponseValidator()

    context = """
    Approved refunds are normally processed within
    5 to 7 business days.
    """

    answer = """
    Approved refunds normally take 5 to 7 business days.
    """

    result = validator.validate(
        answer,
        context
    )

    print(result)
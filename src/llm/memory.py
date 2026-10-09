from collections import defaultdict


class ConversationMemory:
    """
    Simple in-memory conversation history.

    Each customer/conversation gets its own message history.
    """

    def __init__(self, max_messages: int = 10):
        self.max_messages = max_messages
        self._history = defaultdict(list)

    def add_message(
        self,
        conversation_id: str,
        role: str,
        content: str
    ) -> None:
        """
        Add a message to a conversation.
        """

        self._history[conversation_id].append(
            {
                "role": role,
                "content": content
            }
        )

        # Keep only the latest messages
        self._history[conversation_id] = (
            self._history[conversation_id][-self.max_messages:]
        )

    def get_history(
        self,
        conversation_id: str
    ) -> list[dict]:
        """
        Return conversation history.
        """

        return self._history.get(
            conversation_id,
            []
        )

    def clear(
        self,
        conversation_id: str
    ) -> None:
        """
        Clear a conversation.
        """

        self._history.pop(
            conversation_id,
            None
        )

    def format_history(
        self,
        conversation_id: str
    ) -> str:
        """
        Convert conversation history into text.
        """

        history = self.get_history(
            conversation_id
        )

        if not history:
            return "No previous conversation."

        lines = []

        for message in history:
            role = message["role"].upper()
            content = message["content"]

            lines.append(
                f"{role}: {content}"
            )

        return "\n".join(lines)


if __name__ == "__main__":

    memory = ConversationMemory()

    memory.add_message(
        "C100",
        "user",
        "I want a refund."
    )

    memory.add_message(
        "C100",
        "assistant",
        "Sure. Please provide your order number."
    )

    memory.add_message(
        "C100",
        "user",
        "My order number is ORD12345."
    )

    print(
        memory.format_history("C100")
    )
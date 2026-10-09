from src.config.settings import settings
from src.llm.llm_client import LLMClient
from src.llm.memory import ConversationMemory
from src.llm.prompts import build_rag_prompt
from src.llm.response_validator import ResponseValidator
from src.rag.retriever import Retriever


class RAGPipeline:
    """
    Complete RAG customer-support pipeline.
    """

    def __init__(self):

        self.retriever = Retriever(
            top_k=settings.TOP_K
        )

        self.llm = LLMClient()

        self.memory = ConversationMemory(
            max_messages=10
        )

        self.validator = ResponseValidator()

    def retrieve_context(
        self,
        query: str
    ) -> list[dict]:

        return self.retriever.retrieve(
            query
        )

    def build_context(
        self,
        documents: list[dict]
    ) -> str:

        context_parts = []

        for index, document in enumerate(
            documents,
            start=1
        ):

            context_parts.append(
                f"Knowledge Source {index}:\n"
                f"{document['text']}"
            )

        return "\n\n".join(
            context_parts
        )

    def ask(
        self,
        conversation_id: str,
        query: str
    ) -> dict:

        # 1. Retrieve relevant documents
        documents = self.retrieve_context(
            query
        )

        # 2. Build context
        context = self.build_context(
            documents
        )

        # 3. Get conversation history
        history = self.memory.format_history(
            conversation_id
        )

        # 4. Build prompt
        prompt = build_rag_prompt(
            query=query,
            context=context,
            conversation_history=history
        )

        # 5. Generate answer
        answer = self.llm.generate(
            prompt
        )

        # 6. Validate answer
        validation = self.validator.validate(
            answer=answer,
            context=context
        )

        # 7. Save conversation
        self.memory.add_message(
            conversation_id,
            "user",
            query
        )

        self.memory.add_message(
            conversation_id,
            "assistant",
            answer
        )

        # 8. Return complete response
        return {
            "conversation_id": conversation_id,
            "query": query,
            "answer": answer,
            "documents": documents,
            "validation": validation,
        }


if __name__ == "__main__":

    rag = RAGPipeline()

    conversation_id = "DEMO001"

    result = rag.ask(
        conversation_id=conversation_id,
        query="How long does a refund take?"
    )

    print("\n" + "=" * 70)
    print("QUESTION")
    print("=" * 70)

    print(result["query"])

    print("\n" + "=" * 70)
    print("ANSWER")
    print("=" * 70)

    print(result["answer"])

    print("\n" + "=" * 70)
    print("VALIDATION")
    print("=" * 70)

    print(result["validation"])
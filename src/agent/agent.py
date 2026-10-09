
from src.agent.escalation import (
    escalate_to_human,
    should_escalate,
)
from src.agent.tools import (
    check_order_status,
    create_support_ticket,
    search_customer_orders,
)
from src.rag.rag_pipeline import RAGPipeline


class CustomerSupportAgent:
    """
    AI customer-support agent that routes requests to
    RAG, business tools, or human escalation.
    """

    def __init__(self):
        self.rag = RAGPipeline()

    def handle_order_tracking(
        self,
        customer_id: str,
        query: str,
    ) -> dict:
        """Find an order and return its current status."""

        order_id = None

        for word in query.upper().split():
            candidate = word.strip(".,?!:;")

            if candidate.startswith("ORD"):
                order_id = candidate
                break

        if order_id:
            result = check_order_status(order_id)

            if result.get("success"):
                return {
                    "agent_action": "check_order_status",
                    "result": result,
                }

            return {
                "agent_action": "check_order_status",
                "result": result,
            }

        # No order number was supplied: look up this customer's orders.
        orders = search_customer_orders(customer_id)

        return {
            "agent_action": "search_customer_orders",
            "result": orders,
        }

    def run(
        self,
        customer_id: str,
        query: str,
        intent: str,
        confidence: float = 1.0,
        priority: str = "medium",
        conversation_id: str | None = None,
    ) -> dict:
        """Choose the appropriate action for the customer request."""

        # 1. Escalate only when the escalation policy requires it.
        if should_escalate(
            intent=intent,
            priority=priority,
            confidence=confidence,
        ):
            escalation = escalate_to_human(
                customer_id=customer_id,
                query=query,
                intent=intent,
                priority=priority,
            )

            return {
                "agent_action": "escalate",
                "result": escalation,
            }

        # 2. Order questions use business tools.
        if intent == "order_tracking":
            return self.handle_order_tracking(
                customer_id=customer_id,
                query=query,
            )

        # 3. Account requests create a support ticket in this prototype.
        if intent == "account":
            ticket_result = create_support_ticket(
                customer_id=customer_id,
                query=query,
                intent=intent,
                priority=priority,
            )

            return {
                "agent_action": "create_ticket",
                "result": ticket_result,
            }

        # 4. Other knowledge questions use RAG.
        rag_result = self.rag.ask(
            conversation_id=conversation_id or customer_id,
            query=query,
        )

        return {
            "agent_action": "rag_response",
            "result": rag_result,
        }


if __name__ == "__main__":
    agent = CustomerSupportAgent()

    # Test a normal refund question.
    result = agent.run(
        customer_id="WEB-C001",
        conversation_id="TEST001",
        query="How long does a refund take?",
        intent="refund",
        confidence=0.26,
        priority="medium",
    )

    print("\n" + "=" * 60)
    print("AGENT RESULT")
    print("=" * 60)
    print("Action:", result["agent_action"])
    print("Result:", result["result"])

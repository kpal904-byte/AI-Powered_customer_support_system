from src.agent.escalation import (
    escalate_to_human,
    should_escalate,
)
from src.agent.tools import (
    check_order_status,
    create_support_ticket,
    get_tracking_info,
    search_customer_orders,
)
from src.rag.rag_pipeline import RAGPipeline


class CustomerSupportAgent:
    """
    Agentic AI controller for customer support.

    The agent decides which action should be taken
    based on the detected intent.
    """

    def __init__(self):

        self.rag = RAGPipeline()

    # -----------------------------------------------------
    # Order related actions
    # -----------------------------------------------------

    def handle_order_tracking(
        self,
        customer_id: str,
        query: str
    ) -> dict:

        # Check whether an order number was provided.
        words = query.upper().split()

        order_id = None

        for word in words:

            if word.startswith("ORD"):
                order_id = word.strip(".,?!")

                break

        # If order ID is available, directly check it.
        if order_id:

            result = check_order_status(
                order_id
            )

            if result["success"]:

                return {
                    "action": "check_order_status",
                    "result": result,
                }

        # Otherwise retrieve customer's orders.
        orders = search_customer_orders(
            customer_id
        )

        return {
            "action": "search_customer_orders",
            "result": orders,
        }

    # -----------------------------------------------------
    # Agent main decision
    # -----------------------------------------------------

    def run(
    self,
    customer_id: str,
    query: str,
    intent: str,
    confidence: float = 1.0,
    priority: str = "medium",
    conversation_id: str | None = None
) -> dict:
        """
        Decide what action the AI agent should perform.
        """

        # -------------------------------------------------
        # Step 1: Check escalation conditions
        # -------------------------------------------------

        if should_escalate(
            intent=intent,
            priority=priority,
            confidence=confidence
        ):

            escalation = escalate_to_human(
                customer_id=customer_id,
                query=query,
                intent=intent,
                priority=priority
            )

            return {
                "agent_action": "escalate",
                "result": escalation,
            }

        # -------------------------------------------------
        # Step 2: Order tracking
        # -------------------------------------------------

        if intent == "order_tracking":

            result = self.handle_order_tracking(
                customer_id=customer_id,
                query=query
            )

            return {
                "agent_action": result["action"],
                "result": result["result"],
            }

        # -------------------------------------------------
        # Step 3: Account/support actions
        # -------------------------------------------------

        if intent == "account":

            result = create_support_ticket(
                customer_id=customer_id,
                query=query,
                intent=intent,
                priority="medium"
            )

            return {
                "agent_action": "create_ticket",
                "result": result,
            }

        # -------------------------------------------------
        # Step 4: Knowledge-based questions
        # -------------------------------------------------

        rag_result = self.rag.ask(
    conversation_id=conversation_id or customer_id,
    query=query
)

        return {
            "agent_action": "rag_response",
            "result": rag_result,
        }


if __name__ == "__main__":

    agent = CustomerSupportAgent()

    result = agent.run(
    customer_id="C002",
    query="My laptop is overheating badly.",
    intent="technical_issue",
    confidence=0.95,
    priority="high"
)

    print("\n" + "=" * 70)
    print("AGENT RESULT")
    print("=" * 70)

    print(result)
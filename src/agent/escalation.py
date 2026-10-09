from src.agent.tools import create_support_ticket


HIGH_PRIORITY_INTENTS = {
    "technical_issue",
    "payment",
}


def should_escalate(
    intent: str,
    priority: str = "medium",
    confidence: float = 1.0
) -> bool:
    """
    Decide whether a request needs human support.
    """

    # Explicit high-priority requests go to human support.
    if priority.lower() == "high":
        return True

    # These intents currently use conservative escalation.
    if intent in HIGH_PRIORITY_INTENTS:
        return True

    # Do not escalate solely because of a low
    # classifier confidence score in this prototype.
    return False


def escalate_to_human(
    customer_id: str,
    query: str,
    intent: str,
    priority: str = "high"
) -> dict:
    """
    Create a human-support ticket.
    """

    ticket_result = create_support_ticket(
        customer_id=customer_id,
        query=query,
        intent=intent,
        priority=priority
    )

    return {
        "escalated": True,
        "reason": "Human support required",
        "ticket": ticket_result
    }


if __name__ == "__main__":

    result = escalate_to_human(
        customer_id="C002",
        query="My device is overheating badly.",
        intent="technical_issue",
        priority="high"
    )

    print(result)
from datetime import datetime


# ---------------------------------------------------------
# Mock order database
# ---------------------------------------------------------

ORDERS = {
    "ORD1001": {
        "order_id": "ORD1001",
        "customer_id": "C001",
        "status": "shipped",
        "tracking_number": "TRK10001",
        "estimated_delivery": "2026-10-12",
    },
    "ORD1002": {
        "order_id": "ORD1002",
        "customer_id": "C002",
        "status": "processing",
        "tracking_number": None,
        "estimated_delivery": "2026-10-14",
    },
    "ORD1003": {
        "order_id": "ORD1003",
        "customer_id": "C003",
        "status": "delivered",
        "tracking_number": "TRK10003",
        "estimated_delivery": "2026-10-05",
    },
}


# ---------------------------------------------------------
# Tool 1: Check order status
# ---------------------------------------------------------

def check_order_status(order_id: str) -> dict:
    """
    Check the current status of an order.
    """

    order_id = order_id.strip().upper()

    order = ORDERS.get(order_id)

    if not order:
        return {
            "success": False,
            "message": f"Order {order_id} was not found."
        }

    return {
        "success": True,
        "order": order
    }


# ---------------------------------------------------------
# Tool 2: Get tracking information
# ---------------------------------------------------------

def get_tracking_info(order_id: str) -> dict:
    """
    Get tracking information for an order.
    """

    order_id = order_id.strip().upper()

    order = ORDERS.get(order_id)

    if not order:
        return {
            "success": False,
            "message": f"Order {order_id} was not found."
        }

    if not order["tracking_number"]:
        return {
            "success": False,
            "message": "Tracking information is not available yet."
        }

    return {
        "success": True,
        "tracking_number": order["tracking_number"],
        "status": order["status"],
        "estimated_delivery": order["estimated_delivery"]
    }


# ---------------------------------------------------------
# Tool 3: Create support ticket
# ---------------------------------------------------------

def create_support_ticket(
    customer_id: str,
    query: str,
    intent: str,
    priority: str = "medium"
) -> dict:
    """
    Create a new support ticket.
    """

    ticket_id = (
        f"TICKET-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    )

    ticket = {
        "ticket_id": ticket_id,
        "customer_id": customer_id,
        "query": query,
        "intent": intent,
        "priority": priority,
        "status": "open",
    }

    return {
        "success": True,
        "ticket": ticket,
        "message": (
            f"Support ticket {ticket_id} "
            f"has been created successfully."
        )
    }


# ---------------------------------------------------------
# Tool 4: Search order
# ---------------------------------------------------------

def search_customer_orders(
    customer_id: str
) -> list[dict]:
    """
    Return orders associated with a customer.
    """

    results = []

    for order in ORDERS.values():

        if order["customer_id"] == customer_id:
            results.append(order)

    return results


# ---------------------------------------------------------
# Tool testing
# ---------------------------------------------------------

if __name__ == "__main__":

    print("\nOrder Status:")
    print(
        check_order_status("ORD1001")
    )

    print("\nTracking:")
    print(
        get_tracking_info("ORD1001")
    )

    print("\nCustomer Orders:")
    print(
        search_customer_orders("C001")
    )

    print("\nCreate Ticket:")
    print(
        create_support_ticket(
            customer_id="C001",
            query="My product is not working.",
            intent="technical_issue",
            priority="high"
        )
    )
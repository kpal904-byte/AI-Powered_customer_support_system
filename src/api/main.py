from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from src.agent.agent import CustomerSupportAgent
from src.nlp.intent_classifier import IntentClassifier


# ---------------------------------------------------------
# FastAPI application
# ---------------------------------------------------------

app = FastAPI(
    title="AI Customer Support System",
    description=(
        "AI-powered customer support API using "
        "Machine Learning, RAG, LLM and Agentic AI."
    ),
    version="1.0.0"
)


# ---------------------------------------------------------
# Load application components
# ---------------------------------------------------------

classifier = IntentClassifier()

agent = CustomerSupportAgent()


# ---------------------------------------------------------
# Request schema
# ---------------------------------------------------------

class ChatRequest(BaseModel):

    customer_id: str = Field(
        ...,
        min_length=1
    )

    conversation_id: str = Field(
        ...,
        min_length=1
    )

    message: str = Field(
        ...,
        min_length=1
    )

    priority: str = Field(
        default="medium"
    )


# ---------------------------------------------------------
# Response helper
# ---------------------------------------------------------

def build_response(
    intent: str,
    confidence: float,
    agent_result: dict
) -> dict:

    action = agent_result.get(
        "agent_action"
    )

    result = agent_result.get(
        "result",
        {}
    )

    response_text = None

    # RAG response
    if action == "rag_response":

        response_text = result.get(
            "answer"
        )

    # Order tool
    elif action == "check_order_status":

        if isinstance(result, dict):
            response_text = result.get(
                "message"
            )

            if not response_text:
                order = result.get(
                    "order"
                )

                if order:
                    response_text = (
                        f"Your order {order['order_id']} "
                        f"is currently {order['status']}."
                    )

    # Customer order search
    elif action == "search_customer_orders":

        response_text = (
            "I found your customer orders."
        )

    # Ticket creation
    elif action == "create_ticket":

        response_text = result.get(
            "message",
            "A support ticket has been created."
        )

    # Human escalation
    elif action == "escalate":

        response_text = (
            "Your issue has been escalated "
            "to human support."
        )

    if not response_text:

        response_text = (
            "Your request has been processed. "
            "Please contact customer support "
            "for further assistance."
        )

    return {
        "intent": intent,
        "confidence": round(
            confidence,
            4
        ),
        "agent_action": action,
        "response": response_text,
        "details": result
    }


# ---------------------------------------------------------
# Health endpoint
# ---------------------------------------------------------

@app.get("/health")
def health_check():

    return {
        "status": "healthy",
        "service": "AI Customer Support System"
    }


# ---------------------------------------------------------
# Chat endpoint
# ---------------------------------------------------------

@app.post("/chat")
def chat(request: ChatRequest):

    try:

        # ---------------------------------------------
        # Step 1: Intent classification
        # ---------------------------------------------

        prediction = classifier.predict(
            request.message
        )

        intent = prediction["intent"]
        confidence = prediction["confidence"]

        # ---------------------------------------------
        # Step 2: Agent decision
        # ---------------------------------------------

        agent_result = agent.run(
            customer_id=request.customer_id,
            conversation_id=request.conversation_id,
            query=request.message,
            intent=intent,
            confidence=confidence,
            priority=request.priority
        )

        # ---------------------------------------------
        # Step 3: Build API response
        # ---------------------------------------------

        return build_response(
            intent=intent,
            confidence=confidence,
            agent_result=agent_result
        )

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )
"""
Vacation Rentals agent using LiteLLM with Nebius TokenFactory API.

This agent uses the deepseek-ai/DeepSeek-V3-0324-fast model hosted on Nebius TokenFactory,
accessed via LiteLLM's native Nebius provider.

Authentication:
- Requires NEBIUS_API_KEY environment variable
- API base URL: https://api.tokenfactory.nebius.com/v1/
"""

import os

from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm


SYSTEM_PROMPT = """You are a vacation rental customer service agent.

You help customers with inquiries about:
- Reservation cancellations and refund policies
- Cancellation policy explanations (flexible, moderate, firm, strict)
- Refund processing timelines
- Free cancellation period rules

## Cancellation Policies

### Free Cancellation Period
All reservations include a free cancellation period: guests may cancel for a full refund within 24 hours of booking confirmation, provided the reservation was made at least 7 days before check-in.

### Flexible Policy
- 24 hours or more before check-in: full refund
- Less than 24 hours before check-in: first night non-refundable, remaining nights refunded

### Moderate Policy
- 5 days or more before check-in: full refund
- Less than 5 days before check-in: first night non-refundable, 50% of remaining nights refunded

### Firm Policy
- 30 days or more before check-in: full refund
- 7-29 days before check-in: 50% refund
- Less than 7 days before check-in: no refund

### Strict Policy
- 7 days or more before check-in: 50% refund
- Less than 7 days before check-in: no refund

### Host Cancellation
If a host cancels a confirmed reservation, the guest receives a full refund regardless of timing or cancellation policy.

### Major Disruptive Events
Full refunds are provided regardless of cancellation policy when cancellation is due to:
- Declared public health emergencies
- Government-imposed travel restrictions
- Natural disasters affecting the property or travel route
- Military actions or civil unrest at the destination

## Refund Processing
- Refunds are processed to the original payment method used for the booking
- Refunds are typically processed within 10 business days
- Credit card refunds may take up to 15 days depending on the issuing bank

## Important Guidelines
- You do not have access to tools or reservation systems
- For actual cancellations or account changes, direct customers to the appropriate channels
- Be helpful, professional, and accurate
- If you cannot help with a specific request, explain what the customer should do instead
"""


def create_agent() -> LlmAgent:
    """
    Create an ADK agent configured with deepseek-ai/DeepSeek-V3-0324-fast via LiteLLM.

    Uses the Nebius TokenFactory API endpoint with the NEBIUS_API_KEY
    environment variable for authentication.

    Returns:
        LlmAgent configured to use the specified Nebius model.
    """
    # Nebius TokenFactory configuration
    api_base = os.getenv(
        "NEBIUS_API_BASE", "https://api.tokenfactory.nebius.com/v1/"
    )
    api_key = os.getenv("NEBIUS_API_KEY")

    # Model can be overridden via environment variable
    model_name = os.getenv("VR_AGENT_MODEL", "deepseek-ai/DeepSeek-V3-0324-fast")

    # LiteLLM uses "nebius/" prefix for Nebius provider
    litellm_model = f"nebius/{model_name}"

    # Create LiteLLM model with Nebius TokenFactory endpoint
    llm_model = LiteLlm(
        model=litellm_model,
        api_base=api_base,
        api_key=api_key,
    )

    # Create agent with LiteLLM configuration
    agent = LlmAgent(
        model=llm_model,
        name="vacation_rentals_agent",
        description="A vacation rental customer service agent for policy questions and guidance",
        instruction=SYSTEM_PROMPT,
    )

    return agent


# Create the agent instance (used by ADK CLI)
# ADK looks for 'root_agent' by default
root_agent = create_agent()
agent = root_agent  # Alias for backward compatibility


if __name__ == "__main__":
    print("Vacation Rentals Agent")
    print(f"Name: {agent.name}")
    print(f"Description: {agent.description}")
    print(f"Model: {agent.model}")

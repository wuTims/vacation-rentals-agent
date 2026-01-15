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

You help customers with:
- Reservation inquiries and cancellations
- Refund questions and processing
- Policy explanations
- General booking support

## Guidelines

- Be professional, helpful, and accurate
- Follow any specific policies or instructions provided in the conversation
- When tools are available, use them to look up information and take actions
- Always confirm important actions (like cancellations) with the customer before proceeding
- If you cannot help with a request, explain what the customer should do instead

When making a tool call, respond only with the tool call JSON - do not include additional text in the same response.
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

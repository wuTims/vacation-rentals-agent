# =============================================================================
# Vacation Rentals Agent - ADK agent using LiteLLM via Nebius TokenFactory
# =============================================================================
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8001 \
    PYTHONPATH=/app/agents \
    AGENTS_DIR=/app/agents \
    # Container mode for logging
    CONTAINER_MODE=true

WORKDIR /app

# Install curl for health checks
RUN apt-get update && apt-get install -y --no-install-recommends curl && rm -rf /var/lib/apt/lists/*

# Install ADK, LiteLLM, and dependencies
RUN pip install --no-cache-dir \
    google-adk[a2a]>=1.18.0 \
    litellm>=1.65.0 \
    httpx>=0.28.0 \
    uvicorn>=0.34.0 \
    loguru>=0.7.3 \
    aiofiles>=24.1.0

# Create agents directory and copy agent source directly into it
# (ADK validates symlinks don't resolve outside base directory)
RUN mkdir -p /app/agents
COPY vacation_rentals_agent/ ./agents/vacation_rentals_agent/

# Copy shared utilities (middleware, server_utils, card_url_utils)
COPY shared_utils/ ./agents/shared_utils/

# Create .adk directory for ADK artifact storage
RUN mkdir -p /app/.adk

EXPOSE 8001

HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD python -c "import httpx; httpx.get('http://localhost:8001/.well-known/agent-card.json', timeout=5).raise_for_status()" || exit 1

# AgentBeats-compatible entrypoint: accepts --host, --port, --card-url args
# CARD_URL env var is read by server.py to update agent.json URL at startup
ENTRYPOINT ["python", "-m", "vacation_rentals_agent.server"]
CMD ["--host", "0.0.0.0"]

# vacation-rentals-agent

A vacation rental customer service agent built with Google ADK and served via A2A protocol. Powered by Nebius TokenFactory LLM (`openai/gpt-oss-120b`) via LiteLLM.

## Features

- A2A-compliant agent serving at root path (`/`) and ADK path (`/a2a/vacation_rentals_agent`)
- Agent card discovery at `/.well-known/agent-card.json`
- Conversational agent for vacation rental policy questions
- Health check endpoints for container orchestration
- Multi-platform Docker image (amd64/arm64)

## Quick Start

### Local Development

1. Clone the repository:
   ```bash
   git clone https://github.com/YOUR_ORG/vacation-rentals-agent.git
   cd vacation-rentals-agent
   ```

2. Set up environment:
   ```bash
   cp .env.example .env
   # Edit .env and add your NEBIUS_API_KEY
   ```

3. Install dependencies:
   ```bash
   uv sync
   ```

4. Run the server:
   ```bash
   uv run python -m vacation_rentals_agent.server
   ```

### Docker

Build and run with Docker Compose:

```bash
docker compose -f vacation_rentals_agent/docker_setup/docker-compose.yml up --build
```

Or build the image directly:

```bash
docker build -t vacation-rentals-agent -f vacation_rentals_agent/docker_setup/Dockerfile .
docker run -p 8001:8001 -e NEBIUS_API_KEY=your-key vacation-rentals-agent
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `NEBIUS_API_KEY` | Nebius TokenFactory API key | Required |
| `NEBIUS_API_BASE` | Nebius API base URL | `https://api.tokenfactory.nebius.com/v1/` |
| `VR_AGENT_MODEL` | Model name | `openai/gpt-oss-120b` |
| `HOST` | Server bind host | `0.0.0.0` |
| `PORT` | Server bind port | `8001` |
| `LOG_LEVEL` | Logging level | `INFO` |
| `CARD_URL` | External URL for agent card | `http://localhost:{PORT}` |

## A2A Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | POST | A2A message endpoint (rewritten to `/a2a/vacation_rentals_agent`) |
| `/.well-known/agent-card.json` | GET | Agent card for discovery |
| `/a2a/vacation_rentals_agent` | POST | Direct ADK A2A endpoint |
| `/a2a/vacation_rentals_agent/.well-known/agent-card.json` | GET | ADK agent card |

## Testing

Test agent card discovery:

```bash
curl http://localhost:8001/.well-known/agent-card.json
```

Test A2A message at root:

```bash
curl -X POST http://localhost:8001/ \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "message/send",
    "params": {
      "message": {
        "role": "user",
        "parts": [{"text": "What is the flexible cancellation policy?"}]
      }
    },
    "id": "1"
  }'
```

## Deployment

The GitHub Actions workflow automatically builds and pushes Docker images to GHCR on:
- Push to `main` branch (tagged as `latest`)
- Version tags (`v*`)

Images are available at:
```
ghcr.io/YOUR_ORG/vacation-rentals-agent:latest
ghcr.io/YOUR_ORG/vacation-rentals-agent:v1.0.0
ghcr.io/YOUR_ORG/vacation-rentals-agent:{sha}
```

## License

MIT

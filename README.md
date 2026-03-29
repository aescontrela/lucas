# Travel Research API

A learning project for exploring **multi-agent router pattern** design with Python and FastAPI.

This API takes a travel query and returns structured research across multiple domains — food, culture, logistics, safety, and must-do activities.

## Architecture

```
User query
    │
    ▼
RouterAgent          ← selects relevant agents, writes a tailored task for each one
    │
    ▼
ResearchOrchestrator ← runs selected agents in parallel, streams results via SSE
    │
    ├── FoodAgent
    ├── CultureAgent
    ├── LogisticsAgent
    ├── MustDoAgent
    └── SafetyAgent
```

## Stack

- Python 3.12
- FastAPI
- Anthropic Claude API (structured outputs)
- uv (package manager)
- Render (deployment)

## Run locally

```bash
cd backend/api
cp .env.example .env  # add your ANTHROPIC_API_KEY
uv run uvicorn main:app --reload
```

## Test

```bash
uv run pytest tests/ -v
```

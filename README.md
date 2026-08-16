# Travel Research API

![CI](https://github.com/aescontrela/lucas/actions/workflows/ci.yml/badge.svg)

**Live API:** [api-dph9.onrender.com/docs](https://api-dph9.onrender.com/docs)

**Lucas** is an AI travel agent designed to power a search-style UI. The user enters a travel query, Lucas analyses it, and streams back live research across food, culture, logistics, safety, and must-do activities.

This repository contains the backend API, a Python/FastAPI implementation of the **multi-agent router pattern**: a router agent interprets each query and dispatches tailored tasks to specialist research agents, whose findings stream back concurrently over a single connection.

Built while learning Python and FastAPI from a JavaScript/React background — feedback and issues welcome.

## Architecture

```
User query
    │
    ▼
RouterAgent          ← selects relevant agents, writes a tailored task for each one
    │
    ▼
ResearchOrchestrator ← runs selected agents concurrently via asyncio.Queue
    │                    multiplexes all results into a single SSE stream
    ├── ResearchAgent("food")
    ├── ResearchAgent("culture")
    ├── ResearchAgent("logistics")
    ├── ResearchAgent("activities")
    └── ResearchAgent("safety")
```

## API

`POST /research` with `{"query": "<travel question, 1-500 chars>"}` returns a Server-Sent Events stream (`text/event-stream`) of JSON events: the research plan, per-agent text deltas, and per-agent completion or error events, always terminated by a `stream_done` event.

Full API documentation — including the event protocol table, request schema, and an example stream — is served by the app itself at [api-dph9.onrender.com/docs](https://api-dph9.onrender.com/docs) (OpenAPI/Swagger UI). Event models are defined in [`app/schemas/events.py`](backend/api/app/schemas/events.py).

Try it against the live deployment (`-N` keeps curl from buffering, so events appear as they stream):

```bash
curl -N -X POST https://api-dph9.onrender.com/research \
  -H "Content-Type: application/json" \
  -d '{"query": "one day in Lisbon"}'
```

Known limitation: the endpoint is unauthenticated and unthrottled — fine for a demo deployment, not for production traffic.

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

Interactive OpenAPI docs are served at [http://localhost:8000/docs](http://localhost:8000/docs).

## Test

```bash
uv run pytest tests/ -v
```

# Tilly — The Email Sorting Agent

👋 Hello from Tilly the personal agent! As of May 2026, Tilly has a LangChain-based email agent that classifies your Gmail inbox using a local LLM via Ollama. ([Jiah](https://github.com/njiah) struggles to sort her emails). The intention is to expand this into a larger multi-agent system.

## What it does

- Fetches recent unread emails from Gmail
- Classifies each email into a category (newsletter, work, personal, etc.) using a local LLM
- Suggests an action (keep in inbox, label only, archive)
- Applies a Gmail label (`ai/<category>`) to each email

All inference runs locally — no email content leaves your machine.

## Stack

- **LangChain + LangGraph** — agent framework
- **Ollama (`llama3.2:3b`)** — local LLM
- **Gmail API** — email access via OAuth 2.0
- **Pydantic** — structured output from the LLM
- **uv** — dependency and environment management

## Project structure

```
tilly/
├── src/
│   └── email_agent/
│       ├── config.py         # paths, env vars, model name
│       ├── gmail_client.py   # Gmail auth and API calls
│       ├── classifier.py     # LLM classification chain
│       └── main.py           # entry point
├── tests/
├── data/                     # SQLite storage (gitignored)
├── .env                      # local config (gitignored)
├── pyproject.toml
└── uv.lock
```

## Setup

### Prerequisites

- Python 3.11+
- [uv](https://docs.astral.sh/uv/)
- [Ollama](https://ollama.com) running locally with `llama3.2:3b` pulled

```bash
ollama pull llama3.2:3b
```

### Install

```bash
git clone https://github.com/njiah/tilly.git
cd tilly
uv venv
source .venv/bin/activate
uv pip install -e .
```

### Configure environment

Copy the example and fill in your values:

```bash
cp .env.example .env
```

```env
MODEL_NAME=llama3.2:3b
GMAIL_USER=you@gmail.com
```

### Gmail API credentials

1. Create a project in [Google Cloud Console](https://console.cloud.google.com)
2. Enable the **Gmail API**
3. Configure the **OAuth consent screen** (External, Testing mode)
4. Add your Gmail address as a **Test user**
5. Create an **OAuth client ID** (Desktop app) and download as `credentials.json` into the project root

### Run

```bash
uv run python -m email_agent.main
```

On first run, a browser window will open for Gmail authorization. After approving, `token.json` is saved and subsequent runs skip the browser step.

## Classification categories

| Category | Action |
|---|---|
| `newsletter` | archive |
| `transactional` | archive |
| `promotional` | archive |
| `spam_like` | archive |
| `personal` | keep in inbox |
| `work` | keep in inbox |
| `needs_reply` | keep in inbox |

Labels are applied as `ai/<category>` in Gmail.

## Creator's Roadmap

- Stage 2: persist classifications to SQLite
- Stage 3: auto-archive based on confidence threshold
- Stage 4: Streamlit UI for reviewing and overriding decisions
- Stage 5: learning from user corrections, i.e., store overrides in SQLite, retrieve similar past examples at classification time and inject as prompt context so the agent improves without fine-tuning
- Stage 6: expand to multi-agent system (reply drafting, scheduling, etc.)

# pythonSynapse

This project provides a Python port of the goSynapse client. It exposes a `SynapseClient` class and a simple interactive CLI.

## Installation

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

## Running Tests

Install test dependencies and execute `pytest`:

```bash
pip install pytest
pytest
```

## Configuration

`storm_cli.py` reads its configuration from environment variables which can be supplied via a `.env` file in the project root.
The CLI now requires these variables to be present and will exit if any are missing.

Example `.env`:

```dotenv
SYNAPSE_HOST=synapse.example.com
SYNAPSE_PORT=443
SYNAPSE_API_KEY=your-api-key
SYNAPSE_VIEW_ID=<view-guid>
```

## Launching the CLI

Execute the CLI after activating your environment and creating the `.env` file:

```bash
python scripts/storm_cli.py
```

At the `storm>` prompt type your Storm queries. Type `exit` or `quit` to leave.

## Health Check Utility

A small helper script is provided to verify that your Synapse instance is reachable.
It automatically loads settings from `.env` and checks both the `/active` endpoint
and a trivial Storm call:

```bash
python scripts/health_check.py
```

The script will query the `/active` endpoint and run `return(1)` via `/storm/call`.
It prints the JSON results and exits non-zero if anything fails.

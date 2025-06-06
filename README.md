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
Run it using the same environment variables as the CLI:

```bash
python scripts/health_check.py
```

The script will query the `/core/info` and `/active` endpoints and print the results as JSON. A non-zero exit code indicates the check failed.

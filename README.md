# pythonSynapse

This project provides a Python port of the goSynapse client. It exposes a `SynapseClient` class and a simple interactive CLI.

## Installation

This project requires **Python 3.9** or newer.

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
# Optional: set to "false" to disable TLS certificate verification
SYNAPSE_VERIFY_TLS=true
```

## Launching the CLI

Execute the CLI after activating your environment and creating the `.env` file:

```bash
python scripts/storm_cli.py
```

TLS certificate verification is enabled by default. Set `SYNAPSE_VERIFY_TLS=false`
in your environment to skip verification when connecting to self-signed hosts.

At the `storm>` prompt type your Storm queries. Type `exit` or `quit` to leave.

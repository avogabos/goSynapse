# PythonSynapse

This project provides a simple Python client for interacting with a Synapse Cortex instance. The `scripts` directory contains a command line interface for running Storm queries.

## Environment variables

The CLI reads connection settings from the environment. The following variables are supported:

- `SYNAPSE_HOST`: Hostname of the Cortex instance (default: `localhost`).
- `SYNAPSE_PORT`: Port of the Cortex instance (default: `443`).
- `SYNAPSE_API_KEY`: Optional API key used for authentication.
- `CORTEX_URL`: Full URL of the Cortex (for example `https://mycortex:4444`). When provided, the host and port are derived from this value and override `SYNAPSE_HOST` and `SYNAPSE_PORT`.
- `OUTPUT_FILE`: Path to the file where Storm results are appended (default: `storm_results.json`).

Load these variables using a `.env` file or your shell environment before running `storm_cli.py`.

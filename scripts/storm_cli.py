import json
import os
import logging
from pathlib import Path
import sys

from dotenv import load_dotenv

from gosynapse.client import SynapseClient


def main() -> None:
    logging.basicConfig(level=logging.DEBUG)
    logging.getLogger("urllib3").setLevel(logging.DEBUG)
    env_path = Path(__file__).resolve().parent.parent / ".env"
    load_dotenv(dotenv_path=env_path)

    host = os.environ.get("SYNAPSE_HOST", "").strip()
    port = os.environ.get("SYNAPSE_PORT", "").strip()
    api_key = os.environ.get("SYNAPSE_API_KEY", "").strip()
    view = os.environ.get("SYNAPSE_VIEW_ID")

    missing = [name for name, val in [
        ("SYNAPSE_HOST", host),
        ("SYNAPSE_PORT", port),
        ("SYNAPSE_API_KEY", api_key),
    ] if not val]
    if missing:
        logging.error("Missing required environment variables: %s", ", ".join(missing))
        sys.exit(1)

    client = SynapseClient(host=host, port=port, api_key=api_key)
    output_file = Path("storm_results.json")

    while True:
        query = input("storm> ").strip()
        if not query or query.lower() in {"quit", "exit"}:
            break
        opts = {"view": view} if view else None
        try:
            init, nodes, fini = client.storm(query, opts=opts)
        except Exception as exc:  # requests.HTTPError or connection errors
            logging.error("Storm query failed: %s", exc)
            continue
        result = {
            "init": [i.__dict__ for i in init],
            "nodes": [n.__dict__ for n in nodes],
            "fini": [f.__dict__ for f in fini],
        }
        with output_file.open("a", encoding="utf-8") as f:
            json.dump(result, f)
            f.write("\n")


if __name__ == "__main__":
    main()

import json
import os
from pathlib import Path

from dotenv import load_dotenv

from gosynapse.client import SynapseClient


def main() -> None:
    load_dotenv()
    host = os.environ.get("SYNAPSE_HOST", "localhost")
    port = os.environ.get("SYNAPSE_PORT", "443")
    api_key = os.environ.get("SYNAPSE_API_KEY", "")

    client = SynapseClient(host=host, port=port, api_key=api_key)
    output_file = Path("storm_results.json")

    while True:
        query = input("storm> ").strip()
        if not query or query.lower() in {"quit", "exit"}:
            break
        init, nodes, fini = client.storm(query)
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

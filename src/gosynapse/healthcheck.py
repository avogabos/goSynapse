import json
import logging
import os
from pathlib import Path

try:
    from dotenv import load_dotenv
except Exception:  # pragma: no cover - optional dependency
    def load_dotenv(*_args, **_kwargs) -> None:  # type: ignore
        return None

from .client import SynapseClient

logger = logging.getLogger(__name__)


def main() -> int:
    """Perform a simple health check against a Synapse instance."""
    logging.basicConfig(level=logging.DEBUG)
    # Load .env from project root if present
    env_path = Path(__file__).resolve().parents[2] / ".env"
    load_dotenv(dotenv_path=env_path)

    host = os.environ.get("SYNAPSE_HOST", "").strip()
    port = os.environ.get("SYNAPSE_PORT", "").strip()
    api_key = os.environ.get("SYNAPSE_API_KEY", "").strip()

    missing = [name for name, val in [
        ("SYNAPSE_HOST", host),
        ("SYNAPSE_PORT", port),
        ("SYNAPSE_API_KEY", api_key),
    ] if not val]
    if missing:
        logger.error("Missing required environment variables: %s", ", ".join(missing))
        return 1

    client = SynapseClient(host=host, port=port, api_key=api_key)

    try:
        active = client.get_active()
    except Exception as exc:
        logger.error("[/active] request failed: %s", exc)
        return 1

    if not isinstance(active.result, dict) or not active.result.get("active", False):
        logger.error("[/active] returned inactive: %s", active.result)
        return 1

    try:
        storm_resp = client.storm_call("return(1)", opts=[])
    except Exception as exc:
        logger.error("[/storm/call] request failed: %s", exc)
        return 1

    result = storm_resp.result
    try:
        ok = int(result) == 1
    except Exception:
        ok = False

    if not ok:
        logger.error("[/storm/call] unexpected result: %s", result)
        return 1

    print(json.dumps({"active": active.result, "storm_call_result": result}))
    logger.info("All health checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

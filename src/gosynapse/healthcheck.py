import json
import logging
import os

try:
    from dotenv import load_dotenv
except Exception:  # pragma: no cover - optional dependency
    def load_dotenv() -> None:  # type: ignore
        return None

from .client import SynapseClient

logger = logging.getLogger(__name__)


def main() -> int:
    """Perform a simple health check against a Synapse instance."""
    logging.basicConfig(level=logging.DEBUG)
    load_dotenv()
    host = os.environ.get("SYNAPSE_HOST", "localhost")
    port = os.environ.get("SYNAPSE_PORT", "443")
    api_key = os.environ.get("SYNAPSE_API_KEY", "")
    client = SynapseClient(host=host, port=port, api_key=api_key)
    try:
        core = client.core_info()
        active = client.get_active()
    except Exception as exc:  # requests.HTTPError or connection errors
        logger.error("Health check failed: %s", exc)
        return 1
    print(json.dumps({"core_info": core.__dict__, "active": active.__dict__}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

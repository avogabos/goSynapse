"""Simple health check utilities for Synapse.

This module verifies basic connectivity to a Synapse Cortex by
querying the ``/active`` endpoint and executing trivial Storm
queries. Environment variables are loaded from a ``.env`` file using
``python-dotenv`` and must define ``SYNAPSE_HOST``, ``SYNAPSE_PORT``,
``SYNAPSE_API_KEY`` and ``SYNAPSE_VIEW_ID``.
"""

from __future__ import annotations

import logging
import os
import sys
from pathlib import Path
from typing import Any

import requests
try:
    from dotenv import load_dotenv, find_dotenv
except Exception:  # pragma: no cover - optional dependency
    def load_dotenv(*_args, **_kwargs):
        """Fallback no-op if python-dotenv is not installed."""
        return False

    def find_dotenv(*_args, **_kwargs) -> str:
        return ""
try:
    from urllib3.exceptions import InsecureRequestWarning
    import urllib3
except Exception:  # pragma: no cover - optional dependency
    class InsecureRequestWarning(Exception):
        pass

    class Dummy:
        @staticmethod
        def disable_warnings(*_a, **_k):
            pass

    urllib3 = Dummy()

logger = logging.getLogger(__name__)

urllib3.disable_warnings(category=InsecureRequestWarning)


def _load_env() -> None:
    """Load a ``.env`` file if present."""
    env_path = find_dotenv(usecwd=True)
    if env_path:
        load_dotenv(env_path)


def _required_env() -> tuple[str, str, str, str] | None:
    """Return required environment variables or ``None`` if any are missing."""
    host = os.environ.get("SYNAPSE_HOST", "").strip()
    port = os.environ.get("SYNAPSE_PORT", "").strip()
    api_key = os.environ.get("SYNAPSE_API_KEY", "").strip()
    view_id = os.environ.get("SYNAPSE_VIEW_ID", "").strip()
    if not host or not port or not api_key or not view_id:
        logger.error("One or more required variables are missing in .env")
        logger.error("SYNAPSE_HOST=%s", host or "(empty)")
        logger.error("SYNAPSE_PORT=%s", port or "(empty)")
        logger.error("SYNAPSE_API_KEY=%s", "present" if api_key else "(empty)")
        logger.error("SYNAPSE_VIEW_ID=%s", view_id or "(empty)")
        return None
    return host, port, api_key, view_id


def _check_active(base_url: str, headers: dict[str, str]) -> bool:
    """Verify that ``/active`` returns ``active: true``."""
    url = f"{base_url}/active"
    resp = requests.get(url, headers=headers, verify=False, timeout=5)
    resp.raise_for_status()
    data: Any = resp.json()
    if isinstance(data, dict):
        if "active" in data:
            return bool(data["active"])
        if data.get("status") == "ok" and isinstance(data.get("result"), dict):
            if "active" in data["result"]:
                return bool(data["result"]["active"])
    raise ValueError(f"Unexpected JSON from /active: {data}")


def _check_storm_call(base_url: str, headers: dict[str, str], view_id: str) -> bool:
    """Verify that a trivial Storm query can be executed."""
    url = f"{base_url}/storm/call"
    resp = requests.post(
        url,
        headers=headers,
        json={"view": view_id, "query": "return(1)"},
        verify=False,
        timeout=5,
    )
    resp.raise_for_status()
    data: Any = resp.json()
    if isinstance(data, dict) and data.get("status") == "ok":
        try:
            return int(data.get("result")) == 1
        except Exception as exc:  # pragma: no cover - defensive
            raise ValueError(f"Bad result from /storm/call: {data}") from exc
    raise ValueError(f"Unexpected JSON from /storm/call: {data}")


def _check_hash_md5(base_url: str, headers: dict[str, str], view_id: str) -> bool:
    """Lookup a known MD5 via the streaming ``/storm`` endpoint."""
    url = f"{base_url}/storm"
    payload = {
        "query": '[ hash:md5="ac46297df513b5afaceb9109fa986abe" ]',
        "opts": {"view": view_id},
        "stream": "jsonlines",
    }
    resp = requests.post(
        url,
        headers=headers,
        json=payload,
        verify=False,
        timeout=5,
        stream=True,
    )
    resp.raise_for_status()
    for chunk in resp.iter_content(chunk_size=None, decode_unicode=True):
        if chunk and chunk.strip():
            return True
    return False


def main() -> int:
    """Run the health check returning ``0`` on success."""
    logging.basicConfig(level=logging.INFO)
    _load_env()
    params = _required_env()
    if not params:
        return 1
    host, port, api_key, view_id = params
    base_url = f"https://{host}:{port}/api/v1"
    headers = {"X-API-KEY": api_key, "Content-Type": "application/json"}

    try:
        if not _check_active(base_url, headers):
            logger.error("/active reported inactive")
            return 1
        if not _check_storm_call(base_url, headers, view_id):
            logger.error("/storm/call failed")
            return 1
        if not _check_hash_md5(base_url, headers, view_id):
            logger.error("/storm MD5 lookup failed")
            return 1
    except Exception as exc:  # pragma: no cover - network errors
        logger.error("Health check failed: %s", exc)
        return 1

    print("✅ All health checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

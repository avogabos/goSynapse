"""Python client for Synapse API rewritten from goSynapse."""

from typing import Any

SynapseClient: Any
try:
    from .client import SynapseClient as _SynapseClient
    SynapseClient = _SynapseClient
except ModuleNotFoundError:  # requests may be missing in some environments
    SynapseClient = object()

from .parse import parse_json_stream, InitData, Node, FiniData, PrintData  # noqa: E402
from .types import (  # noqa: E402
    Users,
    Roles,
    Active,
    GenericMessage,
    CortexModel,
    AxonDelete,
)

__all__ = [
    "SynapseClient",
    "parse_json_stream",
    "InitData",
    "Node",
    "FiniData",
    "PrintData",
    "Users",
    "Roles",
    "Active",
    "GenericMessage",
    "CortexModel",
    "AxonDelete",
]

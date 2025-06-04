"""Python client for Synapse API rewritten from goSynapse."""

from typing import Any

SynapseClient: Any
try:
    from .client import SynapseClient as _SynapseClient
    SynapseClient = _SynapseClient
except ModuleNotFoundError:  # requests may be missing in some environments
    SynapseClient = object()
from .parse import parse_json_stream, InitData, Node, FiniData  # noqa: E402
from .types import (  # noqa: E402
from .client import SynapseClient
from .parse import parse_json_stream, InitData, Node, FiniData
from .types import (

  main
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
    "Users",
    "Roles",
    "Active",
    "GenericMessage",
    "CortexModel",
    "AxonDelete",
]

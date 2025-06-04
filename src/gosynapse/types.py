from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass
class Users:
    status: str
    result: List[Dict[str, Any]]


@dataclass
class Roles:
    status: str
    result: List[Dict[str, Any]]


@dataclass
class Active:
    status: str
    result: Dict[str, Any]


@dataclass
class GenericMessage:
    status: str
    result: Any


@dataclass
class CortexModel:
    types: Dict[str, Any] = field(default_factory=dict)
    forms: Dict[str, Any] = field(default_factory=dict)
    tagprops: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AxonDelete:
    status: str
    result: Dict[str, bool]

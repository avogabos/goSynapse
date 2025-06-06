from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List

import requests  # type: ignore

from .types import (
    Users,
    Roles,
    Active,
    GenericMessage,
    CortexModel,
    AxonDelete,
)
from .parse import parse_json_stream, InitData, Node, FiniData

logger = logging.getLogger(__name__)

API_KEY_HEADER = "X-Api-Key"


@dataclass
class SynapseClient:
    host: str
    port: str
    api_key: str = ""
    session: requests.Session = field(default_factory=requests.Session)

    def _url(self, path: str) -> str:
        return f"https://{self.host}:{self.port}{path}"

    def _headers(self) -> Dict[str, str]:
        headers = {}
        if self.api_key:
            headers[API_KEY_HEADER] = self.api_key
        return headers

    def login(self, username: str, password: str) -> None:
        url = self._url("/api/v1/login")
        resp = self.session.post(url, json={"user": username, "passwd": password}, headers=self._headers(), verify=False)
        resp.raise_for_status()
        self.session.headers.update({"Cookie": resp.headers.get("Set-Cookie", "")})

    def logout(self) -> None:
        url = self._url("/api/v1/logout")
        resp = self.session.get(url, headers=self._headers())
        resp.raise_for_status()

    def get_active(self) -> Active:
        url = self._url("/api/v1/active")
        resp = self.session.get(url, headers=self._headers())
        resp.raise_for_status()
        return Active(**resp.json())

    def get_users(self) -> Users:
        url = self._url("/api/v1/auth/users")
        resp = self.session.get(url, headers=self._headers())
        resp.raise_for_status()
        return Users(**resp.json())

    def get_roles(self) -> Roles:
        url = self._url("/api/v1/auth/roles")
        resp = self.session.get(url, headers=self._headers())
        resp.raise_for_status()
        return Roles(**resp.json())

    def add_user(self, username: str) -> GenericMessage:
        url = self._url("/api/v1/auth/adduser")
        resp = self.session.post(url, json={"name": username}, headers=self._headers())
        resp.raise_for_status()
        return GenericMessage(**resp.json())

    def add_role(self, role_name: str) -> GenericMessage:
        url = self._url("/api/v1/auth/addrole")
        resp = self.session.post(url, json={"name": role_name}, headers=self._headers())
        resp.raise_for_status()
        return GenericMessage(**resp.json())

    def delete_role(self, role_name: str) -> GenericMessage:
        url = self._url("/api/v1/auth/delrole")
        resp = self.session.post(url, json={"name": role_name}, headers=self._headers())
        resp.raise_for_status()
        return GenericMessage(**resp.json())

    def modify_user(self, iden: str, user: Dict[str, Any]) -> GenericMessage:
        url = self._url(f"/api/v1/auth/user/{iden}")
        resp = self.session.post(url, json=user, headers=self._headers())
        resp.raise_for_status()
        return GenericMessage(**resp.json())

    def change_password(self, iden: str, password: str) -> GenericMessage:
        url = self._url(f"/api/v1/auth/password/{iden}")
        resp = self.session.post(url, json={"passwd": password}, headers=self._headers())
        resp.raise_for_status()
        return GenericMessage(**resp.json())

    def feed(self, nodes: Dict[str, str]) -> GenericMessage:
        url = self._url("/api/v1/feed")
        resp = self.session.post(url, json=nodes, headers=self._headers())
        resp.raise_for_status()
        return GenericMessage(**resp.json())

    def storm(
        self, storm_query: str, opts: Optional[Dict[str, str]] = None
    ) -> tuple[List[InitData], List[Node], List[FiniData]]:
        url = self._url("/api/v1/storm")
        payload = {"query": storm_query, "opts": opts or {}, "stream": "jsonlines"}
        logger.debug("Storm request URL: %s", url)
        logger.debug("Storm request payload: %s", payload)
        # Use POST for Storm queries. Some Cortex deployments do not expose the
        # legacy GET /storm endpoint, so using POST ensures broader
        # compatibility while still returning the streaming JSON lines.
        resp = self.session.post(
            url,
            json=payload,
            headers=self._headers(),
            verify=False,
            stream=True,
        )
        logger.debug("Storm response status code: %s", resp.status_code)
        resp.raise_for_status()
        body = resp.content
        logger.debug("Storm response body: %s", body.decode(errors="ignore"))
        return parse_json_stream(body)

    def storm_call(self, storm_query: str, opts: List[str]) -> GenericMessage:
        url = self._url("/api/v1/storm/call")
        # Storm function invocations are made via POST requests
        resp = self.session.post(
            url,
            json={"query": storm_query, "opts": opts},
            headers=self._headers(),
        )
        resp.raise_for_status()
        return GenericMessage(**resp.json())

    def storm_export(self, storm_query: str, opts: List[str]) -> GenericMessage:
        url = self._url("/api/v1/storm/export")
        resp = self.session.post(
            url,
            json={"query": storm_query, "opts": opts},
            headers=self._headers(),
        )
        resp.raise_for_status()
        return GenericMessage(**resp.json())

    def model(self) -> CortexModel:
        url = self._url("/api/v1/model")
        resp = self.session.get(url, headers=self._headers())
        resp.raise_for_status()
        return CortexModel(**resp.json())

    def vars_get(self) -> GenericMessage:
        url = self._url("/api/v1/vars/get")
        resp = self.session.get(url, headers=self._headers())
        resp.raise_for_status()
        return GenericMessage(**resp.json())

    def vars_set(self, vars_map: Dict[str, Any]) -> GenericMessage:
        url = self._url("/api/v1/vars/set")
        resp = self.session.post(url, json=vars_map, headers=self._headers())
        resp.raise_for_status()
        return GenericMessage(**resp.json())

    def vars_pop(self, key: str) -> GenericMessage:
        url = self._url("/api/v1/vars/pop")
        resp = self.session.post(url, json={"name": key}, headers=self._headers())
        resp.raise_for_status()
        return GenericMessage(**resp.json())

    def core_info(self) -> GenericMessage:
        url = self._url("/api/v1/core/info")
        resp = self.session.get(url, headers=self._headers())
        resp.raise_for_status()
        return GenericMessage(**resp.json())

    # Axon methods
    def axon_delete(self, sha256s: List[str]) -> AxonDelete:
        url = self._url("/api/v1/axon/files/del")
        resp = self.session.post(url, json={"sha256": sha256s}, headers=self._headers())
        resp.raise_for_status()
        return AxonDelete(**resp.json())

    def axon_put(self, file_bytes: bytes) -> GenericMessage:
        url = self._url("/api/v1/axon/files/put")
        resp = self.session.post(url, data=file_bytes, headers=self._headers())
        resp.raise_for_status()
        return GenericMessage(**resp.json())

    def axon_has(self, sha256: str) -> GenericMessage:
        url = self._url(f"/api/v1/axon/files/has/sha256/{sha256}")
        resp = self.session.get(url, headers=self._headers())
        resp.raise_for_status()
        return GenericMessage(**resp.json())

    def axon_get(self, sha256: str) -> bytes:
        url = self._url(f"/api/v1/axon/files/by/sha256/{sha256}")
        resp = self.session.get(url, headers=self._headers())
        resp.raise_for_status()
        return bytes(resp.content)

import types
import sys

requests_stub = types.ModuleType("requests")
class SessionStub:
    def post(self, *a, **k):
        pass

    def get(self, *a, **k):
        pass
class HTTPError(Exception):
    pass
requests_stub.Session = SessionStub
requests_stub.HTTPError = HTTPError
def _dummy(*a, **k):
    raise NotImplementedError
requests_stub.get = _dummy
requests_stub.post = _dummy
sys.modules.setdefault("requests", requests_stub)

from gosynapse.client import SynapseClient, InitData
from gosynapse import client as client_module

class FakeResponse:
    def __init__(self, status_code, content=b''):
        self.status_code = status_code
        self.content = content
    class HTTPError(Exception):
        pass

    def raise_for_status(self):
        if self.status_code >= 400:
            raise self.HTTPError(f"{self.status_code} error")


def test_storm_post_fallback_to_get(monkeypatch):
    """POST is attempted first and GET is used if POST returns 404."""
    cli = SynapseClient(host="h", port="1")

    post_resp = FakeResponse(404, b"notfound")
    get_resp = FakeResponse(200, b"data")

    monkeypatch.setattr(cli.session, "post", lambda *a, **k: post_resp)
    monkeypatch.setattr(cli.session, "get", lambda *a, **k: get_resp)

    result_tuple = ([InitData(tick=1, text="", abstick=0, hash="", task="")], [], [], [])
    captured = {}

    def fake_parse_json_stream(data):
        captured["data"] = data
        return result_tuple

    monkeypatch.setattr(client_module, "parse_json_stream", fake_parse_json_stream)

    init, nodes, fini, prints = cli.storm("foo")

    assert init == result_tuple[0]
    assert prints == result_tuple[3]
    assert captured["data"] == b"data"

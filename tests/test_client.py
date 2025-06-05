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


def test_storm_uses_get(monkeypatch):
    cli = SynapseClient(host='h', port='1')

    get_resp = FakeResponse(200, b'data')

    captured = {}
    def fake_get(*args, **kwargs):
        captured['verify'] = kwargs.get('verify')
        return get_resp

    monkeypatch.setattr(cli.session, 'get', fake_get)

    result_tuple = ([InitData(tick=1, text='', abstick=0, hash='', task='')], [], [])
    parsed = {}
    def fake_parse_json_stream(data):
        parsed['data'] = data
        return result_tuple
    monkeypatch.setattr(client_module, 'parse_json_stream', fake_parse_json_stream)

    init, nodes, fini = cli.storm('foo')

    assert init == result_tuple[0]
    assert parsed['data'] == b'data'
    assert captured['verify'] is True


def test_storm_verify_flag(monkeypatch):
    cli = SynapseClient(host='h', port='1')

    get_resp = FakeResponse(200, b'data')

    captured = {}

    def fake_get(*args, **kwargs):
        captured['verify'] = kwargs.get('verify')
        return get_resp

    monkeypatch.setattr(cli.session, 'get', fake_get)

    result_tuple = ([InitData(tick=1, text='', abstick=0, hash='', task='')], [], [])
    monkeypatch.setattr(client_module, 'parse_json_stream', lambda d: result_tuple)

    cli.storm('foo', verify=False)

    assert captured['verify'] is False

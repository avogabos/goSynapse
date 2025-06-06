import json
import importlib.util

from gosynapse.client import SynapseClient
from gosynapse.healthcheck import main


class Dummy:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


def test_main_success(monkeypatch, capsys):
    monkeypatch.setenv("SYNAPSE_HOST", "host")
    monkeypatch.setenv("SYNAPSE_PORT", "443")
    monkeypatch.setenv("SYNAPSE_API_KEY", "key")
    monkeypatch.setattr(SynapseClient, "get_active", lambda self: Dummy(status="ok", result={"active": True}))
    monkeypatch.setattr(SynapseClient, "storm_call", lambda self, q, opts: Dummy(status="ok", result=1))
    exit_code = main()
    out = capsys.readouterr().out
    data = json.loads(out)
    assert exit_code == 0
    assert data["active"]["active"] is True
    assert data["storm_call_result"] == 1


def test_main_failure(monkeypatch):
    monkeypatch.setenv("SYNAPSE_HOST", "host")
    monkeypatch.setenv("SYNAPSE_PORT", "443")
    monkeypatch.setenv("SYNAPSE_API_KEY", "key")
    def boom(*args, **kwargs):
        raise Exception("fail")
    monkeypatch.setattr(SynapseClient, "get_active", boom)
    exit_code = main()
    assert exit_code == 1

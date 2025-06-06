import json
import importlib.util

from gosynapse.client import SynapseClient
from gosynapse.healthcheck import main


class Dummy:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


def test_main_success(monkeypatch, capsys):
    monkeypatch.setattr(SynapseClient, "core_info", lambda self: Dummy(status="ok", result={}))
    monkeypatch.setattr(SynapseClient, "get_active", lambda self: Dummy(status="ok", result={}))
    exit_code = main()
    out = capsys.readouterr().out
    data = json.loads(out)
    assert exit_code == 0
    assert "core_info" in data
    assert "active" in data


def test_main_failure(monkeypatch):
    def boom(*args, **kwargs):
        raise Exception("fail")
    monkeypatch.setattr(SynapseClient, "core_info", boom)
    exit_code = main()
    assert exit_code == 1

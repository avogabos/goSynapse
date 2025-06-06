import requests
from gosynapse.healthcheck import main


class Resp:
    def __init__(self, data):
        self._data = data
        self.status_code = 200

    def raise_for_status(self):
        pass

    def json(self):
        return self._data


def test_main_success(monkeypatch, capsys):
    monkeypatch.setenv("SYNAPSE_HOST", "h")
    monkeypatch.setenv("SYNAPSE_PORT", "1")
    monkeypatch.setenv("SYNAPSE_API_KEY", "k")

    monkeypatch.setattr(
        requests,
        "get",
        lambda *a, **k: Resp({"status": "ok", "result": {"active": True}}),
    )
    monkeypatch.setattr(
        requests,
        "post",
        lambda *a, **k: Resp({"status": "ok", "result": 1}),
    )

    exit_code = main()
    out = capsys.readouterr().out
    assert exit_code == 0
    assert "All health checks passed" in out


def test_main_failure(monkeypatch):
    monkeypatch.setenv("SYNAPSE_HOST", "h")
    monkeypatch.setenv("SYNAPSE_PORT", "1")
    monkeypatch.setenv("SYNAPSE_API_KEY", "k")

    def boom(*a, **k):
        raise requests.HTTPError("fail")

    monkeypatch.setattr(requests, "get", boom)
    exit_code = main()
    assert exit_code == 1

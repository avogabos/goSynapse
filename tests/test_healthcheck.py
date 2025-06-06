import requests
from gosynapse.healthcheck import main


class Resp:
    def __init__(self, data=None, *, status=200, stream_chunks=None):
        self._data = data
        self.status_code = status
        self._stream = stream_chunks or []

    def raise_for_status(self):
        if self.status_code >= 400:
            raise requests.HTTPError("fail")

    def json(self):
        return self._data

    def iter_content(self, chunk_size=None, decode_unicode=False):
        for ch in self._stream:
            yield ch


def test_main_success(monkeypatch, capsys):
    monkeypatch.setenv("SYNAPSE_HOST", "h")
    monkeypatch.setenv("SYNAPSE_PORT", "1")
    monkeypatch.setenv("SYNAPSE_API_KEY", "k")
    monkeypatch.setenv("SYNAPSE_VIEW_ID", "v")

    monkeypatch.setattr(
        requests,
        "get",
        lambda *a, **k: Resp({"status": "ok", "result": {"active": True}}),
    )

    def fake_post(url, *a, **k):
        if url.endswith("/storm/call"):
            return Resp({"status": "ok", "result": 1})
        if url.endswith("/storm"):
            return Resp(stream_chunks=["[node]"])
        raise AssertionError(url)

    monkeypatch.setattr(requests, "post", fake_post)

    exit_code = main()
    out = capsys.readouterr().out
    assert exit_code == 0
    assert "All health checks passed" in out


def test_main_failure(monkeypatch):
    monkeypatch.setenv("SYNAPSE_HOST", "h")
    monkeypatch.setenv("SYNAPSE_PORT", "1")
    monkeypatch.setenv("SYNAPSE_API_KEY", "k")
    monkeypatch.setenv("SYNAPSE_VIEW_ID", "v")

    def boom(*a, **k):
        raise requests.HTTPError("fail")

    monkeypatch.setattr(requests, "get", boom)
    exit_code = main()
    assert exit_code == 1

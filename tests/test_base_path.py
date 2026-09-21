from app import base_path, create_app


def test_serves_at_root_when_unset(monkeypatch):
    monkeypatch.delenv("BASE_PATH", raising=False)
    client = create_app({"TESTING": True}).test_client()
    assert client.get("/healthz").status_code == 200


def test_serves_under_prefix(monkeypatch):
    monkeypatch.setenv("BASE_PATH", "/direct/agent-7:3000")
    client = create_app({"TESTING": True}).test_client()
    assert client.get("/direct/agent-7:3000/healthz").status_code == 200
    assert client.get("/healthz").status_code == 404


def test_normalisation(monkeypatch):
    monkeypatch.setenv("BASE_PATH", "direct/agent-7:3000/")
    assert base_path() == "/direct/agent-7:3000"

def test_index(client):
    assert b"Flask scaffold" in client.get("/").data


def test_healthz(client):
    assert client.get("/healthz").get_json() == {"status": "ok"}

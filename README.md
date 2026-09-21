# Flask template

Provisioned from [`Qode-Platform/fleet-template-v1`](https://github.com/Qode-Platform/fleet-template-v1) — the fleet
lifecycle contract (`bin/`, `fleet.conf`, deploy workflows) with a
Flask starter laid on top.

## Origin

    hand-written (no official generator) — application factory + blueprint

Generated 2026-09-21 on Node v22.12.0 / Python 3.12.3. **Dependencies were
never installed and this has never been built or run.** Boot it once before
trusting it.

## Fleet lifecycle

`fleet.conf` drives every script in `bin/`:

| step | command |
|---|---|
| install | `python3 -m venv .venv && .venv/bin/pip install --upgrade pip -r requirements.txt` |
| build | `(none)` |
| start | `.venv/bin/gunicorn "app:create_app()" --bind 0.0.0.0:$PORT` |

    ./bin/run       # install, build, start in the foreground
    ./bin/start     # start from existing build artifacts
    ./bin/restart   # rebuild and restart
    ./bin/stop      # stop whatever holds the port

Listens on `$PORT` (default `8000`); health check hits `/healthz`.

## What differs from stock output

- Added gunicorn to requirements.txt; the Flask dev server is not a production start command.

---

# Flask scaffold

Hand-written — Flask ships no project generator. Layout follows the official
tutorial: application factory + blueprints.

    python -m venv .venv && . .venv/bin/activate
    pip install -r requirements.txt
    flask --app app run --debug     # http://127.0.0.1:5000
    pytest

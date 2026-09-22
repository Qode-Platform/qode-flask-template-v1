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

## BASE_PATH

The fleet injects `BASE_PATH` (`/direct/<agent>:<port>`) and nginx forwards
that prefix **unchanged** — so this app serves every route and asset under
it. An empty or unset value means standalone mode: serve at the host root.

- DispatcherMiddleware mounts the app at the prefix; ProxyFix trusts the fleet's X-Forwarded-* headers.
- `HEALTH_PATH` in `fleet.conf` stays un-prefixed; the fleet prepends `$BASE_PATH` itself.
- A value like `direct/x:3000/` is normalised to `/direct/x:3000`.
- Verified here: 5 tests pass, covering root mode, prefixed mode and normalisation.

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

## Rule: everything under BASE_PATH

The fleet serves this app behind a proxy at `BASE_PATH=/direct/<agent>:<port>`, and the
prefix is forwarded **unchanged** — it is NOT stripped before it reaches Flask. So every
route, every redirect, every asset URL and every docs URL must carry `$BASE_PATH`.

Never hard-code a leading-slash path in `app/templates/*.html` or in a redirect.
`href="/healthz"`, `redirect("/")` and `src="/static/app.css"` all point at the proxy's
root and 404.

Use Flask's own mechanism — it already works here:

- `app/__init__.py` mounts the app with `DispatcherMiddleware` under the prefix, so the
  prefix lives in `SCRIPT_NAME` and `url_for()` emits it.
- In templates use `{{ url_for('main.index') }}` and
  `{{ url_for('static', filename='app.css') }}`; in views use
  `redirect(url_for('main.index'))`.
- Blueprint route decorators stay relative (`@bp.get("/healthz")`) — the mount adds the
  prefix; do not repeat it.
- `HEALTH_PATH` in `fleet.conf` stays un-prefixed; the fleet prepends `$BASE_PATH` itself.

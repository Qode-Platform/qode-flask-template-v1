"""Application factory, as in the official Flask tutorial."""

import os

from flask import Flask
from werkzeug.exceptions import NotFound
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.middleware.proxy_fix import ProxyFix


def base_path() -> str:
    """Normalised fleet prefix: '' or '/leading/no-trailing-slash'.

    nginx forwards the whole /direct/<agent>:<port> prefix UNCHANGED, so the
    app must answer on it. Empty/unset => serve at the host root.
    """
    raw = (os.getenv("BASE_PATH") or "").strip().strip("/")
    return f"/{raw}" if raw else ""


def create_app(test_config: dict | None = None) -> Flask:
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(SECRET_KEY="dev")

    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.from_mapping(test_config)

    from app import routes

    app.register_blueprint(routes.bp)

    # The fleet terminates TLS upstream and forwards over HTTP.
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

    # Mount the whole app under the prefix. DispatcherMiddleware moves the
    # prefix into SCRIPT_NAME, so url_for() emits prefixed URLs and the views
    # themselves stay unaware of it.
    prefix = base_path()
    if prefix:
        app.wsgi_app = DispatcherMiddleware(NotFound(), {prefix: app.wsgi_app})

    return app

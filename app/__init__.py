"""Application factory, as in the official Flask tutorial."""

from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix


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

    return app

"""Blueprints keep routes out of the factory."""

from flask import Blueprint, jsonify, render_template

bp = Blueprint("main", __name__)


@bp.get("/")
def index():
    return render_template("index.html", title="Flask scaffold")


@bp.get("/healthz")
def healthz():
    return jsonify(status="ok")

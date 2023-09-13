#!/usr/bin/python3
"""script returns the status of api"""

import os
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views


app = Flask(__name__)
app.register_blueprint(app_views)
app.url_map.strict_slashes = False


@app.teardown_appcontext
def close_storage(exception=None):
    """close current SQLalchmey session"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """returns 404 err"""
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    HBNB_API_HOST = os.environ.get("HBNB_API_HOST") or "0.0.0.0"
    HBNB_API_PORT = os.environ.get("HBNB_API_PORT") or 5000
    app.run(HBNB_API_HOST, HBNB_API_PORT, threaded=True)

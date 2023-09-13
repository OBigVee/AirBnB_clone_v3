#!/usr/bin/python3

from api.v1.views import app_views
from models import storage
from api.v1.views import app_views
from flask import jsonify


@app_views.route("/status")
def status():
    """returns json  describing the status of api"""
    return jsonify({"status": "OK"})

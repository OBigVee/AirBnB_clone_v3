#!/usr/bin/python3
"""index file"""

from api.v1.views import app_views
from models import storage
from api.v1.views import app_views
from flask import jsonify


@app_views.route("/status")
def status():
    """returns json  describing the status of api"""
    return jsonify({"status": "OK"})


@app_views.route("/stats")
def stat():
    """endpoint retrieves number of each objects by type"""
    from models.user import User
    from models.amenity import Amenity
    from models.city import City
    from models.place import Place
    from models.state import State
    from models.review import Review

    classes = {
        "amenities": Amenity,
        "cities": City,
        "places": Place,
        "reviews": Review,
        "states": State,
        "users": User,
    }

    return jsonify({obj: storage.count(classes[obj]) for obj in classes})

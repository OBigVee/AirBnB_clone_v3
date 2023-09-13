#!/usr/bin/python3
"""index file"""

from flask import jsonify

from models import storage
from models.city import City
from models.user import User
from models.place import Place
from models.state import State
from models.review import Review
from api.v1.views import app_views
from models.amenity import Amenity

@app_views.route("/status")
def status():
    """returns json  describing the status of api"""
    return jsonify({"status": "OK"})


@app_views.route("/stats")
def stat():
    """endpoint retrieves number of each objects by type"""
    objects = {
        "amenities": Amenity,
        "cities": City,
        "places": Place,
        "reviews": Review,
        "states": State,
        "users": User,
    }

    return jsonify({obj:  storage.count(objects[obj]) for obj in objects})

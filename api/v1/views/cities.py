# #!/usr/bin/python3
"""view fo City objects handles all default RESTFUL API action"""
from models.city import City
from models.state import State

from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from werkzeug.exceptions import NotFound, MethodNotAllowed, BadRequest


# ALLOWED_METHODS = ["GET", "POST", "PUT", "DELETE"]


@app_views.route("/states/<state_id>/cities", methods=["GET"],
                 strict_slashes=False)
def cities_by_states(state_id=None):
    """retrieves city by states id"""
    state = storage.get(State, state_id)
    if state is not None:
        return jsonify([city.to_dict() for city in state.cities])

    else:
        abort(404)


@app_views.route("/cities/<city_id>", methods=["GET"], strict_slashes=False)
def get_city_byID(city_id=None):
    """endpoint fetch city corresponding id"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route("/cities/<city_id>", methods=["DELETE"], strict_slashes=False)
def remove_city_byID(city_id=None):
    """delete city with the corresponding city id"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({}), 200


@app_views.route("/states/<state_id>/cities", methods=["POST"],
                 strict_slashes=False)
def add_city(state_id=None):
    """create a new city"""
    state = storage.get(State, state_id)
    # print(f"##### HERE IS THE STATE ID {state_id}")
    if state is None:
        abort(404)

    data = request.get_json(silent=True)
    if data is None:
        return BadRequest(description="Not a JSON")
    if "name" not in data:
        raise BadRequest(description="Missing name")
    new_city = City(name=data["name"], state_id=state.id)
    new_city.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route("/cities/<city_id>", methods=["PUT"], strict_slashes=False)
def update_city(city_id):
    """update city"""

    ignore_keys = ("id", "state_id", "created_at", "updated_at")
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    data = request.get_json(silent=True)
    if data is None:
        raise BadRequest(description="Not a JSON")
    if "name" not in data:
        raise BadRequest(description="Missing name")
    for k, v in data.items():
        if k not in ignore_keys:
            setattr(city, k, v)
    storage.save()
    return jsonify(city.to_dict()), 200

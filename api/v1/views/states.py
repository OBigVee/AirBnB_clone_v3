#!/usr/bin/python3
"""state object handles all default REST action"""
from models import storage
from api.v1.views import app_views
from flask import jsonify, request
from models.state import State
from werkzeug.exceptions import NotFound, MethodNotAllowed, BadRequest

# all methods allowed on endpoint
ALLOWED_METHODS = ["GET", "POST", "DELETE", "PUT"]


@app_views.route("/states", methods=ALLOWED_METHODS)
@app_views.route("/states/<state_id>", methods=ALLOWED_METHODS)
def handle_states(state_id=None):
    """retrieve the list of all states from storage"""
    handlers = {
        "GET": get_states,
        "POST": add_state,
        "DELETE": remove_state,
        "PUT": update_state,
    }

    if request.method in handlers:
        return handlers[request.method](state_id)
    else:
        raise MethodNotAllowed(list(handlers.keys()))


def get_states(state_id=None):
    """get a state with it corresponding id if provided if not
    return list of all states
    """
    # get list of all states
    all_states = storage.all(State).values()
    if state_id:
        res = list(filter(lambda x: x.id == state_id, all_states))
        if res:
            return jsonify(res[0].to_dict())
        raise NotFound()

    all_states = list(map(lambda x: x.to_dict(), all_states))
    return jsonify(all_states)


def add_state(state_id=None):
    """add new state"""
    # if state_id is not None:
    data = request.get_json()
    if type(data) is not dict:
        raise BadRequest(description="Not a JSON")
    if "name" not in data:
        raise BadRequest(description="Missing name")
    new_state = State(**data)
    new_state.save()
    return jsonify(new_state.to_dict()), 201


def remove_state(state_id=None):
    """Removes a state with the given id"""
    all_states = storage.all(State).values()
    res = list(filter(lambda x: x.id == state_id, all_states))
    if res:
        storage.delete(res[0])
        storage.save()
        return jsonify({}), 200
    raise NotFound


def update_state(state_id=None):
    """Updates the state with the given id"""
    ignore_keys = ("id", "created_at", "updated_at")
    all_states = storage.all(State).values()
    res = list(filter(lambda x: x.id == state_id, all_states))
    if res:
        data = request.get_json()
        if not isinstance(data, dict):
            raise BadRequest(description="Not a JSON")
        old_state = res[0]
        for k, v in data.items():
            if k not in ignore_keys:
                setattr(old_state, k, v)
        old_state.save()
        return jsonify(old_state.to_dict()), 200
    raise NotFound()

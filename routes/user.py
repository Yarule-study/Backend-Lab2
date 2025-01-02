from flask import Blueprint, request, jsonify, abort
from db.DataController import DataController

api = Blueprint("user", __name__)
db = DataController("db/users.csv", ["id", "name"])

@api.route("/user/<user_id>", methods=["GET", "DELETE"])
def get_user(user_id):
    if request.method == "GET":
        user = db.find(user_id)
        if not user:
            abort(404, description="User not found")
        return jsonify(user)
    
    elif request.method == "DELETE":
        user = db.remove(user_id)
        if not user:
            abort(404, description="User not found")
        return jsonify(user)

@api.route("/user", methods=["POST"])
def add_user():
    json = request.json
    user_id = json.get("id")
    name = json.get("name")

    added = db.add(user_id, name)
    if not added:
        abort(409, description="User with this id already exists")
    
    return jsonify({"id": user_id, "name": name}), 201

@api.route("/users", methods=["GET"])
def get_all_users():
    return jsonify(db.read_all())

from flask import Blueprint, request, jsonify, abort
from db.DataController import DataController

api = Blueprint("category", __name__)
db = DataController("db/categories.csv", ["id", "name"])

@api.route("/", methods=["GET", "POST", "DELETE"])
def category():
    if request.method == "GET":
        return jsonify(db.read_all())
    
    json = request.json
    id = json.get("id")

    if request.method == "POST":
        name = json.get("name")
        added = db.add(id, name)
        if not added: abort(409)
        return jsonify({ "id": id, "name": name})
    
    found = db.remove(id)
    if not found: abort(404)
    return jsonify(found)

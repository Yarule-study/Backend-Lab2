from flask import Blueprint, request, jsonify, abort
from db.DataController import DataController
from db.entities import CategorySchema

api = Blueprint("category", __name__)
db = DataController("db/categories.csv", ["id", "name"])

@api.route("/", methods=["GET", "POST", "DELETE"])
def category():
    if request.method == "GET":
        return jsonify(db.read_all())
    
    json = request.json
    id = json.get("id")

    if request.method == "POST":
        try:
            category_schema = CategorySchema()
            params = category_schema.load(json)
            added = db.add(*params.values())
            if not added: abort(409)
            return jsonify(record_schema.dump(params)), 201
        except:
            return jsonify({"errors": err.messages}), 400
    
    found = db.remove(id)
    if not found: abort(404)
    return jsonify(found)

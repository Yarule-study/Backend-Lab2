from flask import Blueprint, request, jsonify, abort
from db.DataController import DataController
from datetime import datetime

api = Blueprint("record", __name__)
db = DataController("db/records.csv", ["id", "user_id", "category_id", "timestamp", "spent"])

@api.route("/", methods=["GET", "POST"])
def record_action():
    if request.method == "GET":
        user_id = request.args.get("user_id")
        category_id = request.args.get("category_id")
        
        if not user_id and not category_id:
            abort(400, description="Both user_id and category_id cannot be empty")
        
        records = db.read()
        filtered = []
        for record in records:
            user_match = user_id and record["user_id"] == user_id
            category_match = category_id and record["category_id"] == category_id

            if (user_id and category_id and user_match and category_match) or \
               (user_id and user_match) or \
               (category_id and category_match):
                filtered.append(record)

        return jsonify(filtered)

    params = {key: request.json.get(key) for key in ["id", "user_id", "category_id", "spent"]}
    params["timestamp"] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    added = db.add(*params.values())
    if not added: abort(409)
    return jsonify(params)

@api.route("/<record_id>", methods=["GET", "DELETE"])
def record_id_action(record_id):
    record = db.find(record_id) if request.method == "GET" else db.remove(record_id)
    if not record: abort(404)
    return jsonify(record)

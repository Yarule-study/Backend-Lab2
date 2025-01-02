from flask import Blueprint, request, jsonify

api = Blueprint("routes", __name__)

@api.route("/test", methods=["GET"])
def get_items():
    return jsonify([{"status": "working"}])

@api.route("/add", methods=["POST"])
def add_item():
    data = request.get_json()
    return jsonify({"status": "success", "data": data}), 201

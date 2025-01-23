from flask import Blueprint, request, jsonify, abort
from factory import db
from data_utils.models import CategoryModel
from flask_jwt_extended import jwt_required

api = Blueprint("category", __name__)


@jwt_required()
@api.route("/", methods=["GET", "POST", "DELETE"])
def category():
    if request.method == "GET":
        categories = CategoryModel.query.all()
        return jsonify([cat.to_dict() for cat in categories])

    json_data = request.json
    if not json_data:
        abort(400, "Request must contain JSON data")

    id = json_data.get("id")

    if request.method == "POST":
        name = json_data.get("name")
        if not name:
            abort(400, "Missing 'name' field")
        existing_category = CategoryModel.query.filter_by(name=name).first()
        if existing_category:
            abort(409, "Category with this name already exists")
        new_category = CategoryModel(name=name)
        db.session.add(new_category)
        db.session.commit()
        return jsonify(new_category.to_dict()), 201

    if request.method == "DELETE":
        if not id:
            abort(400, "Missing 'id' field")
        category = CategoryModel.query.get(id)
        if not category:
            abort(404, "Category not found")
        db.session.delete(category)
        db.session.commit()
        return jsonify({"message": "Category deleted", "id": id})

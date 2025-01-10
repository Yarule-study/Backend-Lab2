from flask import Blueprint, request, jsonify, abort
from factory import db
from db.models import UserModel

api = Blueprint("user", __name__)

@api.route("/user/<int:user_id>", methods=["GET", "DELETE"])
def user_action_id(user_id):
    user = UserModel.query.get(user_id)
    if not user:
        abort(404, "User not found")
    
    if request.method == "GET":
        return jsonify(user.to_dict())

    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted", "id": user_id})

@api.route("/user", methods=["POST"])
def add_user():
    json_data = request.json
    if not json_data:
        abort(400, "Missing JSON data")

    try:
        name = json_data["name"]
        existing_user = UserModel.query.filter_by(name=name).first()
        if existing_user:
            abort(409, "User with this name already exists")

        new_user = UserModel(name=name)
        db.session.add(new_user)
        db.session.commit()
        return jsonify(new_user.to_dict()), 201
    except KeyError:
        abort(400, "Missing 'name' field")
    except Exception as e:
        abort(500, str(e))

@api.route("/users", methods=["GET"])
def get_all_users():
    users = UserModel.query.all()
    return jsonify([user.to_dict() for user in users])
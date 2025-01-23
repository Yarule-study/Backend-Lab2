from flask import Blueprint, request, jsonify, abort
from factory import db
from data_utils.models import UserModel
from flask_jwt_extended import create_access_token, jwt_required
from passlib.hash import pbkdf2_sha256

api = Blueprint("user", __name__)


@jwt_required()
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

        password = json_data["password"]
        new_user = UserModel(
            name=name,
            password=pbkdf2_sha256.hash(json_data["password"]),
        )
        db.session.add(new_user)
        db.session.commit()
        return jsonify(new_user.to_dict()), 201
    except KeyError as e:
        abort(400, f"Missing field: {e}")
    except Exception as e:
        abort(500, str(e))

@api.route("/login", methods=["POST"])
def login():
    json_data = request.json
    if not json_data:
        abort(400, "Missing JSON data")

    try:
        name = json_data["name"]
        user = UserModel.query.filter_by(name=name).first()
        if not user or not pbkdf2_sha256.verify(json_data["password"], user.password):
            abort(401, "Invalid name or password")

        access_token = create_access_token(identity=user.id)
        return jsonify({"token": access_token}), 200
    except KeyError as e:
        abort(400, f"Missing field: {e}")
    except Exception as e:
        abort(500, str(e))

@jwt_required()
@api.route("/users", methods=["GET"])
def get_all_users():
    users = UserModel.query.all()
    return jsonify([user.to_dict() for user in users])

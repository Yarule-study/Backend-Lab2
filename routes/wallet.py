from flask import Blueprint, request, jsonify, abort
from factory import db
from data_utils.models import WalletModel
from flask_jwt_extended import jwt_required

api = Blueprint("wallet", __name__)


@jwt_required()
@api.route("/<int:wallet_id>", methods=["GET", "PUT", "DELETE"])
def wallet_action_id(wallet_id):
    wallet = WalletModel.query.get(wallet_id)
    if not wallet:
        abort(404, "Wallet not found")

    if request.method == "GET":
        return jsonify(wallet.to_dict())

    if request.method == "PUT":
        json_data = request.json
        if not json_data:
            abort(400, "Missing json data")
        try:
            wallet.money += json_data["money"]
            db.session.commit()
            return jsonify(wallet.to_dict())
        except KeyError:
            abort(400, "Missing 'money' field")
        except Exception as e:
            abort(500, str(e))

    db.session.delete(wallet)
    db.session.commit()
    return jsonify({"message": "Wallet deleted", "id": wallet_id})


@jwt_required()
@api.route("/", methods=["GET", "POST"])
def wallet_action():
    if request.method == "GET":
        return jsonify([wallet.to_dict() for wallet in WalletModel.query.all()])

    json_data = request.json
    if not json_data:
        abort(400, "Missing JSON data")

    try:
        user_id = json_data["user_id"]
        existing_wallet = WalletModel.query.filter_by(user_id=user_id).first()
        if existing_wallet:
            abort(409, "Wallet with this user already exists")
        new_wallet = WalletModel(user_id=user_id)
        db.session.add(new_wallet)
        db.session.commit()
        return jsonify(new_wallet.to_dict()), 201
    except KeyError:
        abort(400, "Missing 'user_id' field")
    except Exception as e:
        abort(500, str(e))

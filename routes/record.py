from flask import Blueprint, request, jsonify, abort
from factory import db
from data_utils.models import RecordModel, WalletModel
from flask_jwt_extended import jwt_required

api = Blueprint("record", __name__)

@jwt_required()
@api.route("/", methods=["GET", "POST"])
def record_action():
    if request.method == "GET":
        user_id = request.args.get("user_id")
        category_id = request.args.get("category_id")
        if not user_id and not category_id:
            abort(400, "Missing 'user_id' or 'category_id' parameter")
        
        query = RecordModel.query
        if user_id:
            query = query.filter_by(user_id=user_id)
        if category_id:
            query = query.filter_by(category_id=category_id)

        records = query.all()
        return jsonify([record.to_dict() for record in records])

    json_data = request.json
    if not json_data:
        abort(400, "Missing JSON data")

    try:
        user_id = json_data["user_id"]
        wallet = WalletModel.query.filter_by(user_id=user_id).first()
        
        if not wallet:
            abort(400, "User has no wallet")

        spent = json_data["spent"]

        if wallet.money < spent:
            abort(400, "Insufficient funds")

        wallet.money -= spent
        db.session.commit()
        
        new_record = RecordModel(
            user_id=user_id,
            category_id=json_data["category_id"],
            spent=spent
        )
        db.session.add(new_record)
        db.session.commit()
        return jsonify(new_record.to_dict()), 201
    except KeyError as e:
        abort(400, f"Missing field: {e}")
    except Exception as e:
        abort(500, str(e))

@jwt_required()
@api.route("/<int:record_id>", methods=["GET", "DELETE"])
def record_id_action(record_id):
    record = RecordModel.query.get(record_id)
    if not record:
        abort(404, "Record not found")
    
    if request.method == "GET":
        return jsonify(record.to_dict())

    db.session.delete(record)
    db.session.commit()
    return jsonify({"message": "Record deleted", "id": record_id})


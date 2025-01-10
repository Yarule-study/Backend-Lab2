from flask import Blueprint, request, jsonify, abort
from factory import db
from db.models import IncomeModel

api = Blueprint("income", __name__)

@api.route("/<int:income_id>", methods=["GET", "PUT", "DELETE"])
def income_action_id(income_id):
    income = IncomeModel.query.get(income_id)
    if not income:
        abort(404, "Income not found")
    
    if request.method == "GET":
        return jsonify(income.to_dict())
    
    if request.method == "PUT":
        json_data = request.json
        if not json_data:
            abort(400, "Missing json data")
        try:
            income.money += json_data["money"]
            db.session.commit()
            return jsonify(income.to_dict())
        except KeyError:
            abort(400, "Missing 'money' field")
        except Exception as e:
            abort(500, str(e))

    db.session.delete(income)
    db.session.commit()
    return jsonify({"message": "Income deleted", "id": income_id})

@api.route("/", methods=["GET", "POST"])
def income_action():
    if request.method == "GET":
        return jsonify([income.to_dict() for income in IncomeModel.query.all()])

    json_data = request.json
    if not json_data:
        abort(400, "Missing JSON data")

    try:
        user_id = json_data["user_id"]
        existing_income = IncomeModel.query.filter_by(user_id=user_id).first()
        if existing_income:
            abort(409, "Income with this user already exists")
        new_income = IncomeModel(user_id=user_id)
        db.session.add(new_income)
        db.session.commit()
        return jsonify(new_income.to_dict()), 201
    except KeyError:
        abort(400, "Missing 'user_id' field")
    except Exception as e:
        abort(500, str(e))
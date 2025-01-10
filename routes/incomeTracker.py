from flask import Blueprint, request, jsonify, abort
from factory import db
from data_utils.models import IncomeTrackerModel

api = Blueprint("incomeTracker", __name__)

@api.route("/<int:incomeTracker_id>", methods=["GET", "PUT", "DELETE"])
def incomeTracker_action_id(incomeTracker_id):
    incomeTracker = IncomeTrackerModel.query.get(incomeTracker_id)
    if not incomeTracker:
        abort(404, "IncomeTracker not found")
    
    if request.method == "GET":
        return jsonify(incomeTracker.to_dict())
    
    if request.method == "PUT":
        json_data = request.json
        if not json_data:
            abort(400, "Missing json data")
        try:
            incomeTracker.money += json_data["money"]
            db.session.commit()
            return jsonify(incomeTracker.to_dict())
        except KeyError:
            abort(400, "Missing 'money' field")
        except Exception as e:
            abort(500, str(e))

    db.session.delete(incomeTracker)
    db.session.commit()
    return jsonify({"message": "IncomeTracker deleted", "id": incomeTracker_id})

@api.route("/", methods=["GET", "POST"])
def incomeTracker_action():
    if request.method == "GET":
        return jsonify([incomeTracker.to_dict() for incomeTracker in IncomeTrackerModel.query.all()])

    json_data = request.json
    if not json_data:
        abort(400, "Missing JSON data")

    try:
        user_id = json_data["user_id"]
        existing_incomeTracker = IncomeTrackerModel.query.filter_by(user_id=user_id).first()
        if existing_incomeTracker:
            abort(409, "IncomeTracker with this user already exists")
        new_incomeTracker = IncomeTrackerModel(user_id=user_id)
        db.session.add(new_incomeTracker)
        db.session.commit()
        return jsonify(new_incomeTracker.to_dict()), 201
    except KeyError:
        abort(400, "Missing 'user_id' field")
    except Exception as e:
        abort(500, str(e))
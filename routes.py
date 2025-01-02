from flask import Blueprint, request, jsonify, abort

api = Blueprint("routes", __name__)

@api.route("/user/<user_id>", methods=["GET", "DELETE"])
def get_user(user_id):
    if request.method == "DELETE":
        found = None
        with open("db/users.csv", "r") as f:
            file = f.readlines()

        with open("db/users.csv", "w") as f:
            for line in file:
                user_id_from_file, name = line.strip().split(",", 1)
                if user_id_from_file != user_id:
                    f.write(line)
                else:
                    found = {"id": user_id_from_file, "name": name}

        if not found:
            abort(404)

        return jsonify(found)

    with open("db/users.csv", "r") as file:
        for line in file:
            user_id_from_file, name = line.strip().split(",", 1)
            if user_id_from_file == user_id:
                return jsonify({"id": user_id_from_file, "name": name})

    abort(404)


@api.route("/user", methods=["POST"])
def add_user():
    json = request.json
    user_id = json.get("id")
    name = json.get("name")

    with open("db/users.csv", "r") as file:
        if any(line.split(",")[0] == user_id for line in file):
            abort(409)

    with open("db/users.csv", "a") as file:
        file.write(f"{user_id},{name}\n")

    return jsonify({"id": user_id, "name": name}), 201


@api.route("/users", methods=["GET"])
def get_all_users():
    userlist = []
    with open("db/users.csv", "r") as file:
        userlist = [{"id": line.split(",")[0], "name": line.strip().split(",", 1)[1]} for line in file]

    return jsonify(userlist)

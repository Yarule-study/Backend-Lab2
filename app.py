import os

from flask import jsonify
from routes.user import api as user
from routes.category import api as category
from routes.record import api as record
from routes.wallet import api as wallet
from factory import app, jwt

app.register_blueprint(user, url_prefix='/')
app.register_blueprint(category, url_prefix='/category')
app.register_blueprint(record, url_prefix='/record')
app.register_blueprint(wallet, url_prefix='/wallet')


@app.route('/', methods=['GET'])
def root():
    return jsonify({"status": "working"})


@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return (
        jsonify({"message": "The token has expired.", "error": "token_expired"}),
        401,
    )


@jwt.invalid_token_loader
def invalid_token_callback(error):
    return (
        jsonify(
            {"message": "Signature verification failed.", "error": "invalid_token"}
        ),
        401,
    )


@jwt.unauthorized_loader
def missing_token_callback(error):
    return (
        jsonify(
            {
                "description": "Request does not contain an access token.",
                "error": "authorization_required",
            }
        ),
        401,
    )


if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT") or 5000, host="0.0.0.0")

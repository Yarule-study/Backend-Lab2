from flask import Flask, jsonify
from routes.user import api as user

app = Flask(__name__)

app.register_blueprint(user, url_prefix='/')

@app.route('/', methods=['GET'])
def root():
    return jsonify({"status": "working"})

if __name__ == '__main__':
    app.run(debug=True)

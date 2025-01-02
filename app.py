from flask import Flask, jsonify
from routes import api

app = Flask(__name__)

app.register_blueprint(api, url_prefix='/')

@app.route('/', methods=['GET'])
def hello_world():
    return jsonify({"status": "working"})

if __name__ == '__main__':
    app.run(debug=True)
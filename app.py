from flask import Flask, jsonify
from routes.user import api as user
from routes.category import api as category
from routes.record import api as record

app = Flask(__name__)

app.register_blueprint(user, url_prefix='/')
app.register_blueprint(category, url_prefix='/category')
app.register_blueprint(record, url_prefix='/record')

@app.route('/', methods=['GET'])
def root():
    return jsonify({"status": "working"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

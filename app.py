import os

from flask import jsonify
from routes.user import api as user
from routes.category import api as category
from routes.record import api as record
from routes.income import api as income
from factory import app

app.register_blueprint(user, url_prefix='/')
app.register_blueprint(category, url_prefix='/category')
app.register_blueprint(record, url_prefix='/record')
app.register_blueprint(income, url_prefix='/income')

@app.route('/', methods=['GET'])
def root():
    return jsonify({"status": "working"})

if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT") or 5000, host="0.0.0.0")
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_pyfile('./options.py', silent=True)

db = SQLAlchemy(app)
migrate = Migrate(app, db)
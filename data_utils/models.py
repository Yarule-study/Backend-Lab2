from factory import db
from sqlalchemy import func

class UserModel(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)

    record = db.relationship("RecordModel", back_populates="user", lazy="dynamic")
    wallet = db.relationship("WalletModel", back_populates="user", lazy="dynamic")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name
        }

class WalletModel(db.Model):
    __tablename__ = "wallet"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey("user.id"), unique=False, nullable=False
    )
    money = db.Column(db.Float(precision=2), unique=False, nullable=False, default=0)

    user = db.relationship("UserModel", back_populates="wallet")

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "money": self.money
        }

class CategoryModel(db.Model):
    __tablename__ = "category"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True, nullable=False)

    record = db.relationship("RecordModel", back_populates="category", lazy="dynamic")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name
        }


class RecordModel(db.Model):
    __tablename__ = "record"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey("user.id"), unique=False, nullable=False
    )
    category_id = db.Column(
        db.Integer, db.ForeignKey("category.id"), unique=False, nullable=False
    )

    timestamp = db.Column(db.TIMESTAMP, server_default=func.now())
    spent = db.Column(db.Float(precision=2), unique=False, nullable=False)

    user = db.relationship("UserModel", back_populates="record")
    category = db.relationship("CategoryModel", back_populates="record")

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "category_id": self.category_id,
            "spent": self.spent,
        }

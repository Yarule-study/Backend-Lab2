from marshmallow import Schema, fields, validate

class UserSchema:
    id = fields.Int(dump_only=True, validate=validate.Range(min=1))
    name = fields.Str(required=True)

class CategorySchema:
    id = fields.Int(dump_only=True, validate=validate.Range(min=1))
    name = fields.Str(required=True)

class RecordSchema:
    id = fields.Int(dump_only=True, validate=validate.Range(min=1))
    user_id = fields.Int(required=True, validate=validate.Range(min=1))
    category_id = fields.Int(required=True, validate=validate.Range(min=1))
    timestamp = fields.DateTime(format="%d/%m/%Y %H:%M:%S", dump_only=True)
    spent = fields.Float(required=True, validate=validate.Range(min=0))

class IncomeSchema:
    id = fields.Int(dump_only=True, validate=validate.Range(min=1))
    money = fields.Float(required=True, validate=validate.Range(min=0))
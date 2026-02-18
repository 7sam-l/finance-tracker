from marshmallow import Schema, fields, validate, validates, ValidationError
from datetime import date


class CategorySchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=1, max=50))
    type = fields.Str(required=True, validate=validate.OneOf(["income", "expense"]))


class TransactionSchema(Schema):
    id = fields.Int(dump_only=True)
    amount = fields.Decimal(required=True, places=2, as_string=False)
    description = fields.Str(required=True, validate=validate.Length(min=1, max=200))
    type = fields.Str(required=True, validate=validate.OneOf(["income", "expense"]))
    date = fields.Date(required=True)
    created_at = fields.DateTime(dump_only=True)
    category_id = fields.Int(required=True, load_only=True)
    category = fields.Nested(CategorySchema, dump_only=True)

    @validates("amount")
    def validate_amount(self, value):
        if value <= 0:
            raise ValidationError("Amount must be greater than zero.")

    @validates("date")
    def validate_date(self, value):
        if value > date.today():
            raise ValidationError("Date cannot be in the future.")


transaction_schema = TransactionSchema()
transactions_schema = TransactionSchema(many=True)
category_schema = CategorySchema()
categories_schema = CategorySchema(many=True)

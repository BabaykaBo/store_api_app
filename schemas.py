from marshmallow import Schema, fields

# Plain


class PlainItemSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.Str(required=True)
    price = fields.Float(required=True)


class PlainStoreSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.Str(required=True)


class PlainTagSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.Str(required=True)


# Item


class ItemSchema(PlainItemSchema):
    store_id = fields.Integer(required=True, load_only=True)
    store = fields.Nested(PlainStoreSchema(), dump_only=True)


class ItemUpdateSchema(Schema):
    name = fields.Str()
    price = fields.Float()


# Store


class StoreSchema(PlainStoreSchema):
    items = fields.List(fields.Nested(PlainItemSchema()), dump_only=True)
    tags = fields.List(fields.Nested(PlainTagSchema()), dump_only=True)


# Tag


class TagSchema(PlainTagSchema):
    store_id = fields.Integer(required=True, dump_only=True)
    store = fields.Nested(PlainStoreSchema(), dump_only=True)


class TagUpdateSchema(Schema):
    name = fields.Str()

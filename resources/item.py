from db import db
from sqlalchemy.exc import SQLAlchemyError
from models.item import ItemModel
from flask_smorest import abort, Blueprint
from flask.views import MethodView
from flask_jwt_extended import jwt_required
from schemas import ItemSchema, ItemUpdateSchema

blp = Blueprint("items", __name__, description="Operations on items")


@blp.route("/items/<int:item_id>")
class Item(MethodView):
    @jwt_required()
    @blp.response(200, ItemSchema)
    def get(self, item_id):
        return ItemModel.query.get_or_404(item_id)

    @jwt_required()
    @blp.response(204)
    @blp.arguments(ItemUpdateSchema)
    def put(self, item_data, item_id):
        item = ItemModel.query.get_or_404(item_id)

        if "price" in item_data:
            item.price = item_data["price"]

        if "name" in item_data:
            item.name = item_data["name"]
            
        if "description" in item_data:
            item.description = item_data["description"]

        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="Error while updating item!")

        return None

    @jwt_required(fresh=True)
    @blp.response(204)
    def delete(self, item_id):
        item = ItemModel.query.get_or_404(item_id)
        try:
            db.session.delete(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="Error while deleting item!")

        return None


@blp.route("/items")
class ItemList(MethodView):
    @jwt_required()
    @blp.response(200, ItemSchema(many=True))
    def get(self):
        return ItemModel.query.all()

    @jwt_required()
    @blp.response(201, ItemSchema())
    @blp.arguments(ItemSchema)
    def post(self, item_data):
        item = ItemModel(**item_data)

        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="Error while creating item!")

        return item

from resources.helper import create_id
from flask import request
from flask_smorest import abort, Blueprint
from flask.views import MethodView
from db import items, stores

blp = Blueprint("items", __name__, description="Operations on items")


@blp.route("/items/<string:item_id>")
class Item(MethodView):
    def get(self, item_id):
        if item_id in items:
            return items[item_id]

        abort(404, message="Item not found")

    def put(self, item_id):
        item_data = request.get_json()
        price = item_data["price"] if "price" in item_data else None
        name = item_data["name"] if "name" in item_data else None

        if not price and not name:
            abort(
                400,
                message="Bad request. Ensure 'price' or 'name' are included in the JSON payload.",
            )

        if item_id in items:
            if name:
                items[item_id]["name"] = name

            if price:
                items[item_id]["price"] = price

            return "", 204
        else:
            abort(404, message="Item not found")

    def delete(self, item_id):
        if item_id in items:
            del items[item_id]
            return "", 204

        abort(404, message="Item not found")


@blp.route("/items")
class ItemList(MethodView):
    def get(self):
        return {"items": list(items.values())}

    def post(self):
        item_data = request.get_json()
        if (
            "price" not in item_data
            or "store_id" not in item_data
            or "name" not in item_data
        ):
            abort(
                400,
                message="Bad request. Ensure 'price', 'store_id', and 'name' are included in the JSON payload.",
            )

        for item in items.values():
            if (
                item_data["name"] == item["name"]
                and item_data["store_id"] == item["store_id"]
            ):
                abort(400, message="Item already exists.")

        if item_data["store_id"] not in stores:
            abort(404, message="Store not found")

        item_id = create_id()
        item = {**item_data, "id": item_id}
        items[item_id] = item

        return item, 201

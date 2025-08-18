from resources.helper import create_id
from flask import request
from flask_smorest import abort, Blueprint
from flask.views import MethodView
from db import stores
from schemas import StoreSchema

blp = Blueprint("stores", __name__, description="Operations on stores")


@blp.route("/stores/<string:store_id>")
class Store(MethodView):
    def get(self, store_id):
        if store_id in stores:
            return stores[store_id]

        abort(404, message="Store not found")

    def delete(self, store_id):
        if store_id in stores:
            del stores[store_id]
            return "", 204

        abort(404, message="Store not found")


@blp.route("/stores")
class StoreList(MethodView):
    def get(self):
        return list(stores.values())

    @blp.arguments(StoreSchema)
    def post(self, store_data):
        for store in stores.values():
            if store_data["name"] == store["name"]:
                abort(400, message=f"Store already exists.")

        store_id = create_id()
        new_store = {**store_data, "id": store_id}
        stores[store_id] = new_store
        return new_store, 201

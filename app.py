import uuid
from flask import Flask, request
from flask_smorest import abort
from db import stores, items

app: Flask = Flask(__name__)


def create_id() -> str:
    return uuid.uuid4().hex


# Stores


@app.get("/stores")
def get_stores():
    return list(stores.values())


@app.get("/stores/<string:store_id>")
def get_store(store_id):
    if store_id in stores:
        return stores[store_id]

    abort(404, message="Store not found")


@app.post("/stores")
def create_store():
    store_data = request.get_json()

    if "name" not in store_data:
        abort(
            400,
            message="Bad request. Ensure 'name' is included in the JSON payload.",
        )

    for store in stores.values():
        if store_data["name"] == store["name"]:
            abort(400, message=f"Store already exists.")

    store_id = create_id()
    new_store = {**store_data, "id": store_id}
    stores[store_id] = new_store
    return new_store, 201


# Items


@app.get("/items")
def get_all_items():
    return {"items": list(items.values())}


@app.get("/items/<string:item_id>")
def get_item(item_id):
    if item_id in items:
        return items[item_id]

    abort(404, message="Item not found")


@app.post("/items")
def create_item():
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

    return item

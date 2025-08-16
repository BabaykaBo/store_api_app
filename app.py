from typing import Any, List
import uuid
from flask import Flask, request
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

    return {"message": "Not Found"}, 404


@app.post("/stores")
def create_store():
    store_data = request.get_json()
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

    return {"message": "Item not found"}, 404


@app.post("/items")
def create_item():
    item_data = request.get_json()
    if item_data["store_id"] not in stores:
        return {"message": "Store not found"}, 404

    item_id = create_id()
    item = {**item_data, "id": item_id}
    items[item_id] = item

    return item

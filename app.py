from typing import Any, List
from flask import Flask, request

app: Flask = Flask(__name__)

stores: List[dict[str, Any]] = [
    {"name": "Stores", "items": [{"name": "Chair", "price": 15.99}]}
]

# Stores


@app.get("/stores")
def get_stores():
    return {"stores": stores}


@app.get("/stores/<string:name>")
def get_store(name):
    for store in stores:
        if store["name"] == name:
            return store

    return {"message": "Not Found"}, 404


@app.post("/stores")
def create_store():
    request_data = request.get_json()
    new_store = {"name": request_data["name"], "items": []}
    stores.append(new_store)
    return new_store, 201


# Items
@app.get("/stores/<string:name>/items")
def get_items(name):
    for store in stores:
        if store["name"] == name:
            return {"items": store["items"]}

    return {"message": "Not Found"}, 404


@app.post("/stores/<string:name>/items")
def create_item(name: str):
    request_data = request.get_json()
    for store in stores:
        if store["name"] == name:
            new_item = {"name": request_data["name"], "price": request_data["price"]}
            store["items"].append(new_item)
            return new_item

    return {"message": "Not Found"}, 404

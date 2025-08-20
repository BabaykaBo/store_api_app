import os
from dotenv import load_dotenv

from flask import Flask, jsonify
from flask_smorest import Api
from flask_jwt_extended import JWTManager

from db import db
from models.item import ItemModel
from models.store import StoreModel

from resources.item import blp as ItemBlp
from resources.store import blp as StoreBlp
from resources.tag import blp as TagBlp
from resources.user import blp as UserBlp


def create_app(db_url=None):
    app: Flask = Flask(__name__)

    load_dotenv()

    app = Flask(__name__)
    app.config["API_TITLE"] = "Stores REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = (
        "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    )
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or "sqlite:///data.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "1234")

    db.init_app(app)

    api = Api(app)

    jwt = JWTManager(app)

    jwt.expired_token_loader(
        lambda jwt_header, jwt_payload: (
            jsonify({"message": "Token expired", "error": "token_expired"}),
            401,
        )
    )

    jwt.invalid_token_loader(
        lambda error: (
            jsonify({"message": "Token invalid", "error": "invalid_token"}),
            401,
        )
    )

    jwt.unauthorized_loader(
        lambda error: (
            jsonify(
                {
                    "message": "Unauthorized request! Request must contain access token",
                    "error": "unauthorized_request",
                }
            ),
            401,
        )
    )

    with app.app_context():
        db.create_all()

    api.register_blueprint(ItemBlp)
    api.register_blueprint(StoreBlp)
    api.register_blueprint(TagBlp)
    api.register_blueprint(UserBlp)

    return app

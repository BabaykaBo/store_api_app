from db import db
from sqlalchemy.exc import SQLAlchemyError
from models.user import UserModel
from flask_smorest import abort, Blueprint
from flask.views import MethodView
from schemas import UserSchema
from passlib.hash import pbkdf2_sha256

blp = Blueprint("users", __name__, description="Operations on users")


@blp.route("/register")
class UserRegister(MethodView):
    @blp.response(200)
    @blp.arguments(UserSchema)
    def post(self, user_data):
        pass
from db import db
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from models.user import UserModel
from flask_smorest import abort, Blueprint
from flask.views import MethodView
from schemas import UserSchema
from passlib.hash import pbkdf2_sha256 as phs256

blp = Blueprint("users", __name__, description="Operations on users")


@blp.route("/register")
class UserRegister(MethodView):
    @blp.response(201, UserSchema)
    @blp.arguments(UserSchema)
    def post(self, user_data):
        if UserModel.query.filter(UserModel.username == user_data["username"]).first():
            abort(409, message="User with that username already exists!")

        user = UserModel(
            username=user_data["username"], password=phs256.hash(user_data["password"])  # type: ignore
        )
        try:
            db.session.add(user)
            db.session.commit()
        except IntegrityError:
            abort(409, message="User with that username already exists!")
        except SQLAlchemyError:
            abort(500, message="Error while creating store!")

        return user

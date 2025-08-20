from db import db
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from models.user import UserModel
from flask_smorest import abort, Blueprint
from flask.views import MethodView
from schemas import UserSchema, UserAuthSchema
from passlib.hash import pbkdf2_sha256 as phs256
from flask_jwt_extended import create_access_token

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


@blp.route("/login")
class UserLogin(MethodView):
    @blp.response(200, UserAuthSchema)
    @blp.arguments(UserSchema)
    def post(self, user_data):
        user = UserModel.query.filter(
            UserModel.username == user_data["username"]
        ).first()

        if user and phs256.verify(user_data["password"], user.password):
            access_token = create_access_token(identity=str(user.id))
        else:
            abort(401, message="Invalid username or password!")

        return {**user_data, "access_token": access_token}

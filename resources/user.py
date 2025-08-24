from db import db
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from models.user import UserModel
from models.revoked_token import RevokedTokenModel
from flask_smorest import abort, Blueprint
from flask.views import MethodView
from schemas import UserSchema, UserAuthSchema, AccessTokenSchema
from passlib.hash import pbkdf2_sha256 as phs256
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    jwt_required,
    get_jwt,
)

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
            access_token = create_access_token(identity=str(user.id), fresh=True)
            refresh_token = create_refresh_token(identity=str(user.id))
        else:
            abort(401, message="Invalid username or password!")

        return {
            **user_data,
            "access_token": access_token,
            "refresh_token": refresh_token,
        }


@blp.route("/refresh")
class RefreshToken(MethodView):
    @jwt_required(refresh=True)
    @blp.response(200, AccessTokenSchema)
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {"access_token": new_token}


@blp.route("/logout")
class UserLogout(MethodView):
    @jwt_required()
    @blp.response(204)
    def post(self):
        jti = get_jwt()["jti"]

        if RevokedTokenModel.query.filter_by(jti=jti).first():
            return None

        revoked_token = RevokedTokenModel(jti=jti)  # type: ignore

        try:
            db.session.add(revoked_token)
            db.session.commit()
        except IntegrityError:
            return None
        except SQLAlchemyError:
            abort(500, message="Error while logout!")

        return None

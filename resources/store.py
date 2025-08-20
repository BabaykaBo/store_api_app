from db import db
from models.store import StoreModel
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from flask_smorest import abort, Blueprint
from flask.views import MethodView
from schemas import StoreSchema

blp = Blueprint("stores", __name__, description="Operations on stores")


@blp.route("/stores/<int:store_id>")
class Store(MethodView):
    @blp.response(200, StoreSchema)
    def get(self, store_id):
        return StoreModel.query.get_or_404(store_id)

    @blp.response(204)
    def delete(self, store_id):
        store = StoreModel.query.get_or_404(store_id)

        try:
            db.session.delete(store)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="Error while deleting store!")
            
        return None


@blp.route("/stores")
class StoreList(MethodView):
    @blp.response(200, StoreSchema(many=True))
    def get(self):
        return StoreModel.query.all()

    @blp.response(201, StoreSchema)
    @blp.arguments(StoreSchema)
    def post(self, store_data):
        store = StoreModel(**store_data)

        try:
            db.session.add(store)
            db.session.commit()
        except IntegrityError:
            abort(400, message="A store with that name already exists!")
        except SQLAlchemyError:
            abort(500, message="Error while creating store!")

        return store

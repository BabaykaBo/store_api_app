from db import db
from models.item import ItemModel
from models.store import StoreModel
from models.tag import TagModel
from schemas import TagSchema, TagItemSchema
from flask_smorest import Blueprint, abort
from flask.views import MethodView
from sqlalchemy.exc import SQLAlchemyError

blp = Blueprint("tags", __name__, description="Operations on tags")


@blp.route("/stores/<int:store_id>/tags")
class StoreTag(MethodView):
    @blp.response(200, TagSchema(many=True))
    def get(self, store_id):
        return StoreModel.query.get_or_404(store_id).tags.all()

    @blp.response(201, TagSchema)
    @blp.arguments(TagSchema)
    def post(self, tag_data, store_id):
        StoreModel.query.get_or_404(store_id)

        if TagModel.query.filter(
            TagModel.store_id == store_id, TagModel.name == tag_data["name"]
        ).first():
            abort(400, message="Tag with that name already exists for this store!")

        tag = TagModel(**tag_data, store_id=store_id)  # type: ignore

        try:
            db.session.add(tag)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="Error occurred while creating tag!")

        return tag


@blp.route("/items/<int:item_id>/tags/<int:tag_id>")
class LinkTagsToItem(MethodView):
    @blp.response(201, TagSchema)
    def post(self, item_id, tag_id):
        item = ItemModel.query.get_or_404(item_id)
        tag = TagModel.query.get_or_404(tag_id)

        if item.store_id != tag.store_id:
            abort(400, message="Can only link items and tags from the same store.")

        try:
            item.tags.append(tag)
            db.session.add(tag)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="Error occurred while linking tag and item!")

        return tag

    @blp.response(200, TagItemSchema)
    def delete(self, item_id, tag_id):
        item = ItemModel.query.get_or_404(item_id)
        tag = TagModel.query.get_or_404(tag_id)

        if item.store_id != tag.store_id:
            abort(400, message="Can only unlink items and tags from the same store.")

        try:
            item.tags.remove(tag)
            db.session.add(tag)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="Error occurred while unlinking tag and item!")

        return {"message": "Item removed from tag", "tag": tag, "item": item}

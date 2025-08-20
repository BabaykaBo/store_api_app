from db import db

items_tags = db.Table(
    "items_tags",
    db.Column("item_id", db.Integer, db.ForeignKey("items.id", ondelete="CASCADE"), primary_key=True),
    db.Column("tag_id", db.Integer, db.ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True),
)
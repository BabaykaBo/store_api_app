import datetime
from db import db


class RevokedTokenModel(db.Model):
    __tablename__ = "revoked_tokens"

    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String, unique=True, nullable=False) 
    revoked_at = db.Column(
        db.DateTime,
        default=datetime.datetime.now(datetime.timezone.utc),
        nullable=False,
    )

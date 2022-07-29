from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSON

db = SQLAlchemy()

class Photo(db.Model):
    """ image metadata information"""
    __tablename__ = 'images'

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )
    tags = db.Column(
        db.String
    )

    exif_data = db.Column(
        db.JSON
    )
    filename = db.Column(
        db.String
    )

def connect_db(app):
    db.app = app
    db.init_app(app)

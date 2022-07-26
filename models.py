from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Image(db.model):
    """ image metadata information"""
    __tablename__ = 'images'

    id = db.Column(
        db.Integer,
        primary_key=True,
        auto_increment=True
    )

    make = db.Column(
        db.string
    )
    model = db.Column(
        db.string
    )
    latitude = db.Column(
        db.string
    )

    longitude = db.Column(
        db.string
    )

    file_size = db.Column(
        db.string
    )
    MIME_type = db.Column(
        db.string
    )

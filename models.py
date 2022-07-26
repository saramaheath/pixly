from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Image(db.Model):
    """ image metadata information"""
    __tablename__ = 'images'

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    make = db.Column(
        db.String
    )
    model = db.Column(
        db.String
    )
    latitude = db.Column(
        db.String
    )

    longitude = db.Column(
        db.String
    )

    file_size = db.Column(
        db.String
    )
    MIME_type = db.Column(
        db.String
    )

def connect_db(app):
    db.app = app
    db.init_app(app)


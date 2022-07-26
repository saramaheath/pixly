import os
#from dotenv import load_dotenv

from flask import Flask
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError


from models import db, connect_db

# load_dotenv()

app = Flask(__name__)

# Get DB_URI from environ variable (useful for production/testing) or,
# if not set there, use development local db.

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///pixly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "SECRET!"
toolbar = DebugToolbarExtension(app)


connect_db(app)


@app.get('/images')
def get_images():
    """return json of all images"""


@app.post('/images/upload')
def add_image():
    """adds image to database and s3, returns json of that image data"""


@app.get('/images/<int:image_id>')
def get_image():
    """return json of one image"""


@app.get('/images/<tag>')
def get_images_by_tag():
    """returns json of all images that share tag"""


@app.patch('/images/<int:image_id>')
def edit_image():
    """edits image, return json of that new image data"""

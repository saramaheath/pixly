import os
from dotenv import load_dotenv

from flask import Flask, render_template, request, flash, redirect, session, g
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError

from forms import UserAddForm, LoginForm, MessageForm, CSRFProtectForm, UserEditForm
from models import db, connect_db, User, Message

load_dotenv()

app = Flask(__name__)

# Get DB_URI from environ variable (useful for production/testing) or,
# if not set there, use development local db.
app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ['DATABASE_URL'].replace("postgres://", "postgresql://"))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
toolbar = DebugToolbarExtension(app)


connect_db(app)


@app.get('/images')
def get_images():
    """return json of all images"""

@app.post('/images')
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




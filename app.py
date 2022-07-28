from contextlib import redirect_stderr
from email.mime import image
import os
from dotenv import load_dotenv

from flask import Flask, jsonify, request, render_template, redirect
from flask_cors import CORS
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError
from sqlalchemy.dialects.postgresql import JSON
from PIL import Image, ExifTags
from PIL.ExifTags import TAGS
import boto3
from werkzeug.utils import secure_filename
from models import db, connect_db

load_dotenv()

app = Flask(__name__)
CORS(app, origins=['http://localhost:3000'])

# Get DB_URI from environ variable (useful for production/testing) or,
# if not set there, use development local db.

BASE_URL = os.environ['BASE_URL']
AWS_SECRET_KEY = os.environ['AWS_SECRET_KEY']
AWS_ACCESS_KEY_ID = os.environ['AWS_SECRET_KEY_ID']
BUCKET_NAME = os.environ['BUCKET_NAME']
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///pixly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
#toolbar = DebugToolbarExtension(app)

s3 = boto3.client('s3',
                  aws_access_key_id=AWS_ACCESS_KEY_ID,
                  aws_secret_access_key=AWS_SECRET_KEY

                  )
connect_db(app)


@app.route('/')
def home():
    return redirect('/list')


@app.get('/list')
def get_images():
    """return json of all images"""
    image_urls = []
    for item in s3.list_objects(Bucket=BUCKET_NAME)['Contents']:
        image_urls.append(f"{BASE_URL}{item['Key']}")

    return render_template("home.html", image_urls=image_urls)


@app.route('/upload', methods=['post'])
def upload():
    """stores exif data into database, uploads image file to s3 bucket"""
    if request.method == 'POST':
        img = request.files['file']
        if img:
            filename = secure_filename(img.filename)
            img.save(filename)
            s3.upload_file(
                Bucket=BUCKET_NAME,
                Filename=filename,
                Key=filename
            )
            image_source = f"{BASE_URL}{filename}"
            msg = "Upload Done ! "

    image = Image.open(filename)
    print(image, 'image^^^^^^^^^^')

    exifdata = image.getexif()
    print(exifdata, 'exifdata&&&&&&&&&&&')

    exif_obj = {}

    # json object to store exif
    for key, val in exifdata.items():
        if key in ExifTags.TAGS:
            exif_obj[ExifTags.TAGS[key]] = val

    print(exif_obj, '!!!!!!!!!')

    return render_template("home.html", msg=msg, image_source=image_source)


# @app.post('/images/upload')
# def add_image():
#     """adds image to database and s3, returns image to display to user,
#     confirming image was added"""

    # img = request.files['file']
    # if img:
    #             filename = secure_filename(img.filename)
    #             img.save(filename)
    #             s3.upload_file(
    #                 Bucket = BUCKET_NAME,
    #                 Filename=filename,
    #                 Key = filename
    #             )
    #             msg = "Upload Done!"
    # return jsonify('hi')


@app.get('/images/<int:image_id>')
def get_image():
    """return image to display to user"""


@app.get('/images/<tag>')
def get_images_by_tag():
    """returns all images to display that share tag"""


@app.patch('/images/<int:image_id>')
def edit_image():
    """edits image, return new image to display to user with edits complete"""

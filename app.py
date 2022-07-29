from contextlib import redirect_stderr
from email.mime import image
import os
from dotenv import load_dotenv
import json

from flask import Flask, jsonify, request, render_template, redirect
from flask_cors import CORS
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError
from sqlalchemy.dialects.postgresql import JSON
from PIL import Image, ExifTags, TiffImagePlugin
from PIL.ExifTags import TAGS
import boto3
from werkzeug.utils import secure_filename
from models import db, connect_db, Photo

load_dotenv()

app = Flask(__name__)
CORS(app, origins=['http://localhost:3000'])

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
    """redirects to '/list'"""
    return redirect('/list')

@app.get('/list')
def get_images():
    """Displays list of all images"""
    image_urls = []
    for item in s3.list_objects(Bucket=BUCKET_NAME)['Contents']:
        image_urls.append(f"{BASE_URL}{item['Key']}")

    return render_template("home.html", image_urls=image_urls)

@app.route('/upload', methods=['post'])
def upload():
    """stores exif data into database, uploads image file to s3 bucket, 
    displays page with list of images"""
    if request.method == 'POST':
        tag = request.form['tag']
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
    exifdata = image.getexif()
    exif_dict = {}

    for key, val in exifdata.items():
        if key in ExifTags.TAGS:
            if isinstance(val, TiffImagePlugin.IFDRational):
                val = float(val)
            exif_dict[ExifTags.TAGS[key]] = val

    json_dict = json.dumps(exif_dict)
    img = Photo(tags=tag, exif_data=json_dict, filename=filename)

    db.session.add(img)
    db.session.commit()

    return render_template("home.html", msg=msg, image_source=image_source)

@app.get('/images')
def get_images_by_tag():
    """displays all images that share tag from search"""
    tag = request.args.get('search')
    image_instances = Photo.query.filter(Photo.tags.like(f"%{tag}%")).all()

    image_urls = []
    for image in image_instances:
        image_url = image.filename
        image_urls.append(f"{BASE_URL}{image_url}")

    return render_template("home.html", image_urls=image_urls)

@app.patch('/images/<int:image_id>')
def edit_image():
    """edits image, return new image to display to user with edits complete"""

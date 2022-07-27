import os
#from dotenv import load_dotenv

from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError
from PIL import Image
from PIL.ExifTags import TAGS
import boto3
from werkzeug.utils import secure_filename
from models import db, connect_db

# load_dotenv()

app = Flask(__name__)
CORS(app, origins=['http://localhost:3000'])

# Get DB_URI from environ variable (useful for production/testing) or,
# if not set there, use development local db.

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///pixly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
os.environ['SECRET_KEY']
toolbar = DebugToolbarExtension(app)

s3 = boto3.client('s3',
                    aws_access_key_id='access key here',
                    aws_secret_access_key= 'secret key here',
                    aws_session_token='secret token here'
                     )

#BUCKET_NAME = os.environ['ENV_BUCKET_NAME'] 
connect_db(app)


@app.get('/images')
def get_images():
    """return json of all images"""
    #request to aws for images


@app.post('/images/upload')
def add_image():
    """adds image to database and s3, returns image to display to user,
    confirming image was added"""
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
    return jsonify('hi')



@app.get('/images/<int:image_id>')
def get_image():
    """return image to display to user"""



@app.get('/images/<tag>')
def get_images_by_tag():
    """returns all images to display that share tag"""


@app.patch('/images/<int:image_id>')
def edit_image():
    """edits image, return new image to display to user with edits complete"""


    #thepythoncode.com/article/extracting-image-metadata-in-python
    # needs file name like: 'image.jpg' for the open function call argument
    # image = Image.open()
    # #check what image has for data at this point before getexif()?
    # print(image)

    # # image_data = {
    # #     "tag": image.tag,
    # #     "make": image.make,
    # #     "model": image.model,
    # #     "latitude": image.latitude,
    # #     "longitude": image.longitude,
    # #     "file_size": image.file_size,
    # #     "MIME_type": image.MIME_type
    # # }
    # # for label,value in image_data.items():

    # exifdata = image.getexif()

    # for tag_id in exifdata:
    # # get the tag name, instead of human unreadable tag id
    #     tag = TAGS.get(tag_id, tag_id)
    #     data = exifdata.get(tag_id)
    # # decode bytes
    # if isinstance(data, bytes):
    #     data = data.decode()
    # print(f"{tag:25}: {data}")
    #image_data = { tag, make, model, latitude, longitude, file_size, MIME_type }
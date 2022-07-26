# run these tests like:
#
#    FLASK_ENV=production python -m unittest test_app_routes.py

import os
from unittest import TestCase

from models import db

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///pixly_test"

from app import app

app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

#creates test database
db.create_all()

class FlaskTestCase(TestCase):
    def setUp(self):
        #what ever we call our table .query.delete()

        u1 = User.signup("u1", "u1@email.com", "password", None)
        db.session.flush()

        m1 = Message(text="m1-text", user_id=u1.id)
        db.session.add_all([m1])
        db.session.commit()

        self.u1_id = u1.id
        self.m1_id = m1.id

        self.client = app.test_client()

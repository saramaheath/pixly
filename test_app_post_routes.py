from unittest import TestCase
from app import app, db
from models import Image
# testing users page functionality
# Let's configure our app to use a different database for tests
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///pixly_test"
# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True
# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']
# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data
db.create_all()


class FlaskTestCase(TestCase):
    def setUp(self):
        """Create test client, add sample data."""
        # As you add more models later in the exercise, you'll want to delete
        # all of their records before each test just as we're doing with the
        # User model below.
        Image.query.delete()
        self.client = app.test_client()
        test_image = Image(make="testmake1",
                           model="testmodel1",
                           latitude="testlat",
                           longitude="",
                           file_size="",
                           MIME_type="")
        second_image = Image(make="",
                             model="",
                             latitude="",
                             longitude="",
                             file_size="",
                             MIME_type="")

        db.session.add_all([test_image, second_image])
        db.session.commit()


    def tearDown(self):
        """Clean up any fouled transaction."""
        db.session.rollback()

    def test_list_images(self):
        with self.client as c:
            resp = c.post("/images/upload", data={"make": "testmake1",
                                                  "model": "testmodel1",
                                                  "latitude": "testlat",
                                                  "longitude": "",
                                                  "file_size": "",
                                                  "MIME_type": ""})
            self.assertEqual(resp.status_code, 302)

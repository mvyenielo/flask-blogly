"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

def connect_db(app):
    """Connect to database."""

    app.app_context().push()
    db.app = app
    db.init_app(app)

DEFAULT_IMAGE_URL = "https://as2.ftcdn.net/jpg/01/36/08/69/220_F_136086944_knpNCEhMDywOOD3Ggu0ufUC2L2D8BVFm.jpg"

class User(db.Model):
    __tablename__="users"

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True)

    first_name = db.Column(
        db.String(50),
        nullable=False)

    last_name = db.Column(
        db.String(50),
        nullable=False)

    # TODO: check for url validation method
    image_url = db.Column(
        db.Text,
        nullable=True,
        default= DEFAULT_IMAGE_URL
    )

# We are able to create a new instance of a user on our site, and it shows
# up in the database

# However, we cannot update or delete a user from our site and see the changes in the
# database, even though those changes are reflected on the site itself (for edits, not delete
# , get an error for delete)

# Also, when we manually add a user, our default image shows up in the database
# and on the site

# We get this error when we try to delete a user from the site:
# sqlalchemy.exc.InvalidRequestError: Object '<User at 0x105bd92d0>'
# is already attached to session '1' (this is '3')

# We tried moving anything updating db into the "models.py" doc rather than having
# it in the "app.py", and we're still getting the same error



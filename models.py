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

    image_url = db.Column(
        db.Text,
        nullable=True,
        default= DEFAULT_IMAGE_URL
    )




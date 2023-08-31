"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

def connect_db(app):
    """Connect to database."""

    app.app_context().push()
    db.app = app
    db.init_app(app)

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
        default=
        "https://as2.ftcdn.net/jpg/01/36/08/69/220_F_136086944_knpNCEhMDywOOD3Ggu0ufUC2L2D8BVFm.jpg"
    )

    def update_user(self,new_first,new_last,new_url):
        self.first_name = new_first
        self.last_name = new_last
        self.image_url = new_url
        db.session.commit()



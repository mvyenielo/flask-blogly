"""Blogly application."""

import os

from flask import Flask, request, redirect, render_template
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    "DATABASE_URL", 'postgresql:///blogly')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)

q = User.query

@app.get('/')
def render_user_list():
    """redirects to list of users"""

    return redirect('/users')

@app.get('/users')
def render_user_list():
    """Renders list of users/add user button"""

    users = q.all()

    return render_template('index.html',
                           users = users)

@app.get('/users/new')
def render_user_list():
    """"""

    users = q.all()

    render_template('user_new.html',
                    users = users)


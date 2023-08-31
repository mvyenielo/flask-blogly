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

# q = User.query

@app.get('/')
def redirect_user_list():
    """redirects to list of users"""

    return redirect('/users')

@app.get('/users')
def list_users():
    """Renders list of users/add user button"""

    users = User.query.all()

    return render_template('index.html',
                           users = users)

@app.get('/users/new')
def render_new_user_form():
    """"""

    users = User.query.all()

    return render_template('user_new.html',
                    users = users)

@app.post('/users/new')
def submit_new_user():
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url']

    new_user = User(first_name = first_name, last_name = last_name, image_url = image_url)
    db.session.add(new_user)
    db.session.commit()

    return redirect('/users')

@app.get('/users/<int:user_id>')
def show_user_info(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('user_detail.html', user = user)

@app.get('/users/<int:user_id>/edit')
def show_user_edit(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('user_edit.html', user = user)

@app.post('/users/<int:user_id>/edit')
def submit_user_edit(user_id):
    user = User.query.get_or_404(user_id)

    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']
    db.session.add(user)
    db.session.commit()

    return redirect('/users')

@app.post('/users/<int:user_id>/delete')
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect('/users')

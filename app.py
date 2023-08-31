"""Blogly application."""

import os

from flask import Flask, request, redirect, render_template
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    "DATABASE_URL", 'postgresql:///blogly')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)

q = User.query

@app.get('/')
def redirect_user_list():
    """redirects to list of users"""

    return redirect('/users')

@app.get('/users')
def render_user_list():
    """Renders list of users/add user button"""

    users = q.all()

    return render_template('index.html',
                           users = users)

@app.get('/users/new')
def render_new_user_form():
    """"""

    users = q.all()

    return render_template('user_new.html',
                    users = users)

@app.post('/users/new')
def submit_new_user():
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url']

    new_user = User(first_name = first_name, last_name = last_name, image_url = image_url)
    new_user.add_new_user()

    return redirect('/users')

@app.get('/users/<int:user_id>')
def show_user_info(user_id):
    user = q.get_or_404(user_id)
    return render_template('user_detail.html', user = user)

@app.get('/users/<int:user_id>/edit')
def show_user_edit(user_id):
    user = q.get_or_404(user_id)
    return render_template('user_edit.html', user = user)

@app.post('/users/<int:user_id>/edit')
def submit_user_edit(user_id):
    user = q.get_or_404(user_id)

    new_first = request.form['first_name']
    new_last = request.form['last_name']
    new_url = request.form['image_url']

    user.update_user(new_first,new_last,new_url)


    return redirect('/users')

@app.post('/users/<int:user_id>/delete')
def delete_user(user_id):
    user = q.get_or_404(user_id)

    user.delete_user()

    return redirect('/users')

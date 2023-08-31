"""Blogly application."""

import os

from flask import Flask, request, redirect, render_template
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, DEFAULT_IMAGE_URL

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    "DATABASE_URL", 'postgresql:///blogly')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)


@app.get('/')
def redirect_user_list():
    """redirects to list of users"""

    return redirect('/users')

# USER ROUTES BELOW

@app.get('/users')
def list_users():
    """Renders list of users/add user button"""

    users = User.query.all()

    return render_template('index.html',
                           users = users)

@app.get('/users/new')
def render_new_user_form():
    """renders form to add in new user"""

    users = User.query.all()

    return render_template('user_new.html',
                    users = users)
#Potentially have this render just a new user add form with no user list^

@app.post('/users/new')
def submit_new_user():
    """handles new user submit, redirects back to users page"""

    first_name = request.form['first_name']
    last_name = request.form['last_name']
    if request.form['image_url'] == '':
        image_url = None
    else:
        image_url = request.form['image_url']
    # image_url=request.form["image_url"] or None^

    new_user = User(first_name = first_name, last_name = last_name, image_url = image_url)
    db.session.add(new_user)
    db.session.commit()
    # Could flash a positive response 'user added!'
    return redirect('/users')

@app.get('/users/<int:user_id>')
def show_user_info(user_id):
    """renders user info"""

    user = User.query.get_or_404(user_id)
    posts = user.posts
    return render_template('user_detail.html', user = user,
                           posts = posts)

@app.get('/users/<int:user_id>/edit')
def show_user_edit(user_id):
    """renders the user edit page"""
    user = User.query.get_or_404(user_id)
    return render_template('user_edit.html', user = user)

@app.post('/users/<int:user_id>/edit')
def submit_user_edit(user_id):
    """handles user edit, updates database with new edits"""
    user = User.query.get_or_404(user_id)

    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']

    if request.form['image_url'] == '':
        user.image_url = DEFAULT_IMAGE_URL
    else:
        user.image_url = request.form['image_url']
        #TODO: Possibly replicate from above on add-new user^

    db.session.add(user)
    db.session.commit()

    return redirect('/users')

@app.post('/users/<int:user_id>/delete')
def delete_user(user_id):
    """Handles user delete, removes user from database"""
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect('/users')

# USER-POSTS ROUTES START HERE

@app.get('/users/<int:user_id>/posts/new')
def show_new_post_form(user_id):
    """renders new post form"""

    user = User.query.get_or_404(user_id)

    return render_template('post_new.html', user = user)

@app.post('/users/<int:user_id>/posts/new')
def submit_new_post(user_id):

    title = request.form['title']
    content = request.form['content']

    new_post = Post(title=title, content = content, user_id=user_id)
    db.session.add(new_post)
    db.session.commit()

    return redirect(f'/users/{user_id}')

@app.get('/posts/<int:post_id>')
def show_post(post_id):

    post = Post.query.get_or_404(post_id)
    return render_template('post_detail.html',post=post)

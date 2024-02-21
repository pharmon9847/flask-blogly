"""Blogly application."""

from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'supdog9876'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

toolbar = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

@app.route('/')
def root_page():
    """Shows list of posts, most recent first."""
    
    posts = Post.query.orderr_by(Post.created_at.desc()).limit(5).all()
    return redirect('posts/homepage.html', posts=posts)

@app.errorhandler(404)
def page_not_found(e):
    """Shows 404 page."""
    
    return render_template('404.html'), 404

# ###################### USER ROUTES ######################################

@app.route('/users')
def users_index():
    """Page with all users and their info"""
    
    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template('users/index.html', users=users)


@app.route('/users/new', methods=["GET"])
def users_new_form():
    """Form to create a new user"""
    
    return render_template('/users/new.html')


@app.route('/users/new', methods=["POST"])
def users_new():
    """handle form submission for new user"""
    
    new_user = User(
        first_name=request.form['first_name'],
        last_name=request.form['last_name'],
        image_url=request.form['image_url'] or None
    )
    
    db.session.add(new_user)
    db.session.commit()
    flash(f"User {new_user.full_name} has been added.")
    
    return redirect('/users')


@app.route('/users/<int:user_id>')
def users_show(user_id):
    """Page with specific user's info"""
    
    user = User.query.get_or_404(user_id)
    return render_template('users/show.html', user=user)


@app.route('/users/<int:user_id>/edit')
def users_edit(user_id):
    """form to edit existing user"""
    
    user = User.query.get_or_404(user_id)
    return render_template('/users/edit.html', user=user)


@app.route('/users/<int:user_id>/edit', methods=["POST"])
def users_update(user_id):
    """handle form submission for updating existing user"""
    
    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']
    
    db.session.add(user)
    db.session.commit()
    
    return redirect('/users')


@app.route('/users/<int:user_id>/delete', methods=["POST"])
def users_destroy(user_id):
    """handle form submission for deleting user"""
    
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash(f"User {user.full_name} has been deleted.")
    
    return redirect('/users')

# ########################## POSTS ROUTE #################################

@app.route('/users/<int:user_id>/posts/new')
def posts_new_form(user_id):
    """form to create a new post"""
    
    user = User.query.get_or_404(user_id)
    return render_template('posts.new.html', user=user)

@app.route('users/<int:user_id>/posts/new', methods=["POST"])
def posts_new(user_id):
    """handle form submission for creating new posts"""
    
    user = User.query.get_or_404(user_id)
    new_post = Post(title=request.form['title'],
                    content=request.form['content'],
                    user=user)
    
    de.session.add(new_post)
    db.session.commit()
    flash(f"Post '{new_post.title}' has been added.")
    
    return redirect(f"/users/{user_id}")

@app.route('/posts/<int:post_id>')
def posts_show(post_id):
    """shows info page on specific post"""
    
    post = Post.query.get_or_404(post_id)
    return render_template('posts/show.html', post=post)

@app.route('/posts/<int:post_id>/edit')
def posts_edit(post_id):
    """form to edit existing post"""
    
    post = Post.query.get_or_404(post_id)
    return render_template('posts/edit.html', post=post)

@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def posts_update(post_id):
    """handle form submission for updating post"""
    
    post = Post.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form['content']
    
    db.session.add(post)
    db.session.commit()
    flash(f"Post '{post.title}' has been edited.")
    
    return redirect(f"/users/{post.user_id}")

@app.route('/posts/<int:post_id>/delete', methods=["POST"])
def posts_destroy(post_id):
    """handle submission for deleting post"""
    
    post = Post.query.get_or_404(post_id)
    
    db.session.delete(post)
    db.session.commit()
    flash(f"Post '{post.title}' has been deleted.")
    
    return redirect(f"/users/{post.user_id}")
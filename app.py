from flask import Flask, request, redirect, render_template, flash
# from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, Tag
import psycopg2
import os
import sqlalchemy

# from sqlalchemy import create_engine
# engine = create_engine("postgresql+psycopg2://blogly_x519_user:PVGGb0k6fPqbGk9IjMNO48ZNBL1QYWRM@dpg-cng9ja0l6cac739mqv80-a.oregon-postgres.render.com:5432/blogly_x519")
app = Flask(__name__)


# import dj_database_url

# DATABASES = {
#     'default': dj_database_url.config(
#         default='postgres://blogly_x519_user:PVGGb0k6fPqbGk9IjMNO48ZNBL1QYWRM@dpg-cng9ja0l6cac739mqv80-a.oregon-postgres.render.com/blogly_x519',
#         conn_max_age=600,
#         conn_health_checks=True,
#     )
# }

# database_uri = "postgres://blogly_x519_user:PVGGb0k6fPqbGk9IjMNO48ZNBL1QYWRM@dpg-cng9ja0l6cac739mqv80-a/blogly_x519"

# host = "cloudpostgres.postgres.database.azure.com"
# dbname = "cloudpostgres"
# user = "postgres"
# password = "Getfuzzy@1"
# sslmode = "require"

# url_object = "host={0} user={1} dbname={2} password={3} sslmode={4}".format(host, user, dbname, password, sslmode)
# conn = psycopg2.connect(url_object)
# print("Connection established")

# database_url = "postgresl+psycopg2://mpzjqsja:W6DGKwNStfs0uhMwOG8oMozbdZEwo6u9@stampy.db.elephantsql.com:5432/mpzjqsja"

# from sqlalchemy import create_engine

# engine = create_engine('postgresql+psycopg2://mpzjqsja:2s8dz_Ae5V1hNjWUDIFYl8KQ8n20XJUK@stampy.db.elephantsql.com/mpzjqsja')

# url_object = psycopg2.connect(user="postgres", password="Getfuzzy@1", host="azure-db1.postgres.database.azure.com", port=5432, database="postgres")

# database_uri = psycopg2.connect(user="postgres", password="Getfuzzy@1", host="cloudpostgres.postgres.database.azure.com", port=5432, database="postgres")

from sqlalchemy import URL

# url_object = URL.create(
#     "postgresql+pg8000",
#     username="dbuser",
#     password="kx@jj5/g",  # plain (unescaped) text
#     host="pghost10",
#     database="appdb",
# )

# database_uri = "postgresl+psycopg2://blogly_x519_user:PVGGb0k6fPqbGk9IjMNO48ZNBL1QYWRM@dpg-cng9ja0l6cac739mqv80-a/blogly_x519"
database_uri = "postgresql+psycopg2://blogly_x519_user:PVGGb0k6fPqbGk9IjMNO48ZNBL1QYWRM@dpg-cng9ja0l6cac739mqv80-a.oregon-postgres.render.com:5432/blogly_x519"

# engine = create_engine(DB_URL, pool_pre_ping=True, pool_recycle=300)
# database_uri = 'postgresql+psycopg2://postgres:Getfuzzy1@127.0.0.1:5432/blogly'

# from sqlalchemy import create_engine

# engine = create_engine(url_object)

# from sqlalchemy import create_engine

# engine = create_engine('postgresql+psycopg2://postgres:Getfuzzy1@127.0.0.1:5050/blogly')

# from sqlalchemy import Session

# session = Session(engine)


# import inspect

# if not hasattr(inspect, 'getargspec'):
#     inspect.getargspec = inspect.getfullargspec


# app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql+psycopg2://admin:Getfuzzy1@database-1.czy6u4a2ykly.us-east-1.rds.amazonaws.com/database-1"
# connecting to pgadmin instead of postgres locally
# database_uri = 'postgresql+psycopg2://postgres:Getfuzzy1@127.0.0.1:5432/blogly'
# database_url = 'postgres://mpzjqsja:W6DGKwNStfs0uhMwOG8oMozbdZEwo6u9@stampy.db.elephantsql.com:5432/mpzjqsja'
# database_uri = 'psycopg2.connect(user="postgres", password="Getfuzzy1", host="azure-postgres1.postgres.database.azure.com", port=5432, database="postgres")'
# app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:Getfuzzy@1@azure-db-1.postgres.database.azure.com:5432/postgres"
app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'ihaveasecret'
# app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {"pool_pre_ping": True}  


env_config = os.getenv("PROD_APP_SETTINGS", "config.DevelopmentConfig")
app.config.from_object(env_config)

# app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

# toolbar = DebugToolbarExtension(app)

# args, varargs, keywords, defaults, foo, foo1, foo2 = inspect.getfullargspec(func)

connect_db(app)
# db.create_all()


@app.route('/')
def root():
    """Show list of posts, most-recent first."""

    posts = Post.query.order_by(Post.created_at.desc()).limit(10).all()
    return render_template("posts/homepage.html", posts=posts)


@app.errorhandler(404)
def page_not_found(e):
    """Show 404 NOT FOUND page."""

    return render_template('404.html'), 404


##################################### USER ROUTES #########################################

@app.route('/users')
def users_index():
    """Page with info on all users"""

    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template('users/index.html', users=users)


@app.route('/users/new', methods=["GET"])
def users_new_form():
    """Form to create a new user"""

    return render_template('users/new.html')


@app.route("/users/new", methods=["POST"])
def users_new():
    """Handle form submission for creating new user"""

    new_user = User(
        first_name=request.form['first_name'],
        last_name=request.form['last_name'],
        image_url=request.form['image_url'] or None)

    db.session.add(new_user)
    db.session.commit()
    flash(f"User {new_user.full_name} added.")

    return redirect("/users")


@app.route('/users/<int:user_id>')
def users_show(user_id):
    """Page with info on a specific user"""

    user = User.query.get_or_404(user_id)
    return render_template('users/show.html', user=user)


@app.route('/users/<int:user_id>/edit')
def users_edit(user_id):
    """Form to edit an existing user"""

    user = User.query.get_or_404(user_id)
    return render_template('users/edit.html', user=user)


@app.route('/users/<int:user_id>/edit', methods=["POST"])
def users_update(user_id):
    """Handle form submission for updating existing user"""

    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']

    db.session.add(user)
    db.session.commit()
    flash(f"User {user.full_name} edited.")

    return redirect("/users")


@app.route('/users/<int:user_id>/delete', methods=["POST"])
def users_destroy(user_id):
    """Handle form submission for deleting existing user"""

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash(f"User {user.full_name} deleted.")

    return redirect("/users")


#################################### POST ROUTES ##########################################


@app.route('/users/<int:user_id>/posts/new')
def posts_new_form(user_id):
    """Form to create a new post for a specific user"""

    user = User.query.get_or_404(user_id)
    tags = Tag.query.all()
    return render_template('posts/new.html', user=user, tags=tags)


@app.route('/users/<int:user_id>/posts/new', methods=["POST"])
def posts_new(user_id):
    """Handle form submission for creating new post for specific user"""

    user = User.query.get_or_404(user_id)
    tag_ids = [int(num) for num in request.form.getlist("tags")]
    tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    new_post = Post(title=request.form['title'],
                    content=request.form['content'],
                    user=user,
                    tags=tags)

    db.session.add(new_post)
    db.session.commit()
    flash(f"Post '{new_post.title}' added.")

    return redirect(f"/users/{user_id}")


@app.route('/posts/<int:post_id>')
def posts_show(post_id):
    """Page with info on a specific post"""

    post = Post.query.get_or_404(post_id)
    tags = Tag.query.all()
    return render_template('posts/show.html', post=post, tags=tags)


@app.route('/posts/<int:post_id>/edit')
def posts_edit(post_id):
    """Form to edit an existing post"""

    post = Post.query.get_or_404(post_id)
    tags = Tag.query.all()
    return render_template('posts/edit.html', post=post, tags=tags)


@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def posts_update(post_id):
    """Handle form submission for updating existing post"""

    post = Post.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form['content']

    tag_ids = [int(num) for num in request.form.getlist("tags")]
    post.tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    db.session.add(post)
    db.session.commit()
    flash(f"Post '{post.title}' edited.")

    return redirect(f"/users/{post.user_id}")


@app.route('/posts/<int:post_id>/delete', methods=["POST"])
def posts_destroy(post_id):
    """Handle form submission for deleting existing post"""

    post = Post.query.get_or_404(post_id)

    db.session.delete(post)
    db.session.commit()
    flash(f"Post '{post.title} deleted.")

    return redirect(f"/users/{post.user_id}")


#################################### TAGS ROUTES ##########################################


@app.route('/tags')
def tags_index():
    """Page with info on all tags"""

    tags = Tag.query.all()
    return render_template('tags/index.html', tags=tags)


@app.route('/tags/new')
def tags_new_form():
    """Form to create a new tag"""

    posts = Post.query.all()
    return render_template('tags/new.html', posts=posts)


@app.route("/tags/new", methods=["POST"])
def tags_new():
    """Handle form submission for creating new tag"""

    post_ids = [int(num) for num in request.form.getlist("posts")]
    posts = Post.query.filter(Post.id.in_(post_ids)).all()
    new_tag = Tag(name=request.form['name'], posts=posts)

    db.session.add(new_tag)
    db.session.commit()
    flash(f"Tag '{new_tag.name}' added.")

    return redirect("/tags")


@app.route('/tags/<int:tag_id>')
def tags_show(tag_id):
    """Page with info on a specific tag"""

    tag = Tag.query.get_or_404(tag_id)
    return render_template('tags/show.html', tag=tag)


@app.route('/tags/<int:tag_id>/edit')
def tags_edit_form(tag_id):
    """Form to edit an existing tag"""

    tag = Tag.query.get_or_404(tag_id)
    posts = Post.query.all()
    return render_template('tags/edit.html', tag=tag, posts=posts)


@app.route('/tags/<int:tag_id>/edit', methods=["POST"])
def tags_edit(tag_id):
    """Handle form submission for updating existing tag"""

    tag = Tag.query.get_or_404(tag_id)
    tag.name = request.form['name']
    post_ids = [int(num) for num in request.form.getlist("posts")]
    tag.posts = Post.query.filter(Post.id.in_(post_ids)).all()

    db.session.add(tag)
    db.session.commit()
    flash(f"Tag '{tag.name}' edited.")

    return redirect("/tags")


@app.route('/tags/<int:tag_id>/delete', methods=["POST"])
def tags_destroy(tag_id):
    """Handle form submission for deleting existing tag"""

    tag = Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()
    flash(f"Tag '{tag.name}' deleted.")

    return redirect("/tags")
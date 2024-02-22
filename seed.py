from models import db, User, Post
from app import app

db.drop_all()
db.create_all()

User.query.delete()

philip = User(first_name='Philip', last_name='Harmon')
wyatt = User(first_name='Wyatt', last_name='Harmon')
pepper = User(first_name='Pepper', last_name='Harmon')
jessica = User(first_name='Jessica', last_name='Culpepper')
briar = User(first_name='Briar', last_name='Harmon')

Post.query.delete()

post1 = Post(title='Test', content='This is a test', user_id=1)
post2 = Post(title='Test 2', content='This is a test', user_id=2)

db.session.add_all([philip, wyatt, pepper, jessica, briar])
db.session.commit()

db.session.add_all([post1, post2])
db.session.commit()
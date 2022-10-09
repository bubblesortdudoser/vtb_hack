import os
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
import sqlite3

app = Flask(__name__)
app.app_context().push()
basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')

db = SQLAlchemy(app)

class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(5096))
    href = db.Column(db.String(5096))
    text = db.Column(db.String(10192))
    date_time = db.Column(db.String(64))
    source_site = db.Column(db.String(64))
    views = db.Column(db.Integer())
    is_send = db.Column(db.Boolean(), default = False)

def init_post(title:str, href:str, text:str, date_time:str,source_site:str,views:int, is_send:bool):
    try:
        if Post.query.filter_by(href=href).first():
            return {"message": 'Post already added'}
        else:
            post = Post(title = title, href = href, text = text, date_time = date_time, source_site = source_site,views=views,is_send=False)
            db.session.add(post)
            db.session.commit()

        return {"message": f'Added post {post.id}', "href": post.href}

    except Exception as e:
        return jsonify(message=e, status="DB error")

def unsend_posts():
    return Post.query.filter(Post.is_send == False).all()

def get_post(href:str):
    try:
        with app.app_context():

            if Post.query.filter_by(href=href).first():
                post = Post.query.filter_by(href=href).first()
                return post
            else:
                False

    except Exception as e:
        return jsonify(message=e, status="DB error")

def get_all_posts():
    return Post.query.filter(Post.id != None).all()

def change_status(href:str, status:bool):
    try:
        if Post.query.filter_by(href=href).first():
            post = Post.query.filter_by(href=href).first()
            post.is_send = status
            db.session.commit()
            return {"message": f'Post status update {post.id}', "href": post.href}
        else:
            pass

        return {"message": f'Added post {post.id}', "href": post.href}

    except Exception as e:
        return jsonify(message=e, status="DB error")

def rewrite_title_post(title:str, href:str):
    try:
        if Post.query.filter_by(href=href).first():
            post = Post.query.filter_by(href=href).first()
            post.title = title
            db.session.commit()
            return True
        else:
            return False

    except Exception as e:
        return jsonify(message=e, status="DB error")

def to_csv():
    try:
        conn = sqlite3.connect('db.sqlite', isolation_level=None, detect_types=sqlite3.PARSE_COLNAMES)
        db_df = pd.read_sql_query("SELECT * FROM posts", conn)
        db_df.to_csv('../csv/data.csv', index=False)

    except Exception as e:
        return jsonify(message=e, status="DB error")


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer(), primary_key=True)
    chat_id = db.Column(db.Integer())
    role = db.Column(db.String(64))
    scope_of_activity = db.Column(db.String(64))

def init_user(chat_id:int, role:str, scope_of_activity:str):
    try:
        if User.query.filter_by(chat_id=chat_id).first():
            return {"message": 'User already added'}
        else:
            user = User(chat_id=chat_id,role=role,scope_of_activity=scope_of_activity)
            db.session.add(user)
            db.session.commit()

        return {"message": f'Added user {user.id}'}

    except Exception as e:
        return jsonify(message=e, status="DB error")





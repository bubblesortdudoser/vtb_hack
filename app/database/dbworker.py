import os
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import date
import uuid

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

def init_post(title:str, href:str, text:str, date_time:str):
    # try:
        if Post.query.filter_by(href=href).first():
            return {"message": 'Post already added'}
        else:
            post = Post(title = title, href = href, text = text, date_time = date_time)
            db.session.add(post)
            db.session.commit()

        return {"message": f'Added post {post.id}', "href": post.href}

    # except Exception as e:
    #     return jsonify(message=e, status="DB error")

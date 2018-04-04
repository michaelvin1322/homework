# -*- coding: utf-8 -*-

from flask import Flask, request, render_template, flash
from flask_sqlalchemy import SQLAlchemy
from json import dumps

import config as config


app = Flask(__name__, template_folder='templates')
app.config.from_object(config)

# http://flask-sqlalchemy.pocoo.org/2.1/quickstart/#a-minimal-application
db = SQLAlchemy(app)


@app.route('/items', methods=['GET', 'POST', ])
def index():
    from models import GuestBookItem
    from forms import GuestBookForm

    if request.method == 'POST':
        print(request.form)
        form = GuestBookForm(request.form)

        if form.validate():
            post = GuestBookItem(**form.data)
            db.session.add(post)
            db.session.commit()

            return 'Post created!'
        else:
            print(str(form.errors))
            return 'Form is not valid! Post was not created. \n' + str(form.errors)
    else:
        posts = GuestBookItem.query.all()
        # user = User.query.filter(id=posts[0].user_id)
        # user = posts[0].user
        # print(posts)
        # return dumps([post.to_dict() for post in posts])
        return render_template('home.jinja2',
                               posts=posts,
                               )


@app.route('/items/<int:post_id>', methods=['GET', 'POST', ])
def post(post_id):
    from models import CommentItem, GuestBookItem
    from forms import CommentForm

    post = GuestBookItem.query.get_or_404(post_id)

    if request.method == 'POST':
        form = CommentForm(request.form)
        if form.validate():
            comment = CommentItem(**form.data, post_id=post_id)
            db.session.add(comment)
            db.session.commit()
            return 'comment created'
        else:
            return 'fail'
    else:
        comments = CommentItem.query.filter(CommentItem.post_id == post_id).all()
        return render_template('post.jinja2',
                               post=post,
                               comments=comments
                               )


def populate_db():
    print('Creating default user')
    # Creating new ones:
    post = GuestBookItem(user_name='Ivan', title='great title', content='some post.... ')
    comment1 = CommentItem(user_name='Petr', content='some comment ', post_id=1)
    comment2 = CommentItem(user_name='Vasa', content='lorem ipsum dolor ', post_id=1)

    db.session.add(post)
    db.session.add(comment1)
    db.session.add(comment2)

    db.session.commit()

    # note


if __name__ == '__main__':
    from models import *
    db.create_all()

    if GuestBookItem.query.count() == 0:
        populate_db()

    users = GuestBookItem.query.all()
#    print(list(map(str, GuestBookItem)))

    # Running app:
    app.run()

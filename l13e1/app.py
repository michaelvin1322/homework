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
        print(posts)
        return dumps([post.to_dict() for post in posts])


def populate_db():
    print('Creating default user')
    # Creating new ones:
    ivan = GuestBookItem(user_name='Ivan', content='some comment or post.... ')

    db.session.add(ivan)
    db.session.commit()  # note


if __name__ == '__main__':
    from models import *
    db.create_all()

    if GuestBookItem.query.count() == 0:
        populate_db()

    users = GuestBookItem.query.all()
#    print(list(map(str, GuestBookItem)))

    # Running app:
    app.run()

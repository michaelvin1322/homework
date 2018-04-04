# -*- coding: utf-8 -*-

from datetime import date

from app import db


class GuestBookItem(db.Model):
    __tablename__ = 'GuestBookItem'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_name = db.Column(db.String(80), nullable=False)
    title = db.Column(db.String(80), nullable=False)
    content = db.Column(db.String(3000), nullable=False)
    date_created = db.Column(db.Date, default=date.today)
    is_visible = db.Column(db.Boolean, default=True, nullable=False)

    def __str__(self):
        return '<user_name %r, said content %s>'.format(self.user_name, self.content)

    def to_dict(self):
        return {'id': self.id,
                'user_name': self.user_name,
                'content': self.content,
                'date_created': self.date_created.isoformat(),
                }


class CommentItem(db.Model):
    __tablename__ = 'CommentItem'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    post_id = db.Column(
        db.Integer,
        db.ForeignKey('GuestBookItem.id'),
        nullable=False,
                        )
    post = db.relationship(GuestBookItem,
                           foreign_keys=[post_id, ],
                           )
    user_name = db.Column(db.String(80), nullable=False)
    content = db.Column(db.String(3000), nullable=False)
    date_created = db.Column(db.Date, default=date.today)
    is_visible = db.Column(db.Boolean, default=True, nullable=False)

    def __str__(self):
        return '<user_name %r, said content %s>'.format(self.user_name, self.content)

    def to_dict(self):
        return {'id': self.id,
                'post_id': self.post_id,
                'user_name': self.user_name,
                'content': self.content,
                'date_created': self.date_created.isoformat(),
                }
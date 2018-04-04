# -*- coding: utf-8 -*-

from datetime import date

from app import db


class GuestBookItem(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_name = db.Column(db.String(80), nullable=False)
    content = db.Column(db.String(3000), nullable=False)
    date_created = db.Column(db.Date, default=date.today)
    updated_at = db.Column(db.Date, nullable=False, default=date.today)
    is_visible = db.Column(db.Boolean, default=True, nullable=False)

    def __str__(self):
        return '<user_name %r, said content %s>'.format(self.user_name, self.content)

    def to_dict(self):
        res = {'id': self.id,
               'user_name': self.user_name,
               'content': self.content,
               'date_created': self.date_created.isoformat(),
               'updated_at': self.updated_at.isoformat(),
               }
        return res

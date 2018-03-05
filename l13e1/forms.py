# -*- coding: utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import fields, validators
from wtforms_alchemy import ModelForm

# from sqlalchemy_example.models import GuestBookItem


class GuestBookForm(FlaskForm):  # This looks ugly!
    user_name = fields.StringField(validators=[
        validators.DataRequired(),
    ])
    content = fields.StringField(validators=[
        validators.DataRequired(),
        validators.Length(min=5, message='At least 5 symbols'),
    ])


# https://wtforms-alchemy.readthedocs.org/en/latest/introduction.html
# class GuestBookForm(ModelForm):
#     class Meta:
#         model = GuestBookItem


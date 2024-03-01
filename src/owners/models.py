from tortoise import fields

from src.base.models import ModelBase


class Owner(ModelBase):
    username = fields.CharField(max_length=255)
    email = fields.CharField(max_length=255, unique=True)
    password = fields.CharField(max_length=255)
    contact_number = fields.CharField(max_length=255)
    picture_url = fields.CharField(max_length=255)

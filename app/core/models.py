from mongoengine import (
    Document
)
from mongoengine.fields import (
    IntField,
    StringField
)


class Company(Document):
    """Model to hold the company information"""
    meta = {'collection': 'companies'}
    index = IntField(required=True)
    company = StringField(required=True)

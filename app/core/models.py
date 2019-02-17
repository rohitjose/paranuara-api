from mongoengine import (
    Document,
    EmbeddedDocument
)
from mongoengine.fields import (
    IntField,
    StringField,
    BooleanField,
    ListField,
    EmailField,
    URLField,
    EmbeddedDocumentListField
)


class Company(Document):
    """Model to hold the company information"""
    meta = {'collection': 'companies'}
    index = IntField(required=True)
    company = StringField(required=True)


class Friend(EmbeddedDocument):
    """Model to hold the index value field for friends"""
    index = IntField(required=True)


class Person(Document):
    """Model to hold the information of the people in Paranuara"""
    meta = {'collection': 'people'}
    index = IntField(required=True)
    guid = StringField()
    has_died = BooleanField(required=True)
    balance = StringField()
    picture = URLField()
    age = IntField()
    eyeColor = StringField(required=True)
    name = StringField(required=True)
    gender = StringField(choices=['male', 'female'])
    company_id = IntField(required=True)
    email = EmailField()
    phone = StringField()
    address = StringField()
    about = StringField()
    registered = StringField()
    tags = ListField(StringField())
    friends = EmbeddedDocumentListField(Friend)
    greeting = StringField()
    favouriteFood = ListField(StringField())


class Food(Document):
    """Model holds the categorized food types"""
    meta = {'collection': 'food'}
    name = StringField(required=True)
    group = StringField(required=True, choices=['fruit', 'vegetable'])

import json
from mongoengine import (
    connection,
    connect)
from django.test import TestCase
from app.settings import MONGO_TEST

from core.models import Company, Person


class MongoTestCase(TestCase):
    def setUp(self):
        connection.disconnect()
        connect(
            host=MONGO_TEST['host'],
            db=MONGO_TEST['db'],
            username=MONGO_TEST['username'],
            password=MONGO_TEST['password'],
            authentication_source='admin'
           )
        super().setUpClass()

    def tearDown(self):
        from mongoengine.connection import get_connection, disconnect
        connection = get_connection()
        connection.drop_database(MONGO_TEST['db'])
        disconnect()
        super().tearDownClass()


class ModelTests(MongoTestCase):

    def test_company_str(self):
        """Tests the company string representation"""
        company = Company(
            index=10,
            company='ACME Inc'
        )
        company.save()
        assert Company.objects.first().company == company.company

    def test_people_str(self):
        """Tests the validity of the people model"""
        with open("core/tests/test_data/person.json") as person_json:
            person = json.load(person_json)
            person_obj = Person(**person)
            person_obj.save()
            assert Person.objects.first().name == person['name']

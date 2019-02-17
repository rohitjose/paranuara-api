import json
from mongoengine import connect
from django.test import TestCase

from core.models import Company, Person
from app.settings import MONGO_TEST


class MongoTestCase(TestCase):
    def setUp(self):
        self.db = connect(
            host=MONGO_TEST['host'],
            db=MONGO_TEST['db'],
            username=MONGO_TEST['username'],
            password=MONGO_TEST['password'],
            authentication_source='admin'
        )
        super().setUpClass()

    def tearDown(self):
        self.db.drop_database(MONGO_TEST['db'])
        self.db.close()
        super().tearDownClass()


class ModelTests(MongoTestCase):

    def test_company_str(self):
        """Tests the company string representation"""
        company = Company(
            index=11,
            company='ACME Inc'
        )
        company.save()
        assert Company.objects.get(index=11).company == company.company

    def test_people_str(self):
        """Tests the validity of the people model"""
        with open("core/tests/test_data/person.json") as person_json:
            person = json.load(person_json)
            person_obj = Person(**person)
            person_obj.save()
            assert Person.objects.get(
                index=person['index']).name == person['name']

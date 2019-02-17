import json
from graphene.test import Client

from app.schema import schema
from core.models import Person
from core.tests.test_models import MongoTestCase


class CompanyApiTests(MongoTestCase):
    """Tests the APIs for the People entity"""

    def setUp(self):
        super().setUp()
        self.client = Client(schema)
        # Populate the test collectiom with person data
        with open("core/tests/test_data/people.json") as employee_json:
            employees = json.load(employee_json)
            for employee in employees:
                employee_obj = Person(**employee)
                employee_obj.save()

    def test_common_friends_invalid_input(self):
        """Tests if the API returns an error when the
           number of ids sent is less than 2 for the lookup"""
        response = self.client.execute('''
                        {
                            commonFriends(id: [1]) {
                                index,
                                name,
                                age
                            }
                        }''')
        self.assertEqual(response["errors"][0]["message"],
                         "Lookup needs atleast two index values")

    def test_common_friends_no_common_friends(self):
        """Tests if the API returns an error if it is
           unable to find any common friends"""
        response = self.client.execute('''
                        {
                            commonFriends(id: [0,1,2]) {
                                index,
                                name,
                                age
                            }
                        }''')
        self.assertEqual(response["errors"][0]["message"],
                         "No common friends found")

    def test_common_friends_for_two_ids(self):
        """Tests if the API returns the right common friends
           when it is sent 2 lookup ids"""
        valid_common_friends = [0]
        response = self.client.execute('''
                        {
                            commonFriends(id: [1,2]) {
                                index
                            }
                        }''')
        response_common_friends = [friend['index']
                                   for friend in
                                   response['data']['commonFriends']]
        self.assertTrue(valid_common_friends == response_common_friends)

    def test_common_friends_for_more_than_two_ids(self):
        """Tests if the API returns the right common friends
           when it is sent more than 2 lookup ids"""
        valid_common_friends = [0, 2]
        response = self.client.execute('''
                        {
                            commonFriends(id: [1,3,4,5]) {
                                index
                            }
                        }''')
        response_common_friends = [friend['index']
                                   for friend in
                                   response['data']['commonFriends']]
        self.assertTrue(valid_common_friends == response_common_friends)

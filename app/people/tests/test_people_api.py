import json
from graphene.test import Client

from app.schema import schema
from core.models import Person, Food
from core.tests.test_models import MongoTestCase


class CompanyApiTests(MongoTestCase):
    """Tests the APIs for the People entity"""

    def setUp(self):
        super().setUp()
        self.client = Client(schema)

        # Populate the test collectiom with person data
        with open("core/tests/test_data/people.json") as people_json:
            peoples = json.load(people_json)
            for people in peoples:
                people_obj = Person(**people)
                people_obj.save()

        # Populate the food collection from test data file
        with open("core/tests/test_data/food.json") as food_json:
            food_list = json.load(food_json)
            for food in food_list:
                food_obj = Food(**food)
                food_obj.save()

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

    def test_favourite_food_invalid_id(self):
        """Tests if API returns an error for an invalid
           person index value"""
        response = self.client.execute('''
                        {
                            favouriteFood(id: 10001){
                                username,
                                age,
                                fruits,
                                vegetables
                            }
                        }''')
        self.assertEqual(response["errors"][0]["message"],
                         "Person index not found")

    def test_favourite_food_valid(self):
        """Tests if the API returns a valid response
            for a valid person index"""
        valid_veggies = ["celery", "carrot"]
        valid_fruits = ["apple", "orange"]
        name = "Rosemary Hayes"
        age = 30
        response = self.client.execute('''
                        {
                            favouriteFood(id: 3){
                                username,
                                age,
                                fruits,
                                vegetables
                            }
                        }''')
        favouriteFood = response['data']['favouriteFood']

        self.assertTrue(
            favouriteFood['vegetables'] == valid_veggies and
            favouriteFood['fruits'] == valid_fruits and
            favouriteFood['username'] == name and
            favouriteFood['age'] == age
        )

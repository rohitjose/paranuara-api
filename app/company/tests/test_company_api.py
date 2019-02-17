import json
from graphene.test import Client

from app.schema import schema
from core.models import Person, Company
from core.tests.test_models import MongoTestCase


class CompanyApiTests(MongoTestCase):
    """Tests the APIs for the Company entity"""

    def setUp(self):
        super().setUp()
        self.client = Client(schema)
        # Populate the test collectiom with person data
        with open("core/tests/test_data/employees.json") as employee_json:
            employees = json.load(employee_json)
            for employee in employees:
                employee_obj = Person(**employee)
                employee_obj.save()
        # Populate the test collection with company data
        with open("core/tests/test_data/companies.json") as companies_json:
            companies = json.load(companies_json)
            for companies in companies:
                companies_obj = Company(**companies)
                companies_obj.save()

    def test_employee_retrieval_no_employees(self):
        """Tests if the API returns an error when there are no employees"""
        response = self.client.execute('''
                        {
                            employees(lookup:"id", value: "0"){
                                index
                            }
                        }''')
        self.assertEqual(response["errors"][0]["message"],
                         "No employees found")

    def test_employee_retrieval_invalid_id(self):
        """Tests if the API returns an error when the company id is invalid"""
        response = self.client.execute('''
                        {
                            employees(lookup:"id", value: "29012"){
                                index
                            }
                        }''')
        self.assertEqual(response["errors"][0]["message"],
                         "Company index not found")

    def test_employee_retrieval_invalid_name(self):
        """Tests if the API returns an error when the company
           name is invalid"""
        response = self.client.execute('''
                        {
                            employees(lookup:"name", value: "george"){
                                index
                            }
                        }''')
        self.assertEqual(response["errors"][0]["message"],
                         "Company name not found")

    def test_employee_retrieval_id(self):
        """Tests the retrieval of the employee data based on id"""
        with open("core/tests/test_data/employees.json") as employees_json:
            employees = json.load(employees_json)
            test_employee_indices = set([employee['index']
                                         for employee in employees])
            executed = self.client.execute('''
                        {
                            employees(lookup:"id", value: "10"){
                                index
                            }
                        }''')
            executed_employee_indices = set([employee['index']
                                             for employee in
                                             executed['data']['employees']])

        self.assertTrue(test_employee_indices == executed_employee_indices)

    def test_employee_retrieval_name(self):
        """Tests the retrieval of the employee data based on name"""
        with open("core/tests/test_data/employees.json") as employees_json:
            employees = json.load(employees_json)
            test_employee_indices = set([employee['index']
                                         for employee in employees])
            executed = self.client.execute('''
                        {
                            employees(lookup:"name", value: "ZOLARITY"){
                                index
                            }
                        }''')
            executed_employee_indices = set([employee['index']
                                             for employee in
                                             executed['data']['employees']])

        self.assertTrue(test_employee_indices == executed_employee_indices)

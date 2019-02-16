import graphene
from graphene_mongo import MongoengineObjectType

from core.models import Company, Person, Friend


class CompanyType(MongoengineObjectType):
    class Meta:
        model = Company


class PersonType(MongoengineObjectType):
    class Meta:
        model = Person


class FriendType(MongoengineObjectType):
    class Meta:
        model = Friend


class Query(graphene.ObjectType):
    companies = graphene.List(CompanyType)
    employees = graphene.List(PersonType,
                              lookup=graphene.String(),
                              value=graphene.String())

    def resolve_companies(self, info, **kwargs):
        return Company.objects.all()

    def resolve_employees(self, info, lookup='id', value=None, **kwargs):

        # Input validation
        if lookup not in ['id', 'name']:
            raise Exception('Invalid Value - \
                             lookup field - accepts[id, name]')
        if not value:
            raise Exception('Invalid Value - value field')

        # Route based on the lookup type
        # Company ID lookup
        if lookup == 'id':
            employees = Person.objects(company_id=value)
            # If no employees are returned check if the company id is valid
            if len(employees) < 1:
                try:
                    company = Company.objects.get(index=value)
                except Company.DoesNotExist:
                    raise Exception('Company index not found')
                raise Exception('No employees found')
            else:
                return employees

        # Company name lookup
        if lookup == 'name':
            # Find the index of the company first
            try:
                company = Company.objects.get(company=value)
            except Company.DoesNotExist:
                raise Exception('Company name not found')
            # Company found
            employees = Person.objects(company_id=company.index)
            if len(employees) < 1:
                raise Exception('No employees found')
            else:
                return employees

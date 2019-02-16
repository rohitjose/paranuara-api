import graphene
from graphene_mongo import MongoengineObjectType

from core.models import Company


class CompanyType(MongoengineObjectType):
    class Meta:
        model = Company


class Query(graphene.ObjectType):
    companies = graphene.List(CompanyType)

    def resolve_companies(self, info, **kwargs):
        return Company.objects.all()

import graphene

import company.schema
import people.schema


class Query(company.schema.Query, people.schema.Query, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query)

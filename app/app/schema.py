import graphene

import company.schema


class Query(company.schema.Query, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query)

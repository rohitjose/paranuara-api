import graphene

from core.models import Person
from company.schema import PersonType


class Query(graphene.ObjectType):
    people = graphene.List(PersonType)
    common_friends = graphene.List(PersonType,
                                   args={'id':
                                         graphene.List(graphene.Int)})

    def resolve_people(self, info, **kwargs):
        """API resolves to retrieve all Person info"""
        return Person.objects.all()

    def resolve_common_friends(self, info, id, **kwargs):
        """API resolver to find commond friends from multiple people"""
        # Check if input has two indices for lookup
        if len(id) < 2:
            raise Exception('Lookup needs atleast two index values')

        common_friends = set()
        for person in Person.objects.filter(index__in=id):
            current_friends = set([friend.index for
                                   friend in person['friends']])
            if len(common_friends) == 0:
                common_friends = current_friends
            else:
                common_friends.intersection(current_friends)

        # Removes the lookup ids from list of common friends
        for id_value in id:
            if id_value in common_friends:
                common_friends.remove(id_value)

        if len(common_friends) > 0:
            return Person.objects.filter(index__in=list(common_friends))
        else:
            raise Exception('No common friends found')

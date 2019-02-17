import graphene

from core.models import Person, Food
from company.schema import PersonType


class FavouriteFoodType(graphene.ObjectType):
    """Graphene object type to return the
       favourite food of a person"""
    username = graphene.String()
    age = graphene.Int()
    fruits = graphene.List(graphene.String)
    vegetables = graphene.List(graphene.String)


class Query(graphene.ObjectType):
    people = graphene.List(PersonType)
    common_friends = graphene.List(PersonType,
                                   args={'id':
                                         graphene.List(graphene.Int)})
    favourite_food = graphene.Field(FavouriteFoodType, id=graphene.Int())

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
            friends = Person.objects.filter(index__in=list(common_friends),
                                            eyeColor='brown',
                                            has_died=False)
            if friends.count() > 0:
                return friends
        raise Exception('No common friends found')

    def resolve_favourite_food(self, info, id, **kwargs):
        """API resolver to find the favourite food of a person"""
        # Lookup person using id
        try:
            person = Person.objects.get(index=id)
        except Person.DoesNotExist:
            raise Exception('Person index not found')

        # Retrieve the favourite food of the person
        favourite_food_list = \
            Food.objects.filter(name__in=person['favouriteFood'])

        return FavouriteFoodType(
            username=person['name'],
            age=person['age'],
            fruits=[food.name for food in
                    favourite_food_list
                    if food.group == 'fruit'],
            vegetables=[food.name for food in
                        favourite_food_list
                        if food.group == 'vegetable']
        )

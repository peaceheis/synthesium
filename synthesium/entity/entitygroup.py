from typing import Type, Union

from synthesium.entity.primitives import *


class EntityGroup(VectorEntity):
    """Enables multiple Entities (such as the primitives Line, Arc, and Curve), to make what functions as one
    VectorEntity. """

    def __init__(self, *entities: Union[tuple, list], **kwargs: dict) -> None:
        self.entities = entities
        self.points = []
        for entity in entities:
            self.points.extend(entity.get_points())
        configure(kwargs)

    def add_entity(self, entity: VectorEntity) -> "EntityGroup":
        self.entities += entity
        self.points += entity.get_points()
        return self

    def get_entities_by_type(self, entity_type: Type) -> list:
        """[Used for recursively getting the entities that make up  an EntityGroup by type. Used internally to get all the Lines,
            Curves, and Arcs that make up  an EntityGroup.]

        Args:
            type Type(VectorEntity): [the type of the VectorEntity to be found.]

        Returns:
            [list]: a list of all the entities of the type found, if none found, returns an empty list.
        """
        entities = []
        # probably could be more compact as a list comprehension, but it's more readable this way.
        for entity in self.entities:
            if isinstance(entity, EntityGroup):
                entities += entity.get_entities_by_type(entity_type)

            elif isinstance(entity, entity_type):
                entities.append(entity)
        return entities

    def shift(self, amt):
        self.entities = [entity.shift(amt) for entity in self.entities]
        self.points = [entity.get_points() for entity in self.entities]

    def rotate(self, degrees, center, rotates_clockwise=True):
        self.entities = [entity.rotate(degrees, center, rotates_clockwise) for entity in self.entities]
        self.points = [entity.get_points() for entity in self.entities]

    # utils
    def get_points(self) -> "tuple":
        return tuple([entity.get_points() for entity in self.entities])

    def set_points(self, *points):
        """Setting individual points with an EntityGroup is not possible. Try setting the points of the individual
        entities. """
        # despite automatically raising an error on trying to run this, it's best to say WHY
        # the error is being raised,
        # so we set the normal arguments.
        raise Exception(
            "Using set_points() is not allowed with EntityGroups; add an VectorEntity such as Line, Arc, or Curve, "
            "or else another EntityGroup.")
        # allowing entityGroups to have their own points would be incompatible with the current rendering pipeline,
        # which reduces everything to primitives.

    def entities(self):
        return self.entities

    def set_entities(self):
        self.entities = [entities.points() for entities in self.entities]
        self.points = [entity.points for entity in self.entities]

    def __str__(self):
        string = f"VectorEntity Group of type {self.__class__.__name__}, consisting of "
        for entity in self.entities:
            string += f"\n\t {entity.__str__()}"
        return string

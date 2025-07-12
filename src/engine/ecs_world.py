"""
ecs_world.py
------------
Implements the core ECSWorld class for managing entities and components
in an Entity-Component-System (ECS) architecture.

Classes:
    ECSWorld: Handles creation, removal, and querying of entities and their components.
"""

from typing import Dict, Set, Type, Any, Iterable

class ECSWorld:
    """
    A robust implementation of the world in an ECS architecture.
    Efficiently manages entities, components, and queries.

    Attributes:
        _next_entity_id (int): Counter for assigning unique entity IDs.
        _entities (Dict[int, Dict[Type, Any]]): Maps entity IDs to their components.
        _components (Dict[Type, Set[int]]): Maps component types to sets of entity IDs.

    Methods:
        create_entity() -> int:
            Creates a new entity and returns its unique ID.

        remove_entity(entity_id: int):
            Removes an entity and all its components.

        add_component(entity_id: int, component_instance: Any):
            Adds a component instance to an entity.

        remove_component(entity_id: int, component_class: Type):
            Removes a specific component from an entity.

        get_component(entity_id: int, component_class: Type) -> Any:
            Retrieves a component instance from an entity.

        get_entities_with_components(*component_classes: Type) -> Iterable[int]:
            Returns all entity IDs that have all specified component types.
    """
    def __init__(self):
        self._next_entity_id: int = 0
        self._entities: Dict[int, Dict[Type, Any]] = {}
        self._components: Dict[Type, Set[int]] = {}

    def create_entity(self) -> int:
        """
        Creates a new entity and returns its unique ID.
        """
        entity_id = self._next_entity_id
        self._entities[entity_id] = {}
        self._next_entity_id += 1
        return entity_id

    def remove_entity(self, entity_id: int):
        """
        Removes an entity and all its components from the world.

        Args:
            entity_id (int): The ID of the entity to remove.
        """
        if entity_id in self._entities:
            for component_class in self._entities[entity_id]:
                if component_class in self._components:
                    self._components[component_class].discard(entity_id)
            del self._entities[entity_id]

    def add_component(self, entity_id: int, component_instance: Any):
        """
        Adds a component instance to an entity.

        Args:
            entity_id (int): The ID of the entity.
            component_instance (Any): The component instance to add.
        """
        component_class = type(component_instance)
        if entity_id not in self._entities:
            return
        self._entities[entity_id][component_class] = component_instance
        self._components.setdefault(component_class, set()).add(entity_id)
    
    def remove_component(self, entity_id: int, component_class: Type):
        """
        Removes a specific component from an entity.

        Args:
            entity_id (int): The ID of the entity.
            component_class (Type): The class of the component to remove.
        """
        if entity_id in self._entities and component_class in self._entities[entity_id]:
            del self._entities[entity_id][component_class]
            if component_class in self._components:
                self._components[component_class].discard(entity_id)
                if not self._components[component_class]:
                    del self._components[component_class]

    def get_component(self, entity_id: int, component_class: Type) -> Any:
        """
        Retrieves a component instance from an entity.

        Args:
            entity_id (int): The ID of the entity.
            component_class (Type): The class of the component to retrieve.

        Returns:
            Any: The component instance, or None if not found.
        """
        return self._entities.get(entity_id, {}).get(component_class)

    def get_entities_with_components(self, *component_classes: Type) -> Iterable[int]:
        """
        Returns all entity IDs that have all specified component types.

        Args:
            *component_classes (Type): Component classes to filter entities.

        Returns:
            Iterable[int]: Entity IDs that have all specified components.
        """
        if not component_classes:
            return []
        try:
            # Es crucial usar .copy() para no modificar la caché original
            result = self._components[component_classes[0]].copy()
            for i in range(1, len(component_classes)):
                result.intersection_update(self._components[component_classes[i]])
            return result
        except KeyError:
            return []

# ARCHIVO: engine/ecs_world.py
from typing import Dict, Set, Type, Any, Iterable

class ECSWorld:
    """
    Una implementación robusta del mundo en una arquitectura ECS.
    Gestiona entidades, componentes y consultas de manera eficiente.
    """
    def __init__(self):
        self._next_entity_id: int = 0
        self._entities: Dict[int, Dict[Type, Any]] = {}
        self._components: Dict[Type, Set[int]] = {}

    def create_entity(self) -> int:
        entity_id = self._next_entity_id
        self._entities[entity_id] = {}
        self._next_entity_id += 1
        return entity_id

    def remove_entity(self, entity_id: int):
        if entity_id in self._entities:
            for component_class in self._entities[entity_id]:
                if component_class in self._components:
                    self._components[component_class].discard(entity_id)
            del self._entities[entity_id]

    def add_component(self, entity_id: int, component_instance: Any):
        component_class = type(component_instance)
        if entity_id not in self._entities:
            return
        self._entities[entity_id][component_class] = component_instance
        self._components.setdefault(component_class, set()).add(entity_id)

    def get_component(self, entity_id: int, component_class: Type) -> Any:
        return self._entities.get(entity_id, {}).get(component_class)

    def get_entities_with_components(self, *component_classes: Type) -> Iterable[int]:
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

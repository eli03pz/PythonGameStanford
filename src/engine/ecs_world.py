class ECSWorld:
    def __init__(self):
        self._next_entity_id = 0
        self.components = {} # {entity_id: {ComponentType: instance}}

    def create_entity(self):
        entity_id = self._next_entity_id
        self._next_entity_id += 1
        self.components[entity_id] = {}
        return entity_id

    def add_component(self, entity_id, component):
        self.components[entity_id][type(component)] = component

    def get_component(self, entity_id, component_type):
        return self.components[entity_id].get(component_type)

    def remove_component(self, entity_id, component_type):
        if entity_id in self.components and component_type in self.components[entity_id]:
            del self.components[entity_id][component_type]

    def get_entities_with_components(self, *component_types):
        for entity_id, entity_components in self.components.items():
            if all(ct in entity_components for ct in component_types):
                yield entity_id

    def remove_entity(self, entity_id):
        if entity_id in self.components:
            del self.components[entity_id]
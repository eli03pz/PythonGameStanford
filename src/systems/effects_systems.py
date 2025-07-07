
import pygame
from components.menu_components import PositionComponent
from components.effects_components import ParticleComponent

class ParticleSystem:
    """Gestiona la vida y el movimiento de las partículas."""
    def __init__(self, world):
        self.world = world

    def update(self, dt):
        current_time = pygame.time.get_ticks()
        entities_to_remove = []
        for entity in self.world.get_entities_with_components(ParticleComponent, PositionComponent):
            particle = self.world.get_component(entity, PositionComponent)
            particle_data = self.world.get_component(entity, ParticleComponent)
            
            # Comprobar si la partícula ha expirado
            if current_time > particle_data.born_time + particle_data.lifetime:
                entities_to_remove.append(entity)
            else:
                # Mover la partícula
                particle.x += particle_data.velocity[0] * dt
                particle.y += particle_data.velocity[1] * dt
        
        for entity in entities_to_remove:
            self.world.remove_entity(entity)
            
    def draw(self, screen):
        for entity in self.world.get_entities_with_components(ParticleComponent, PositionComponent):
            pos = self.world.get_component(entity, PositionComponent)
            data = self.world.get_component(entity, ParticleComponent)
            pygame.draw.circle(screen, data.color, (pos.x, pos.y), 3)

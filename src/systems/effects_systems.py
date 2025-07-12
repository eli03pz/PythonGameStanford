"""
effects_systems.py
------------------
Implements ECS systems for visual effects, such as particle management.

Classes:
    ParticleSystem: Manages the lifecycle, movement, and rendering of particles.
"""
import pygame
from components.menu_components import PositionComponent
from components.effects_components import ParticleComponent

class ParticleSystem:
    """
    Manages the lifecycle and movement of all particles in the ECS world.

    Attributes:
        world: Reference to the ECS world.

    Methods:
        update(dt):
            Moves particles and removes them if their lifetime has expired.

        draw(screen):
            Draws all active particles on the given Pygame surface.
    """
    def __init__(self, world):
        self.world = world

    def update(self, dt):
        """
        Moves particles and removes them if their lifetime has expired.

        Args:
            dt (float): Delta time since last frame.
        """
        current_time = pygame.time.get_ticks()
        entities_to_remove = []
        
        for entity in self.world.get_entities_with_components(ParticleComponent, PositionComponent):
            particle_data = self.world.get_component(entity, ParticleComponent)
            pos = self.world.get_component(entity, PositionComponent)
            
            if current_time > particle_data.born_time + particle_data.lifetime:
                entities_to_remove.append(entity)
            else:
                # Aplicar una física simple (gravedad)
                particle_data.velocity = (particle_data.velocity[0], particle_data.velocity[1] + 150 * dt)
                pos.x += particle_data.velocity[0] * dt
                pos.y += particle_data.velocity[1] * dt
        
        for entity in entities_to_remove:
            self.world.remove_entity(entity)
            
    def draw(self, screen):
        """
        Draws all active particles.

        Args:
            screen: The Pygame surface to draw on.
        """
        for entity in self.world.get_entities_with_components(ParticleComponent, PositionComponent):
            pos = self.world.get_component(entity, PositionComponent)
            data = self.world.get_component(entity, ParticleComponent)
            pygame.draw.circle(screen, data.color, (pos.x, pos.y), 3)


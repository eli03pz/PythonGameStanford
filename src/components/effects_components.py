"""
effects_components.py
---------------------
This module defines components related to visual effects, such as particles,
for the game's ECS architecture.

Classes:
    ParticleComponent: Represents a single particle with lifetime, velocity, and color.
"""

import pygame

class ParticleComponent:
    """
    A component representing a single particle in the effects system.

    Attributes:
        born_time (int): The time when the particle was created (in milliseconds).
        lifetime (int): The duration of the particle's life in milliseconds.
        velocity (tuple): The initial velocity of the particle (dx, dy).
        color (tuple): The RGB color of the particle.

    Args:
        lifetime_ms (int): Lifetime of the particle in milliseconds.
        initial_velocity (tuple): Initial velocity (dx, dy).
        color (tuple): RGB color of the particle.
    """
    def __init__(self, lifetime_ms, initial_velocity, color):
        self.born_time = pygame.time.get_ticks()
        self.lifetime = lifetime_ms
        self.velocity = initial_velocity
        self.color = color
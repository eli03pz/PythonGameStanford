import pygame

class ParticleComponent:
    """Un componente para una partícula individual."""
    def __init__(self, lifetime_ms, initial_velocity, color):
        self.born_time = pygame.time.get_ticks()
        self.lifetime = lifetime_ms
        self.velocity = initial_velocity
        self.color = color
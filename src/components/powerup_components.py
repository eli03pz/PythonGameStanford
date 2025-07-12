# RESPONSABILIDAD: Definir los componentes para los poderes y efectos especiales.

import pygame

class PowerupComponent:
    """Marca una entidad como un ítem de poder que se puede recoger."""
    def __init__(self, powerup_type: str):
        self.type = powerup_type  # Ej: 'BIG_PADDLE', 'GHOST_BALL'
        self.spawn_time = pygame.time.get_ticks()

class ActivePowerupComponent:
    """Marca una entidad (pala) que tiene un poder activo."""
    def __init__(self, powerup_type: str, duration_ms: int):
        self.type = powerup_type
        self.activation_time = pygame.time.get_ticks()
        self.duration = duration_ms
        self.is_applied = False # Para asegurar que el efecto se aplica solo una vez

class HitFlashComponent:
    """Componente temporal para el efecto de "flash" al golpear la pelota."""
    def __init__(self, duration_ms: int):
        self.activation_time = pygame.time.get_ticks()
        self.duration = duration_ms

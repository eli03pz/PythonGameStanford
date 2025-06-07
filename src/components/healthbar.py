import pygame

class HealthBar:
    def __init__(self, player, x, y, width, height, max_health):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.max_health = max_health
        self.current_health = max_health
        self.player = player

    def update(self, current_health):
        self.current_health = current_health

    def render(self, surface):
        # Fondo de la barra (rojo)
        pygame.draw.rect(surface, (255, 0, 0), (int(self.x), int(self.y), int(self.width), int(self.height)))
        # Barra de vida actual (verde)
        current_width = int(self.width * (self.player.health / self.max_health))
        pygame.draw.rect(surface, (0, 255, 0), (int(self.x), int(self.y), current_width, int(self.height)))
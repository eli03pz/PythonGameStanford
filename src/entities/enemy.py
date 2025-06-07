import pygame

class Enemy:
    def __init__(self, x, y, health):
        self.x = x
        self.y = y
        self.health = health
        self.speed = 2
        self.attack_power = 10
        self.radius = 20

    def update(self):
        # TODO: Implement enemy behavior
        pass
    
    def render(self, surface):
        pygame.draw.circle(surface, (255, 0, 0), (int(self.x), int(self.y)), self.radius)
    
    def move(self):
        # Logic for enemy movement
        self.x += self.speed

    def attack(self, player):
        # Logic for attacking the player
        player.health -= self.attack_power

    def is_alive(self):
        return self.health > 0

    def draw(self, screen):
        # Logic for drawing the enemy on the screen
        pass
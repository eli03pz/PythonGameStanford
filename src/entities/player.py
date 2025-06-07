import pygame

class Player:
    def __init__(self, x, y, color, abilities):
        self.x = x
        self.y = y
        self.color = color
        self.radius = 20
        self.health = 100
        self.abilities = abilities
        self.score = 0
        self.speed = 5

    def update(self):
        # TODO: Update player state (movement, cooldowns, etc.)
        pass
    
    def handle_input(self):
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        if keys[pygame.K_w]:
            dy -= 1
        if keys[pygame.K_s]:
            dy += 1
        if keys[pygame.K_a]:
            dx -= 1
        if keys[pygame.K_d]:
            dx += 1
        if dx != 0 or dy != 0:
            self.move(dx, dy)
    
    def move(self, dx, dy):
        self.x += dx * self.speed
        self.y += dy * self.speed

    def shoot(self):
        # TODO: Implement shooting logic
        pass

    def use_ability(self, ability_index):
        if 0 <= ability_index < len(self.abilities):
            ability = self.abilities[ability_index]
            # TODO: Implement ability logic
            pass

    def take_damage(self, amount):
        self.health -= amount
        if self.health < 0:
            self.health = 0

    def is_alive(self):
        return self.health > 0

    def update_score(self, points):
        self.score += points

    def render(self, surface):
        # Draw the player as a circle
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)
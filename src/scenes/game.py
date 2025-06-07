import pygame
from entities.enemy import Enemy
from entities.player import Player
from systems.environment import Environment
from components.healthbar import HealthBar
from systems.score import Score

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.width = 800
        self.height = 600
        self.clock = pygame.time.Clock()
        self.running = True
        
        self.players = [Player(100, 100, (0, 255, 0), ["dash", "shield"]),   # Jugador 1: verde
                        Player(200, 100, (0, 0, 255), ["invisible", "heal"]) # Jugador 2: azul
        ]
        self.enemies = [Enemy(400, 300, 100)]  # 100 es un ejemplo de salud inicial
        self.powerups = []
        self.environment = Environment(self.width, self.height)
        self.health_bars = [
            HealthBar(player, 10 + i*410, 20, 200, 20, player.health)
            for i, player in enumerate(self.players)
        ]
        self.score = Score()

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(60)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

        for player in self.players:
            player.handle_input()

    def update(self):
        for player in self.players:
            player.update()
        for enemy in self.enemies:
            enemy.update()
        self.environment.update()
        self.check_collisions()

    def check_collisions(self):
        # Implement collision detection logic here
        pass
    
    def render(self):
        self.screen.fill((0, 0, 0))  # Limpia la pantalla con negro

        self.environment.render(self.screen)
        for player in self.players:
            player.render(self.screen)
        for enemy in self.enemies:
            enemy.render(self.screen)
        for health_bar in self.health_bars:
            health_bar.render(self.screen)
        # self.score.render(self.screen)

        pygame.display.flip()

    def quit(self):
        pygame.quit()
"""
game_scene.py
-------------
Implements the main game scene, including setup, cleanup, event handling,
updating, and drawing. Uses ECS systems for game logic, rendering, powerups,
effects, and input.

Classes:
    GameScene: Handles the creation and management of game entities and systems for gameplay.
"""
import pygame
from scenes.base_scene import BaseScene
from systems.environment import BallBoundarySystem
from systems.score import ScoringSystem
from utils.game_state import GameState

# Importamos todos los componentes y sistemas que usaremos
from components.menu_components import PositionComponent, DimensionsComponent
from components.game_components import *
from components.powerup_components import *
from components.effects_components import *
from systems.game_systems import *
from systems.powerup_systems import *
from systems.effects_systems import *

# Componente simple para el botón de pausa
class PauseButtonComponent: 
    """Simple marker component for the pause button entity."""
    pass

class GameScene(BaseScene):
    """
    Main game scene for gameplay.

    Attributes:
        num_players (int): Number of players (1 or 2).
        mode (str): Game mode ('classic', 'shrink', etc.).
        game_entities (list): List of entity IDs created for this scene.

    Methods:
        setup():
            Initializes all ECS systems and creates game entities (paddles, ball, scores, pause button).

        cleanup():
            Removes all entities created by this scene and clears particles.

        handle_events(events):
            Processes player input, pause button clicks, and ESC key for pausing.

        update(dt):
            Updates all game systems, including movement, AI, collisions, powerups, and scoring.

        draw(screen):
            Renders all game entities, particles, and draws the pause button.
    """
    def __init__(self, game, num_players, mode='classic'):
        super().__init__(game)
        self.num_players = num_players
        self.mode = mode
        self.game_entities = []

    def setup(self):
        """
        Initializes all ECS systems and creates game entities for gameplay.
        """
        print(f"GameScene: Configurando para {self.num_players} jugador(es) en modo '{self.mode}'.")
        
        # --- 1. Crear los sistemas del juego ---
        self.player_input_system = PlayerInputSystem(self.game.world, self.game.config_manager)
        self.ai_system = AISystem(self.game.world, self.game.screen_height)
        self.movement_system = MovementSystem(self.game.world, self.game.screen_height)
        self.ball_boundary_system = BallBoundarySystem(self.game.world, self.game.screen_height)
        self.paddle_collision_system = PaddleCollisionSystem(self.game.world, self.mode)
        self.scoring_system = ScoringSystem(self.game.world, self.game.screen_width, self.game.screen_height)
        self.render_system = GameRenderSystem(self.game.world, self.game.screen)
        
        # CORRECCIÓN: Corregido el error de tipeo de 'particule_system' a 'particle_system'
        self.particle_system = ParticleSystem(self.game.world)
        
        # Sistemas de Poderes
        self.powerup_spawning_system = PowerupSpawningSystem(self.game.world, self.game.screen_width, self.game.screen_height)
        self.powerup_collision_system = PowerupCollisionSystem(self.game.world)
        self.powerup_effect_system = PowerupEffectSystem(self.game.world)

        # --- 2. Crear las entidades del juego ---
        # (El código de creación de entidades es el mismo y está correcto)
        # Botón de Pausa
        pause_button_id = self.game.world.create_entity()
        self.game_entities.append(pause_button_id)
        self.game.world.add_component(pause_button_id, PositionComponent(self.game.screen_width - 60, 10))
        self.game.world.add_component(pause_button_id, DimensionsComponent(50, 50))
        self.game.world.add_component(pause_button_id, PauseButtonComponent())
        # Palas
        paddle_dims = DimensionsComponent(15, 100)
        p1_id = self.game.world.create_entity()
        self.game.world.add_component(p1_id, PositionComponent(50, self.game.screen_height / 2 - paddle_dims.height / 2))
        self.game.world.add_component(p1_id, paddle_dims)
        self.game.world.add_component(p1_id, VelocityComponent(0, 0))
        self.game.world.add_component(p1_id, PaddleComponent(player_number=1))
        self.game_entities.append(p1_id)
        p2_id = self.game.world.create_entity()
        self.game.world.add_component(p2_id, PositionComponent(self.game.screen_width - 50 - paddle_dims.width, self.game.screen_height / 2 - paddle_dims.height / 2))
        self.game.world.add_component(p2_id, DimensionsComponent(15, 100))
        self.game.world.add_component(p2_id, VelocityComponent(0, 0))
        if self.num_players == 2: self.game.world.add_component(p2_id, PaddleComponent(player_number=2))
        else: self.game.world.add_component(p2_id, AIControlledComponent())
        self.game_entities.append(p2_id)
        # Pelota
        ball_id = self.game.world.create_entity()
        self.game.world.add_component(ball_id, PositionComponent(self.game.screen_width / 2 - 10, self.game.screen_height / 2 - 10))
        self.game.world.add_component(ball_id, DimensionsComponent(20, 20))
        self.game.world.add_component(ball_id, VelocityComponent(300, 300))
        self.game.world.add_component(ball_id, BallComponent())
        self.game_entities.append(ball_id)
        # Puntuaciones
        score1_id = self.game.world.create_entity()
        self.game.world.add_component(score1_id, PositionComponent(self.game.screen_width / 4, 50))
        self.game.world.add_component(score1_id, ScoreComponent(player_number=1))
        self.game_entities.append(score1_id)
        score2_id = self.game.world.create_entity()
        self.game.world.add_component(score2_id, PositionComponent(self.game.screen_width * 3 / 4, 50))
        self.game.world.add_component(score2_id, ScoreComponent(player_number=2))
        self.game_entities.append(score2_id)

    def cleanup(self):
        """
        Removes all entities created by this scene and clears particles.
        """
        for entity_id in self.game_entities:
            self.game.world.remove_entity(entity_id)
        for entity_id in list(self.game.world.get_entities_with_components(ParticleComponent)):
            self.game.world.remove_entity(entity_id)
        self.game_entities.clear()

    def handle_events(self, events):
        """
        Processes player input, pause button clicks, and ESC key for pausing.

        Args:
            events (list): List of Pygame events.
        """
        self.player_input_system.process(events)
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.game.game_state_manager.set_state(GameState.PAUSA)
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mx, my = event.pos
                for e in self.game.world.get_entities_with_components(PauseButtonComponent, PositionComponent, DimensionsComponent):
                    pos = self.game.world.get_component(e, PositionComponent)
                    dim = self.game.world.get_component(e, DimensionsComponent)
                    if pos.x <= mx <= pos.x + dim.width and pos.y <= my <= pos.y + dim.height:
                        self.game.game_state_manager.set_state(GameState.PAUSA); return

    def update(self, dt):
        """
        Updates all game systems, including movement, AI, collisions, powerups, and scoring.

        Args:
            dt (float): Delta time since last frame.
        """
        self.particle_system.update(dt)
        if not self.scoring_system.waiting_to_reset:
            self.ai_system.process()
            self.movement_system.process(dt)
            self.ball_boundary_system.process()
            self.paddle_collision_system.process(self.powerup_collision_system)
            self.powerup_spawning_system.process()
            self.powerup_collision_system.process()
            self.powerup_effect_system.process()
        self.scoring_system.process()

    def draw(self, screen):
        """
        Renders all game entities, particles, and draws the pause button.

        Args:
            screen: The Pygame surface to draw on.
        """
        self.render_system.process()
        
        # CORRECCIÓN: Añadida la llamada para dibujar las partículas
        self.particle_system.draw(screen)

        # Dibujar el botón de pausa
        for e in self.game.world.get_entities_with_components(PauseButtonComponent, PositionComponent, DimensionsComponent):
            pos, dim = self.game.world.get_component(e, PositionComponent), self.game.world.get_component(e, DimensionsComponent)
            rect = pygame.Rect(pos.x, pos.y, dim.width, dim.height)
            mx, my = pygame.mouse.get_pos()
            color = (220, 220, 220) if rect.collidepoint(mx, my) else (180, 180, 180)
            pygame.draw.rect(screen, color, rect, border_radius=8)
            pygame.draw.rect(screen, (20, 20, 20), (pos.x + 12, pos.y + 10, 8, 30), border_radius=2)
            pygame.draw.rect(screen, (20, 20, 20), (pos.x + 30, pos.y + 10, 8, 30), border_radius=2)

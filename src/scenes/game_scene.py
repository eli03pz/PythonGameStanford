# ARCHIVO: scenes/game_scene.py

import pygame
from scenes.base_scene import BaseScene
from utils.game_state import GameState

# Importamos los componentes necesarios
from components.game_components import *
from components.menu_components import PositionComponent, DimensionsComponent

# Importamos los sistemas refactorizados
from systems.game_systems import (
    MovementSystem, PlayerInputSystem, AISystem, GameRenderSystem,
    BallBoundarySystem, PaddleCollisionSystem, ScoringSystem # <-- Nuevos sistemas
)

class GameScene(BaseScene):
    def __init__(self, game, num_players):
        super().__init__(game)
        self.num_players = num_players
        self.game_entities = []

    def setup(self):
        print(f"GameScene: Configurando para {self.num_players} jugador(es).")
        
        # --- 1. Crear los sistemas del juego (ahora más especializados) ---
        self.player_input_system = PlayerInputSystem(self.game.world, self.game.config_manager)
        self.ai_system = AISystem(self.game.world, self.game.screen_height)
        self.movement_system = MovementSystem(self.game.world, self.game.screen_height)
        
        # Reemplazamos CollisionSystem por tres sistemas más pequeños
        self.ball_boundary_system = BallBoundarySystem(self.game.world, self.game.screen_height)
        self.paddle_collision_system = PaddleCollisionSystem(self.game.world)
        self.scoring_system = ScoringSystem(self.game.world, self.game.screen_width, self.game.screen_height)

        self.render_system = GameRenderSystem(self.game.world, self.game.screen)

        # --- 2. La creación de entidades no cambia ---
        # (El código para crear palas, pelota y puntuaciones es el mismo de antes)
        paddle_dims = DimensionsComponent(15, 100)
        p1_id = self.game.world.create_entity()
        self.game.world.add_component(p1_id, PositionComponent(50, self.game.screen_height / 2 - paddle_dims.height / 2))
        self.game.world.add_component(p1_id, paddle_dims)
        self.game.world.add_component(p1_id, VelocityComponent(0, 0))
        self.game.world.add_component(p1_id, PaddleComponent(player_number=1))
        self.game_entities.append(p1_id)
        p2_id = self.game.world.create_entity()
        self.game.world.add_component(p2_id, PositionComponent(self.game.screen_width - 50 - paddle_dims.width, self.game.screen_height / 2 - paddle_dims.height / 2))
        self.game.world.add_component(p2_id, paddle_dims)
        self.game.world.add_component(p2_id, VelocityComponent(0, 0))
        if self.num_players == 2: self.game.world.add_component(p2_id, PaddleComponent(player_number=2))
        else: self.game.world.add_component(p2_id, AIControlledComponent())
        self.game_entities.append(p2_id)
        ball_id = self.game.world.create_entity()
        self.game.world.add_component(ball_id, PositionComponent(self.game.screen_width / 2 - 10, self.game.screen_height / 2 - 10))
        self.game.world.add_component(ball_id, DimensionsComponent(20, 20))
        self.game.world.add_component(ball_id, VelocityComponent(300, 300))
        self.game.world.add_component(ball_id, BallComponent())
        self.game_entities.append(ball_id)
        score1_id = self.game.world.create_entity()
        self.game.world.add_component(score1_id, PositionComponent(self.game.screen_width / 4, 50))
        self.game.world.add_component(score1_id, ScoreComponent(player_number=1))
        self.game_entities.append(score1_id)
        score2_id = self.game.world.create_entity()
        self.game.world.add_component(score2_id, PositionComponent(self.game.screen_width * 3 / 4, 50))
        self.game.world.add_component(score2_id, ScoreComponent(player_number=2))
        self.game_entities.append(score2_id)

    def cleanup(self):
        print(f"GameScene: Limpiando {len(self.game_entities)} entidades de juego.")
        for entity_id in self.game_entities:
            self.game.world.remove_entity(entity_id)
        self.game_entities.clear()

    def handle_events(self, events):
        self.player_input_system.process(events)
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.game.game_state_manager.set_state(GameState.MENU_PRINCIPAL)

    def update(self, dt):
        # La lógica se ejecuta en un orden específico y ahora es más legible
        self.ai_system.process()
        self.movement_system.process(dt)
        self.ball_boundary_system.process()
        self.paddle_collision_system.process()
        self.scoring_system.process()

    def draw(self, screen):
        self.render_system.process()


# ARCHIVO: scenes/game_scene.py

import pygame
from scenes.base_scene import BaseScene
from utils.game_state import GameState
# Importamos todos los componentes y sistemas que usaremos
from components.game_components import *
from systems.game_systems import *
from components.menu_components import PositionComponent, DimensionsComponent

# Componente simple para el botón de pausa
class PauseButtonComponent: pass

class GameScene(BaseScene):
    def __init__(self, game, num_players):
        super().__init__(game)
        self.num_players = num_players
        self.game_entities = []

    def setup(self):
        """
        Configura la escena del juego, creando todos los sistemas y entidades necesarios.
        """
        print(f"GameScene: Configurando para {self.num_players} jugador(es).")
        
        # --- 1. Crear los sistemas del juego ---
        # CORRECCIÓN: Nos aseguramos de pasar las dependencias correctas (self.game.world, etc.)
        self.player_input_system = PlayerInputSystem(self.game.world, self.game.config_manager)
        self.ai_system = AISystem(self.game.world, self.game.screen_height)
        self.movement_system = MovementSystem(self.game.world, self.game.screen_height)
        self.ball_boundary_system = BallBoundarySystem(self.game.world, self.game.screen_height)
        self.paddle_collision_system = PaddleCollisionSystem(self.game.world)
        self.scoring_system = ScoringSystem(self.game.world, self.game.screen_width, self.game.screen_height)
        self.render_system = GameRenderSystem(self.game.world, self.game.screen)

        # --- 2. Crear las entidades del juego ---
        
        # --- AÑADIR BOTÓN DE PAUSA ---
        pause_button_id = self.game.world.create_entity()
        self.game_entities.append(pause_button_id)
        # CORRECCIÓN: Usamos self.game.world para acceder al ECSWorld
        self.game.world.add_component(pause_button_id, PositionComponent(self.game.screen_width - 60, 10))
        self.game.world.add_component(pause_button_id, DimensionsComponent(50, 50))
        self.game.world.add_component(pause_button_id, PauseButtonComponent())
        
        # --- CREAR PALAS, PELOTA Y MARCADORES ---
        paddle_dims = DimensionsComponent(15, 100)
        
        # Pala del Jugador 1
        p1_id = self.game.world.create_entity()
        self.game.world.add_component(p1_id, PositionComponent(50, self.game.screen_height / 2 - paddle_dims.height / 2))
        self.game.world.add_component(p1_id, paddle_dims)
        self.game.world.add_component(p1_id, VelocityComponent(0, 0))
        self.game.world.add_component(p1_id, PaddleComponent(player_number=1))
        self.game_entities.append(p1_id)

        # Pala del Jugador 2 (o de la IA)
        p2_id = self.game.world.create_entity()
        self.game.world.add_component(p2_id, PositionComponent(self.game.screen_width - 50 - paddle_dims.width, self.game.screen_height / 2 - paddle_dims.height / 2))
        self.game.world.add_component(p2_id, paddle_dims)
        self.game.world.add_component(p2_id, VelocityComponent(0, 0))
        if self.num_players == 2:
            self.game.world.add_component(p2_id, PaddleComponent(player_number=2))
        else:
            self.game.world.add_component(p2_id, AIControlledComponent())
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
        print(f"GameScene: Limpiando {len(self.game_entities)} entidades de juego.")
        for entity_id in self.game_entities:
            self.game.world.remove_entity(entity_id)
        self.game_entities.clear()

    def handle_events(self, events):
        self.player_input_system.process(events)
        for event in events:
            # Pausar con la tecla ESC
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.game.game_state_manager.set_state(GameState.PAUSA)
            # Pausar con clic en el botón
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mx, my = event.pos
                for e in self.game.world.get_entities_with_components(PauseButtonComponent, PositionComponent, DimensionsComponent):
                    pos = self.game.world.get_component(e, PositionComponent)
                    dim = self.game.world.get_component(e, DimensionsComponent)
                    if pos.x <= mx <= pos.x + dim.width and pos.y <= my <= pos.y + dim.height:
                        self.game.game_state_manager.set_state(GameState.PAUSA)
                        return

    def update(self, dt):
        self.ai_system.process()
        self.movement_system.process(dt)
        self.ball_boundary_system.process()
        self.paddle_collision_system.process()
        self.scoring_system.process()

    def draw(self, screen):
        # Dibujar entidades del juego (palas, pelota, marcador)
        self.render_system.process()
        
        # Dibujar el botón de pausa
        for e in self.game.world.get_entities_with_components(PauseButtonComponent, PositionComponent, DimensionsComponent):
            pos = self.game.world.get_component(e, PositionComponent)
            dim = self.game.world.get_component(e, DimensionsComponent)
            rect = pygame.Rect(pos.x, pos.y, dim.width, dim.height)
            # Damos un estilo al botón
            mx, my = pygame.mouse.get_pos()
            color = (220, 220, 220) if rect.collidepoint(mx, my) else (180, 180, 180)
            pygame.draw.rect(screen, color, rect, border_radius=8)
            # Dibujar las dos barras de pausa
            pygame.draw.rect(screen, (20, 20, 20), (pos.x + 12, pos.y + 10, 8, 30), border_radius=2)
            pygame.draw.rect(screen, (20, 20, 20), (pos.x + 30, pos.y + 10, 8, 30), border_radius=2)

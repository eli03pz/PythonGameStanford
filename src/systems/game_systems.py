# ARCHIVO: systems/game_systems.py
# RESPONSABILIDAD: Implementar la lógica del juego siguiendo el Principio de Responsabilidad Única.

import pygame
import random
from components.menu_components import PositionComponent, DimensionsComponent
from components.game_components import (
    VelocityComponent, PaddleComponent, BallComponent, ScoreComponent, AIControlledComponent
)

# --- SISTEMAS DE MOVIMIENTO Y CONTROL (Sin cambios, ya cumplen con SRP) ---

class MovementSystem:
    def __init__(self, world, screen_height):
        self.world = world
        self.screen_height = screen_height
    def process(self, dt):
        for entity in self.world.get_entities_with_components(PositionComponent, VelocityComponent):
            pos = self.world.get_component(entity, PositionComponent)
            vel = self.world.get_component(entity, VelocityComponent)
            pos.x += vel.vx * dt
            pos.y += vel.vy * dt
            if self.world.get_component(entity, PaddleComponent) or self.world.get_component(entity, AIControlledComponent):
                dim = self.world.get_component(entity, DimensionsComponent)
                pos.y = max(0, min(pos.y, self.screen_height - dim.height))

class PlayerInputSystem:
    def __init__(self, world, config_manager):
        self.world = world
        self.config_manager = config_manager
        self.paddle_speed = 400

    def process(self, events):
        keys = pygame.key.get_pressed()
        for entity in self.world.get_entities_with_components(VelocityComponent, PaddleComponent):
            vel = self.world.get_component(entity, VelocityComponent)
            paddle = self.world.get_component(entity, PaddleComponent)
            
            if paddle.player_number == 1:
                key_up = self.config_manager.get_p1_key('up')
                key_down = self.config_manager.get_p1_key('down')
                if keys[key_up]: vel.vy = -self.paddle_speed
                elif keys[key_down]: vel.vy = self.paddle_speed
                else: vel.vy = 0
            
            elif paddle.player_number == 2:
                key_up = self.config_manager.get_p2_key('up')
                key_down = self.config_manager.get_p2_key('down')
                if keys[key_up]: vel.vy = -self.paddle_speed
                elif keys[key_down]: vel.vy = self.paddle_speed
                else: vel.vy = 0

class AISystem:
    def __init__(self, world, screen_height):
        self.world = world
        self.screen_height = screen_height
        self.paddle_speed = 300
    def process(self):
        ball_pos = next((self.world.get_component(e, PositionComponent) for e in self.world.get_entities_with_components(PositionComponent, BallComponent)), None)
        if not ball_pos: return
        for entity in self.world.get_entities_with_components(PositionComponent, VelocityComponent, AIControlledComponent):
            pos = self.world.get_component(entity, PositionComponent)
            vel = self.world.get_component(entity, VelocityComponent)
            dim = self.world.get_component(entity, DimensionsComponent)
            paddle_center = pos.y + dim.height / 2
            if ball_pos.y < paddle_center - 10: vel.vy = -self.paddle_speed
            elif ball_pos.y > paddle_center + 10: vel.vy = self.paddle_speed
            else: vel.vy = 0

# --- NUEVOS SISTEMAS ESPECIALIZADOS DE FÍSICA Y REGLAS ---

class BallBoundarySystem:
    """ÚNICA RESPONSABILIDAD: Gestionar la colisión de la pelota con los bordes superior e inferior."""
    def __init__(self, world, screen_height):
        self.world = world
        self.sh = screen_height
    def process(self):
        for ball_id in self.world.get_entities_with_components(BallComponent, PositionComponent, VelocityComponent, DimensionsComponent):
            b_pos = self.world.get_component(ball_id, PositionComponent)
            b_vel = self.world.get_component(ball_id, VelocityComponent)
            b_dim = self.world.get_component(ball_id, DimensionsComponent)
            if (b_pos.y <= 0 and b_vel.vy < 0) or (b_pos.y >= self.sh - b_dim.height and b_vel.vy > 0):
                b_vel.vy *= -1

class PaddleCollisionSystem:
    """ÚNICA RESPONSABILIDAD: Gestionar la colisión de la pelota con las palas."""
    def __init__(self, world):
        self.world = world
    def process(self):
        for ball_id in self.world.get_entities_with_components(BallComponent, PositionComponent, VelocityComponent, DimensionsComponent):
            b_pos = self.world.get_component(ball_id, PositionComponent)
            b_vel = self.world.get_component(ball_id, VelocityComponent)
            b_dim = self.world.get_component(ball_id, DimensionsComponent)
            ball_rect = pygame.Rect(b_pos.x, b_pos.y, b_dim.width, b_dim.height)

            for paddle_id in self.world.get_entities_with_components(PositionComponent, DimensionsComponent):
                is_paddle = self.world.get_component(paddle_id, PaddleComponent) or self.world.get_component(paddle_id, AIControlledComponent)
                if is_paddle:
                    p_pos = self.world.get_component(paddle_id, PositionComponent)
                    p_dim = self.world.get_component(paddle_id, DimensionsComponent)
                    paddle_rect = pygame.Rect(p_pos.x, p_pos.y, p_dim.width, p_dim.height)
                    
                    if ball_rect.colliderect(paddle_rect):
                        # Evitar que la bola se quede "pegada"
                        if (b_vel.vx < 0 and ball_rect.left < paddle_rect.right) or \
                           (b_vel.vx > 0 and ball_rect.right > paddle_rect.left):
                            b_vel.vx *= -1.1
                            b_vel.vy = random.uniform(-1.5, 1.5) * 200
                            # Pequeño empuje para evitar recolisión
                            b_pos.x += b_vel.vx * 0.05 
                            return # Salir tras una colisión para evitar bugs

class ScoringSystem:
    """ÚNICA RESPONSABILIDAD: Gestionar la puntuación y el reseteo de la pelota."""
    def __init__(self, world, screen_width, screen_height):
        self.world = world
        self.sw = screen_width
        self.sh = screen_height
    def process(self):
        for ball_id in self.world.get_entities_with_components(BallComponent, PositionComponent):
            b_pos = self.world.get_component(ball_id, PositionComponent)
            b_dim = self.world.get_component(ball_id, DimensionsComponent)
            
            # Punto para jugador 2
            if b_pos.x <= -b_dim.width:
                self.handle_score(ball_id, 2)
                return
            # Punto para jugador 1
            if b_pos.x >= self.sw:
                self.handle_score(ball_id, 1)
                return
                
    def handle_score(self, ball_id, scoring_player):
        for score_entity in self.world.get_entities_with_components(ScoreComponent):
            score_comp = self.world.get_component(score_entity, ScoreComponent)
            if score_comp and score_comp.player_number == scoring_player:
                score_comp.score += 1
                break
        self.reset_ball(ball_id)

    def reset_ball(self, ball_id):
        b_pos = self.world.get_component(ball_id, PositionComponent)
        b_vel = self.world.get_component(ball_id, VelocityComponent)
        b_pos.x, b_pos.y = self.sw / 2 - 10, self.sh / 2 - 10
        b_vel.vx = 300 * random.choice([-1, 1])
        b_vel.vy = 300 * random.choice([-1, 1])

# --- SISTEMA DE RENDERIZADO (Sin cambios, ya cumple con SRP) ---

class GameRenderSystem:
    def __init__(self, world, screen):
        self.world = world
        self.screen = screen
        self.font = pygame.font.Font(None, 74)
    def process(self):
        for entity in self.world.get_entities_with_components(PositionComponent, DimensionsComponent):
            if self.world.get_component(entity, PaddleComponent) or self.world.get_component(entity, AIControlledComponent) or self.world.get_component(entity, BallComponent):
                pos = self.world.get_component(entity, PositionComponent)
                dim = self.world.get_component(entity, DimensionsComponent)
                pygame.draw.rect(self.screen, "white", (pos.x, pos.y, dim.width, dim.height))
        for entity in self.world.get_entities_with_components(PositionComponent, ScoreComponent):
            pos = self.world.get_component(entity, PositionComponent)
            score = self.world.get_component(entity, ScoreComponent)
            text_surface = self.font.render(str(score.score), True, "white")
            text_rect = text_surface.get_rect(center=(pos.x, pos.y))
            self.screen.blit(text_surface, text_rect)

"""
game_systems.py
---------------
Implements core ECS systems for game logic, including movement, input, AI, collisions,
scoring, and rendering.

Classes:
    MovementSystem: Updates entity positions based on velocity.
    PlayerInputSystem: Handles player input for paddle movement.
    AISystem: Controls AI paddle movement.
    BallBoundarySystem: Handles ball collisions with screen boundaries.
    PaddleCollisionSystem: Handles ball and paddle collisions, including shrink mode.
    ScoringSystem: Manages scoring, ball resets, and win conditions.
    GameRenderSystem: Renders paddles, ball, powerups, and scores.
"""

import pygame
import random
from components.menu_components import PositionComponent, DimensionsComponent
from components.game_components import *
from components.powerup_components import *
from components.effects_components import ParticleComponent
from utils.utils import *

class MovementSystem:
    """
    Updates entity positions based on their velocity.

    Attributes:
        world: Reference to the ECS world.
        screen_height (int): Height of the game screen.

    Methods:
        process(dt): Updates positions and clamps paddles within screen bounds.
    """
    def __init__(self, world, screen_height):
        self.world = world
        self.screen_height = screen_height
    def process(self, dt):
        for entity in self.world.get_entities_with_components(PositionComponent, VelocityComponent):
            pos, vel = self.world.get_component(entity, PositionComponent), self.world.get_component(entity, VelocityComponent)
            if not all([pos, vel]): continue
            pos.x += vel.vx * dt
            pos.y += vel.vy * dt
            if self.world.get_component(entity, PaddleComponent) or self.world.get_component(entity, AIControlledComponent):
                dim = self.world.get_component(entity, DimensionsComponent)
                if not dim: continue
                pos.y = clamp(pos.y, 0, self.screen_height - dim.height)

class PlayerInputSystem:
    """
    Handles player input for paddle movement.

    Attributes:
        world: Reference to the ECS world.
        config_manager: Reference to the ConfigManager.
        paddle_speed (int): Speed of paddle movement.

    Methods:
        process(events): Updates paddle velocity based on key presses.
    """
    def __init__(self, world, config_manager):
        self.world, self.config_manager, self.paddle_speed = world, config_manager, 400
    def process(self, events):
        keys = pygame.key.get_pressed()
        for entity in self.world.get_entities_with_components(VelocityComponent, PaddleComponent):
            vel, paddle = self.world.get_component(entity, VelocityComponent), self.world.get_component(entity, PaddleComponent)
            if not all([vel, paddle]): continue
            if paddle.player_number == 1:
                key_up, key_down = self.config_manager.get_p1_key('up'), self.config_manager.get_p1_key('down')
                if keys[key_up]: vel.vy = -self.paddle_speed
                elif keys[key_down]: vel.vy = self.paddle_speed
                else: vel.vy = 0
            elif paddle.player_number == 2:
                key_up, key_down = self.config_manager.get_p2_key('up'), self.config_manager.get_p2_key('down')
                if keys[key_up]: vel.vy = -self.paddle_speed
                elif keys[key_down]: vel.vy = self.paddle_speed
                else: vel.vy = 0

class AISystem:
    """
    Controls AI paddle movement to follow the ball.

    Attributes:
        world: Reference to the ECS world.
        screen_height (int): Height of the game screen.
        paddle_speed (int): Speed of AI paddle movement.

    Methods:
        process(): Updates AI paddle velocity to track the ball.
    """
    def __init__(self, world, screen_height):
        self.world, self.screen_height, self.paddle_speed = world, screen_height, 300
    def process(self):
        ball_entities = self.world.get_entities_with_components(PositionComponent, BallComponent)
        ball_pos = next((self.world.get_component(e, PositionComponent) for e in ball_entities), None)
        if not ball_pos: return
        for entity in self.world.get_entities_with_components(PositionComponent, VelocityComponent, AIControlledComponent):
            pos, vel, dim = self.world.get_component(entity, PositionComponent), self.world.get_component(entity, VelocityComponent), self.world.get_component(entity, DimensionsComponent)
            if not all([pos, vel, dim]): continue
            paddle_center = pos.y + dim.height / 2
            if ball_pos.y < paddle_center - 10: vel.vy = -self.paddle_speed
            elif ball_pos.y > paddle_center + 10: vel.vy = self.paddle_speed
            else: vel.vy = 0

class BallBoundarySystem:
    """
    Handles ball collisions with the top and bottom boundaries of the screen.

    Attributes:
        world: Reference to the ECS world.
        sh (int): Screen height.

    Methods:
        process(): Inverts ball vertical velocity if it hits the top or bottom edge.
    """
    def __init__(self, world, screen_height):
        self.world, self.sh = world, screen_height
    def process(self):
        for ball_id in self.world.get_entities_with_components(BallComponent, PositionComponent, VelocityComponent, DimensionsComponent):
            b_pos, b_vel, b_dim = self.world.get_component(ball_id, PositionComponent), self.world.get_component(ball_id, VelocityComponent), self.world.get_component(ball_id, DimensionsComponent)
            if not all([b_pos, b_vel, b_dim]): continue
            if (b_pos.y <= 0 and b_vel.vy < 0) or (b_pos.y >= self.sh - b_dim.height and b_vel.vy > 0):
                b_vel.vy *= -1

class PaddleCollisionSystem:
    """
    Handles ball and paddle collisions, including shrink mode and hit effects.

    Attributes:
        world: Reference to the ECS world.
        game_mode (str): Current game mode.

    Methods:
        process(powerup_collision_system): Handles collision logic and effects.
        calculate_bounce_vy(ball_rect, paddle_rect): Calculates new ball vertical velocity after collision.
    """
    def __init__(self, world, game_mode='classic'):
        self.world, self.game_mode = world, game_mode
    def process(self, powerup_collision_system):
        ball_entities = self.world.get_entities_with_components(BallComponent)
        ball_entity = next(iter(ball_entities), None)
        if not ball_entity: return
        b_pos, b_vel, b_dim = self.world.get_component(ball_entity, PositionComponent), self.world.get_component(ball_entity, VelocityComponent), self.world.get_component(ball_entity, DimensionsComponent)
        if not all([b_pos, b_vel, b_dim]): return
        ball_rect = pygame.Rect(b_pos.x, b_pos.y, b_dim.width, b_dim.height)
        paddles_and_ai = list(self.world.get_entities_with_components(PaddleComponent)) + list(self.world.get_entities_with_components(AIControlledComponent))
        for paddle_id in paddles_and_ai:
            p_pos, p_dim = self.world.get_component(paddle_id, PositionComponent), self.world.get_component(paddle_id, DimensionsComponent)
            if not all([p_pos, p_dim]): continue
            paddle_rect = pygame.Rect(p_pos.x, p_pos.y, p_dim.width, p_dim.height)
            if ball_rect.colliderect(paddle_rect):
                if (b_vel.vx < 0 and ball_rect.left < paddle_rect.right) or (b_vel.vx > 0 and ball_rect.right > paddle_rect.left):
                    if b_vel.vx < 0: b_pos.x = paddle_rect.right
                    else: b_pos.x = paddle_rect.left - b_dim.width
                    b_vel.vx *= -1.1
                    b_vel.vy = self.calculate_bounce_vy(ball_rect, paddle_rect)
                    self.world.add_component(paddle_id, HitFlashComponent(150))
                    if self.game_mode == 'shrink':
                        if p_dim and p_dim.height > 20: p_dim.height -= 5
                    powerup_collision_system.last_paddle_hit = paddle_id
                    break
    def calculate_bounce_vy(self, ball_rect, paddle_rect):
        """
        Calculates new ball vertical velocity after collision.

        Args:
            ball_rect (pygame.Rect): Ball rectangle.
            paddle_rect (pygame.Rect): Paddle rectangle.

        Returns:
            float: New vertical velocity for the ball.
        """
        relative_intersect = (paddle_rect.centery - ball_rect.centery) / (paddle_rect.height / 2)
        return -relative_intersect * 400

class ScoringSystem:
    """
    Manages scoring, ball resets, and win conditions.

    Attributes:
        world: Reference to the ECS world.
        sw (int): Screen width.
        sh (int): Screen height.
        waiting_to_reset (bool): True if waiting to reset the ball.
        reset_timer (int): Time to reset the ball.
        ball_to_reset: Entity ID of the ball to reset.

    Methods:
        process(): Handles scoring and ball reset logic.
        handle_score(ball_id, scoring_player): Updates score and triggers confetti.
        create_confetti(x, y): Spawns confetti particles.
        reset_ball(ball_id): Resets ball position and velocity.
    """
    def __init__(self, world, screen_width, screen_height):
        self.world, self.sw, self.sh = world, screen_width, screen_height
        self.waiting_to_reset = False
        self.reset_timer = 0
        self.ball_to_reset = None
    def process(self):
        if self.waiting_to_reset and pygame.time.get_ticks() >= self.reset_timer:
            self.reset_ball(self.ball_to_reset)
            self.waiting_to_reset = False
            self.ball_to_reset = None
        if not self.waiting_to_reset:
            for ball_id in self.world.get_entities_with_components(BallComponent, PositionComponent):
                b_pos, b_dim = self.world.get_component(ball_id, PositionComponent), self.world.get_component(ball_id, DimensionsComponent)
                if not all([b_pos, b_dim]): continue
                if b_pos.x <= -b_dim.width: self.handle_score(ball_id, 2); break
                if b_pos.x >= self.sw: self.handle_score(ball_id, 1); break
    def handle_score(self, ball_id, scoring_player):
        for score_entity in self.world.get_entities_with_components(ScoreComponent):
            score_comp = self.world.get_component(score_entity, ScoreComponent)
            if score_comp and score_comp.player_number == scoring_player:
                score_comp.score += 1
                if score_comp.score >= WINNING_SCORE:
                    print(f"JUGADOR {scoring_player} GANA!")
                    # Aquí podrías cambiar a una escena de fin de juego
                break
        b_pos = self.world.get_component(ball_id, PositionComponent)
        b_vel = self.world.get_component(ball_id, VelocityComponent)
        if b_pos: self.create_confetti(b_pos.x, b_pos.y)
        if b_vel: b_vel.vx, b_vel.vy = 0, 0
        self.waiting_to_reset = True
        self.reset_timer = pygame.time.get_ticks() + 1000
        self.ball_to_reset = ball_id
    def create_confetti(self, x, y):
        for _ in range(30):
            entity = self.world.create_entity()
            self.world.add_component(entity, PositionComponent(x, y))
            velocity = (pygame.math.Vector2(1, 0).rotate(random.uniform(0, 360))) * random.uniform(50, 200)
            self.world.add_component(entity, ParticleComponent(random.randint(500, 1500), velocity, random.choice(CONFETTI_COLORS)))
    def reset_ball(self, ball_id):
        b_pos, b_vel = self.world.get_component(ball_id, PositionComponent), self.world.get_component(ball_id, VelocityComponent)
        if not all([b_pos, b_vel]): return
        b_pos.x, b_pos.y = self.sw / 2 - 10, self.sh / 2 - 10
        b_vel.vx, b_vel.vy = 300 * random.choice([-1, 1]), 300 * random.choice([-1, 1])

class GameRenderSystem:
    """
    Renders paddles, ball, powerups, and scores.

    Attributes:
        world: Reference to the ECS world.
        screen: Pygame surface to draw on.
        font: Font for rendering scores.

    Methods:
        process(): Draws all game entities and scores.
    """
    def __init__(self, world, screen):
        self.world, self.screen, self.font = world, screen, pygame.font.Font(None, 74)
    def process(self):
        current_time = pygame.time.get_ticks()
        for entity in self.world.get_entities_with_components(PositionComponent, DimensionsComponent):
            pos, dim = self.world.get_component(entity, PositionComponent), self.world.get_component(entity, DimensionsComponent)
            if not all([pos, dim]): continue
            if self.world.get_component(entity, PaddleComponent) or self.world.get_component(entity, AIControlledComponent):
                color = COLOR_PADDLE
                hit_flash = self.world.get_component(entity, HitFlashComponent)
                if hit_flash:
                    if current_time < hit_flash.activation_time + hit_flash.duration: color = COLOR_HIT_FLASH
                    else: self.world.remove_component(entity, HitFlashComponent)
                pygame.draw.rect(self.screen, color, (pos.x, pos.y, dim.width, dim.height))
            elif self.world.get_component(entity, BallComponent):
                pygame.draw.rect(self.screen, COLOR_BALL, (pos.x, pos.y, dim.width, dim.height))
            elif self.world.get_component(entity, PowerupComponent):
                pygame.draw.rect(self.screen, COLOR_POWERUP, (pos.x, pos.y, dim.width, dim.height))
        for entity in self.world.get_entities_with_components(PositionComponent, ScoreComponent):
            pos, score = self.world.get_component(entity, PositionComponent), self.world.get_component(entity, ScoreComponent)
            if not all([pos, score]): continue
            text_surf = self.font.render(str(score.score), True, COLOR_WHITE)
            self.screen.blit(text_surf, text_surf.get_rect(center=(pos.x, pos.y)))

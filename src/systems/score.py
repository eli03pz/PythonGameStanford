"""
score.py
--------
Implements the ScoringSystem for managing scores, ball resets, and confetti effects
when a player scores in the game.

Classes:
    ScoringSystem: Handles score updates, ball reset logic, and confetti particle spawning.
"""

import random
import pygame

from components.effects_components import ParticleComponent
from components.game_components import BallComponent, ScoreComponent, VelocityComponent
from components.menu_components import DimensionsComponent, PositionComponent


class ScoringSystem:
    """
    Handles score updates, ball reset logic, and confetti particle spawning.

    Attributes:
        world: Reference to the ECS world.
        sw (int): Screen width.
        sh (int): Screen height.
        waiting_to_reset (bool): True if waiting to reset the ball after a score.
        reset_timer (int): Time (ms) to reset the ball.
        ball_to_reset: Entity ID of the ball to reset.

    Methods:
        process(): Checks for scoring events and manages ball reset timing.
        handle_score(ball_id, scoring_player): Updates score and triggers confetti.
        create_confetti(x, y): Spawns confetti particles at the given position.
        reset_ball(ball_id): Resets ball position and velocity after a score.
    """
    def __init__(self, world, screen_width, screen_height):
        self.world, self.sw, self.sh = world, screen_width, screen_height
        self.waiting_to_reset = False
        self.reset_timer = 0
        self.ball_to_reset = None

    def process(self):
        """
        Checks for scoring events and manages ball reset timing.
        """
        if self.waiting_to_reset and pygame.time.get_ticks() >= self.reset_timer:
            self.reset_ball(self.ball_to_reset)
            self.waiting_to_reset = False
            self.ball_to_reset = None
        
        if not self.waiting_to_reset:
            for ball_id in self.world.get_entities_with_components(BallComponent, PositionComponent):
                b_pos, b_dim = self.world.get_component(ball_id, PositionComponent), self.world.get_component(ball_id, DimensionsComponent)
                if not all([b_pos, b_dim]): continue
                # CORRECCIÓN: Usamos 'break' para salir del bucle de la pelota (solo hay una).
                if b_pos.x <= -b_dim.width: self.handle_score(ball_id, 2); break
                if b_pos.x >= self.sw: self.handle_score(ball_id, 1); break
                
    def handle_score(self, ball_id, scoring_player):
        """
        Updates the score for the scoring player and triggers confetti effect.

        Args:
            ball_id: Entity ID of the ball.
            scoring_player (int): Player number who scored.
        """
        for score_entity in self.world.get_entities_with_components(ScoreComponent):
            score_comp = self.world.get_component(score_entity, ScoreComponent)
            if score_comp and score_comp.player_number == scoring_player:
                score_comp.score += 1
                break
        
        b_pos = self.world.get_component(ball_id, PositionComponent)
        b_vel = self.world.get_component(ball_id, VelocityComponent)
        if b_pos: self.create_confetti(b_pos.x, b_pos.y)
        if b_vel: b_vel.vx, b_vel.vy = 0, 0
        
        self.waiting_to_reset = True
        self.reset_timer = pygame.time.get_ticks() + 1000
        self.ball_to_reset = ball_id

    def create_confetti(self, x, y):
        """
        Spawns confetti particles at the given position.

        Args:
            x (float): X coordinate for confetti spawn.
            y (float): Y coordinate for confetti spawn.
        """
        for _ in range(30):
            entity = self.world.create_entity()
            self.world.add_component(entity, PositionComponent(x, y))
            velocity = (pygame.math.Vector2(1, 0).rotate(random.uniform(0, 360))) * random.uniform(50, 200)
            lifetime = random.randint(500, 1500)
            color = random.choice([(255, 192, 203), (173, 216, 230), (255, 255, 0), (144, 238, 144)])
            self.world.add_component(entity, ParticleComponent(lifetime, velocity, color))

    def reset_ball(self, ball_id):
        """
        Resets ball position and velocity after a score.

        Args:
            ball_id: Entity ID of the ball to reset.
        """
        b_pos, b_vel = self.world.get_component(ball_id, PositionComponent), self.world.get_component(ball_id, VelocityComponent)
        if not all([b_pos, b_vel]): return
        b_pos.x, b_pos.y = self.sw / 2 - 10, self.sh / 2 - 10
        b_vel.vx, b_vel.vy = 300 * random.choice([-1, 1]), 300 * random.choice([-1, 1])

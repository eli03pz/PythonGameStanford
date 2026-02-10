"""
environment.py
--------------
Implements ECS systems related to the game environment, such as ball boundary handling.

Classes:
    BallBoundarySystem: Handles ball collisions with the top and bottom boundaries of the screen.
"""

from components.game_components import BallComponent, VelocityComponent
from components.menu_components import DimensionsComponent, PositionComponent


class BallBoundarySystem:
    """
    Handles ball collisions with the top and bottom boundaries of the screen.

    Attributes:
        world: Reference to the ECS world.
        sh (int): Screen height.

    Methods:
        process():
            Checks each ball entity and inverts its vertical velocity if it hits the top or bottom edge.
    """
    def __init__(self, world, screen_height):
        self.world, self.sh = world, screen_height
    def process(self):
        """
        Checks each ball entity and inverts its vertical velocity if it hits the top or bottom edge.
        """
        for ball_id in self.world.get_entities_with_components(BallComponent, PositionComponent, VelocityComponent, DimensionsComponent):
            b_pos, b_vel, b_dim = self.world.get_component(ball_id, PositionComponent), self.world.get_component(ball_id, VelocityComponent), self.world.get_component(ball_id, DimensionsComponent)
            if not all([b_pos, b_vel, b_dim]): continue
            if (b_pos.y <= 0 and b_vel.vy < 0) or (b_pos.y >= self.sh - b_dim.height and b_vel.vy > 0):
                b_vel.vy *= -1

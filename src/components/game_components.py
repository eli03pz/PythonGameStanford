"""
game_components.py
------------------
Defines specific components for game logic in the ECS architecture.

Classes:
    VelocityComponent: Stores the velocity of an entity in pixels per second.
    PaddleComponent: Marks an entity as a player-controlled paddle.
    BallComponent: Marks an entity as the ball.
    ScoreComponent: Stores the score for a player.
    AIControlledComponent: Marks an entity as AI-controlled.
"""
class VelocityComponent:
    """
    Stores the velocity of an entity in pixels per second.

    Attributes:
        vx (float): Velocity in the x direction.
        vy (float): Velocity in the y direction.
    """
    def __init__(self, vx, vy):
        self.vx = vx
        self.vy = vy

class PaddleComponent:
    """
    Marks an entity as a paddle controlled by a player.

    Attributes:
        player_number (int): The player number (1 or 2).
    """
    def __init__(self, player_number):
        self.player_number = player_number # 1 o 2

class BallComponent:
    """
    Marks an entity as the ball.
    """
    pass

class ScoreComponent:
    """
    Stores the score for a player.

    Attributes:
        player_number (int): The player number.
        score (int): The current score.
    """
    def __init__(self, player_number):
        self.player_number = player_number
        self.score = 0

class AIControlledComponent:
    """
    Marks an entity as controlled by AI.
    """
    pass

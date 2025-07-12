"""
powerup_systems.py
------------------
Implements ECS systems for powerup logic, including spawning, collision detection,
and applying/removing powerup effects.

Classes:
    PowerupSpawningSystem: Handles spawning powerup items on the field.
    PowerupCollisionSystem: Detects when the ball collects a powerup.
    PowerupEffectSystem: Applies and removes active powerup effects.
"""

import pygame
import random
from components.menu_components import PositionComponent, DimensionsComponent
from components.game_components import BallComponent
from components.powerup_components import PowerupComponent, ActivePowerupComponent

class PowerupSpawningSystem:
    """
    Handles spawning powerup items on the field at intervals.

    Attributes:
        world: Reference to the ECS world.
        sw (int): Screen width.
        sh (int): Screen height.
        last_spawn_time (int): Last time a powerup was spawned.
        spawn_interval (int): Interval between spawns in milliseconds.

    Methods:
        process(): Spawns a powerup if none exist and interval has passed.
    """
    def __init__(self, world, screen_width, screen_height):
        self.world = world
        self.sw, self.sh = screen_width, screen_height
        self.last_spawn_time = pygame.time.get_ticks()
        self.spawn_interval = 10000 # 10 segundos

    def process(self):
        current_time = pygame.time.get_ticks()
        if any(self.world.get_entities_with_components(PowerupComponent)):
            return
            
        if current_time > self.last_spawn_time + self.spawn_interval:
            self.last_spawn_time = current_time
            entity_id = self.world.create_entity()
            x = random.randint(int(self.sw * 0.25), int(self.sw * 0.75))
            y = random.randint(int(self.sh * 0.2), int(self.sh * 0.8))
            self.world.add_component(entity_id, PositionComponent(x, y))
            self.world.add_component(entity_id, DimensionsComponent(30, 30))
            self.world.add_component(entity_id, PowerupComponent('BIG_PADDLE'))

class PowerupCollisionSystem:
    """
    Detects when the ball collects a powerup and applies it to the last paddle hit.

    Attributes:
        world: Reference to the ECS world.
        last_paddle_hit: Entity ID of the last paddle that hit the ball.

    Methods:
        process(): Checks for collisions between the ball and powerups.
    """
    def __init__(self, world):
        self.world = world
        self.last_paddle_hit = None

    def process(self):
        # CORRECCIÓN: Usamos next(iter(...), None) para obtener la pelota de forma segura.
        ball_entities = self.world.get_entities_with_components(BallComponent)
        ball_entity = next(iter(ball_entities), None)
        if not ball_entity: return
        
        b_pos = self.world.get_component(ball_entity, PositionComponent)
        b_dim = self.world.get_component(ball_entity, DimensionsComponent)
        if not all([b_pos, b_dim]): return
        ball_rect = pygame.Rect(b_pos.x, b_pos.y, b_dim.width, b_dim.height)

        for powerup_id in list(self.world.get_entities_with_components(PowerupComponent)):
            p_pos = self.world.get_component(powerup_id, PositionComponent)
            p_dim = self.world.get_component(powerup_id, DimensionsComponent)
            if not all([p_pos, p_dim]): continue
            powerup_rect = pygame.Rect(p_pos.x, p_pos.y, p_dim.width, p_dim.height)

            if ball_rect.colliderect(powerup_rect):
                powerup_data = self.world.get_component(powerup_id, PowerupComponent)
                if self.last_paddle_hit:
                    self.world.add_component(self.last_paddle_hit, ActivePowerupComponent(powerup_data.type, 5000))
                self.world.remove_entity(powerup_id)

class PowerupEffectSystem:
    """
    Applies and removes the effects of active powerups.

    Attributes:
        world: Reference to the ECS world.

    Methods:
        process(): Applies effects when activated and removes them when expired.
        apply_effect(entity, powerup_type, activate): Applies or removes the effect.
    """
    def __init__(self, world):
        self.world = world

    def process(self):
        current_time = pygame.time.get_ticks()
        for entity in list(self.world.get_entities_with_components(ActivePowerupComponent)):
            powerup = self.world.get_component(entity, ActivePowerupComponent)
            if not powerup: continue
            
            if not powerup.is_applied:
                self.apply_effect(entity, powerup.type, True)
                powerup.is_applied = True

            if current_time > powerup.activation_time + powerup.duration:
                self.apply_effect(entity, powerup.type, False)
                self.world.remove_component(entity, ActivePowerupComponent)

    def apply_effect(self, entity, powerup_type, activate):
        """
        Applies or removes the effect of a powerup.

        Args:
            entity: Entity ID to apply the effect to.
            powerup_type (str): Type of powerup.
            activate (bool): True to apply, False to remove.
        """
        if powerup_type == 'BIG_PADDLE':
            dim = self.world.get_component(entity, DimensionsComponent)
            if dim:
                dim.height = 150 if activate else 100

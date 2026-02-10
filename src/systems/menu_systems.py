"""
menu_systems.py
---------------
Implements ECS systems for menu logic, including input handling and rendering.

Classes:
    MenuInputSystem: Handles mouse input for menu button interactions.
    MenuRenderSystem: Renders menu buttons and their text.
"""

import pygame
from utils.game_state import GameState
from components.menu_components import (
    PositionComponent, DimensionsComponent, RenderComponent, TextComponent, ButtonComponent
)

class MenuInputSystem:
    """
    Handles mouse input for menu button interactions.

    Attributes:
        world: Reference to the ECS world.
        game_state_manager: Reference to the GameStateManager.
        mouse_pressed (bool): Tracks mouse button state.

    Methods:
        process(events): Updates button states based on mouse position and clicks.
    """
    def __init__(self, world, game_state_manager):
        self.world = world
        self.game_state_manager = game_state_manager
        self.mouse_pressed = False

    def process(self, events):
        """
        Updates button states based on mouse position and clicks.

        Args:
            events (list): List of Pygame events.
        """
        if self.game_state_manager.state != GameState.MENU_PRINCIPAL: return
        mx, my = pygame.mouse.get_pos()
        for e in self.world.get_entities_with_components(PositionComponent, DimensionsComponent, ButtonComponent):
            pos, dim, btn = (self.world.get_component(e, c) for c in (PositionComponent, DimensionsComponent, ButtonComponent))
            if pos.x <= mx <= pos.x + dim.width and pos.y <= my <= pos.y + dim.height:
                btn.state = 'hover' if not self.mouse_pressed else 'clicked'
            else:
                btn.state = 'normal'
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: self.mouse_pressed = True
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                self.mouse_pressed = False
                for e in self.world.get_entities_with_components(ButtonComponent):
                    btn = self.world.get_component(e, ButtonComponent)
                    if btn.state == 'clicked': self.game_state_manager.set_state(btn.action); return

class MenuRenderSystem:
    """
    Renders menu buttons and their text.

    Attributes:
        world: Reference to the ECS world.
        screen: Pygame surface to draw on.
        game_state_manager: Reference to the GameStateManager.

    Methods:
        process(): Draws menu buttons and their text based on button state.
    """
    def __init__(self, world, screen, game_state_manager):
        self.world = world
        self.screen = screen
        self.game_state_manager = game_state_manager

    def process(self):
        """
        Draws menu buttons and their text based on button state.
        """
        if self.game_state_manager.state != GameState.MENU_PRINCIPAL: return
        for e in self.world.get_entities_with_components(PositionComponent, DimensionsComponent, RenderComponent, TextComponent, ButtonComponent):
            pos, dim, render, txt, btn = (self.world.get_component(e, c) for c in (PositionComponent, DimensionsComponent, RenderComponent, TextComponent, ButtonComponent))
            if not all([pos, dim, render, txt, btn]): continue
            color = render.color_normal
            if btn.state == 'hover': color = render.color_hover
            elif btn.state == 'clicked': color = render.color_clicked
            rect = pygame.Rect(pos.x, pos.y, dim.width, dim.height)
            pygame.draw.rect(self.screen, color, rect, border_radius=12)
            surf = txt.font.render(txt.text, True, txt.color)
            text_rect = surf.get_rect(center=rect.center)
            if btn.state == 'clicked': text_rect.y += 2
            self.screen.blit(surf, text_rect)

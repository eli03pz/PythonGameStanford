"""
menu_components.py
------------------
Defines data components used by menu entities in the ECS architecture.

Classes:
    PositionComponent: Stores the position (x, y) of an entity.
    DimensionsComponent: Stores the width and height of an entity.
    RenderComponent: Stores color states for rendering (normal, hover, clicked).
    TextComponent: Stores text, font size, color, and font object for rendering text.
    ButtonComponent: Stores the action associated with a button and its current state.
"""

import pygame
from utils.game_state import GameState

class PositionComponent:
    """
    Stores the position of an entity.

    Attributes:
        x (int): X coordinate.
        y (int): Y coordinate.
    """
    def __init__(self, x, y):
        self.x, self.y = x, y

class DimensionsComponent:
    """
    Stores the dimensions of an entity.

    Attributes:
        width (int): Width of the entity.
        height (int): Height of the entity.
    """
    def __init__(self, width, height):
        self.width, self.height = width, height

class RenderComponent:
    """
    Stores color states for rendering a menu entity.

    Attributes:
        color_normal (tuple): RGB color when in normal state.
        color_hover (tuple): RGB color when hovered.
        color_clicked (tuple): RGB color when clicked.
    """
    def __init__(self, color_normal, color_hover, color_clicked):
        self.color_normal = color_normal
        self.color_hover = color_hover
        self.color_clicked = color_clicked

class TextComponent:
    """
    Stores text and font information for rendering.

    Attributes:
        text (str): The text to display.
        font_size (int): Font size.
        color (tuple): RGB color of the text.
        font (pygame.font.Font): Font object for rendering.
    """
    def __init__(self, text, font_size, color):
        self.text = text
        self.font_size = font_size
        self.color = color
        self.font = pygame.font.Font(None, self.font_size)

class ButtonComponent:
    """
    Stores the action and state of a menu button.

    Attributes:
        action (GameState): The action/state to trigger when the button is pressed.
        state (str): Current button state ('normal', 'hover', 'clicked').
    """
    def __init__(self, action: GameState):
        self.action = action
        self.state = 'normal'  # 'normal', 'hover', 'clicked'

# ARCHIVO: components/menu_components.py
# RESPONSABILIDAD: Definir los bloques de datos (Componentes)
# que utilizan las entidades del menú.

import pygame
from utils.game_state import GameState

class PositionComponent:
    def __init__(self, x, y):
        self.x, self.y = x, y

class DimensionsComponent:
    def __init__(self, width, height):
        self.width, self.height = width, height

class RenderComponent:
    def __init__(self, color_normal, color_hover, color_clicked):
        self.color_normal = color_normal
        self.color_hover = color_hover
        self.color_clicked = color_clicked

class TextComponent:
    def __init__(self, text, font_size, color):
        self.text = text
        self.font_size = font_size
        self.color = color
        self.font = pygame.font.Font(None, self.font_size)

class ButtonComponent:
    def __init__(self, action: GameState):
        self.action = action
        self.state = 'normal'  # 'normal', 'hover', 'clicked'

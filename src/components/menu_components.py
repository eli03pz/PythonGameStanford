from utils.game_state import GameState

class PositionComponent:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class DimensionsComponent:
    def __init__(self, width, height):
        self.width = width
        self.height = height

class RenderComponent:
    def __init__(self, image_path=None, color=None):
        """
        Componente para renderizar una imagen o un color de fondo.
        image_path: Ruta al archivo de imagen (para Pixel Art).
        color: Tupla RGB para un color sólido (ej. (255, 0, 0) para rojo).
        """
        self.image_path = image_path
        self.color = color

class TextComponent:
    def __init__(self, text, font_size, color, font_path=None):
        """
        Componente para renderizar texto.
        text: La cadena de texto a mostrar.
        font_size: Tamaño de la fuente.
        color: Tupla RGB del color del texto.
        font_path: Ruta al archivo de fuente (ej. .ttf)
        """
        self.text = text
        self.font_size = font_size
        self.color = color
        self.font_path = font_path

class ButtonComponent:
    def __init__(self, action: GameState):
        """
        Componente que marca una entidad como un botón.
        action: El GameState al que se cambiará cuando se haga clic en este botón.
        """
        self.action = action

class ClickableComponent:
    def __init__(self):
        """
        Componente que indica que una entidad puede ser clicada.
        Los sistemas de entrada interactuarán con entidades que tengan este componente.
        """
        pass
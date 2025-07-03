from enum import Enum, auto

class GameState(Enum):
    """
    Defines the different states the game can be in.
    Using Enum ensures type safety and readability.
    """
    # Using auto() is a clean way to assign unique values automatically
    MENU_PRINCIPAL = auto()
    JUGANDO_SINGLE_PLAYER = auto()
    JUGANDO_TWO_PLAYERS = auto()
    OPCIONES = auto()
    PAUSA = auto()
    SALIR = auto()
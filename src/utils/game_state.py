from enum import Enum

class GameState(Enum):
    """
    Enum representing the different states of the game.
    """
    MENU_PRINCIPAL = 1
    JUGANDO_SINGLE_PLAYER = 2
    JUGANDO_TWO_PLAYERS = 3
    PAUSA = 4
    GAME_OVER = 5
    SALIR = 6
    
 
# No es necesario importar GameState aquí si solo usas type hints,
# pero es buena práctica hacerlo para claridad.
from utils.game_state import GameState

class GameStateManager:
    """
    Manages the current state of the game.
    Acts as a single source of truth for the game's state.
    """
    def __init__(self, initial_state: GameState = GameState.MENU_PRINCIPAL):
        """
        Initializes the manager with a starting state.
        """
        self.state = initial_state
        print(f"Game State Initialized to: {self.state.name}")

    def set_state(self, new_state: GameState):
        """
        Changes the current game state to a new one.
        This is the only method that should be used to change the state
        to ensure transitions are handled correctly.
        """
        if self.state != new_state:
            print(f"Changing state from <{self.state.name}> to <{new_state.name}>")
            self.state = new_state

    def get_state(self) -> GameState:
        """
        Returns the current state.
        """
        return self.state
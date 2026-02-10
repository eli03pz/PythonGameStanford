"""
game_state_manager.py
---------------------
Manages the current and previous game states.

Classes:
    GameStateManager: Handles transitions between game states and keeps track of the previous state.
"""

from utils.game_state import GameState

class GameStateManager:
    """
    Manages the current and previous state of the game.

    Attributes:
        state (GameState): The current game state.
        previous_state (GameState): The previous game state.

    Methods:
        set_state(new_state: GameState):
            Updates the current state and stores the previous state.
    """
    def __init__(self, initial_state=GameState.MENU_PRINCIPAL):
        self.state = initial_state
        # El estado previo es clave para saber de dónde venimos
        self.previous_state = None

    def set_state(self, new_state: GameState):
        """
        Updates the current state and stores the previous state.

        Args:
            new_state (GameState): The new state to set.
        """
        if self.state != new_state:
            self.previous_state = self.state
            self.state = new_state

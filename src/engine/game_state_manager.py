
from utils.game_state import GameState

class GameStateManager:
    """Gestiona el estado actual y previo del juego."""
    def __init__(self, initial_state=GameState.MENU_PRINCIPAL):
        self.state = initial_state
        # El estado previo es clave para saber de dónde venimos
        self.previous_state = None

    def set_state(self, new_state: GameState):
        """Actualiza el estado, guardando el actual como el previo."""
        if self.state != new_state:
            self.previous_state = self.state
            self.state = new_state

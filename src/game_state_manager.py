from utils.game_state import GameState

class GameStateManager:
    def __init__(self):
        self._current_state = GameState.MENU_PRINCIPAL
        self._previous_state = None

    @property
    def state(self) -> GameState:
        return self._current_state

    def set_state(self, new_state: GameState):
        if self._current_state != new_state:
            self._previous_state = self._current_state
            self._current_state = new_state
            print(f"Estado del juego cambiado de {self._previous_state.name} a {self._current_state.name}")

    def revert_to_previous_state(self):
        if self._previous_state:
            self.set_state(self._previous_state)
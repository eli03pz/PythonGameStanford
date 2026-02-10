"""
config_manager.py
-----------------
Manages game configuration settings, starting with player controls.

Classes:
    ConfigManager: Stores and manages all game configuration options, currently focused on player controls.
"""

import pygame

class ConfigManager:
    """
    Stores and manages all game configuration options.
    Currently, it handles player control key bindings.

    Attributes:
        controls (dict): Dictionary containing key bindings for player actions.

    Methods:
        get_p1_key(action: str) -> int:
            Returns the key binding for a given action of Player 1.

        get_p2_key(action: str) -> int:
            Returns the key binding for a given action of Player 2.

        set_key(player: str, action: str, new_key: int):
            Updates the key binding for a specific player and action.
    """
    def __init__(self):
        # Valores por defecto de las teclas
        self.controls = {
            'player1': {
                'up': pygame.K_w,
                'down': pygame.K_s
            },
            'player2': {
                'up': pygame.K_UP,
                'down': pygame.K_DOWN
            }
        }
        print("ConfigManager inicializado con controles por defecto.")

    def get_p1_key(self, action: str) -> int:
        """Returns the key binding for a given action of Player 1."""
        return self.controls['player1'].get(action)

    def get_p2_key(self, action: str) -> int:
        """Returns the key binding for a given action of Player 2."""
        return self.controls['player2'].get(action)

    def set_key(self, player: str, action: str, new_key: int):
        """
        Updates the key binding for a specific player and action.

        Args:
            player (str): The player identifier ('player1' or 'player2').
            action (str): The action to update ('up' or 'down').
            new_key (int): The new pygame key constant.

        Example:
            set_key('player1', 'up', pygame.K_z)
        """
        if player in self.controls and action in self.controls[player]:
            self.controls[player][action] = new_key
            print(f"Tecla para {player} '{action}' cambiada a {pygame.key.name(new_key)}")

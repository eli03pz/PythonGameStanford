# ARCHIVO: config/config_manager.py
# RESPONSABILIDAD: Gestionar la configuración del juego, empezando por las teclas.

import pygame

class ConfigManager:
    """
    Guarda y gestiona todas las configuraciones del juego.
    Por ahora, solo maneja los controles de los jugadores.
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
        """Devuelve la tecla para una acción del Jugador 1."""
        return self.controls['player1'].get(action)

    def get_p2_key(self, action: str) -> int:
        """Devuelve la tecla para una acción del Jugador 2."""
        return self.controls['player2'].get(action)

    def set_key(self, player: str, action: str, new_key: int):
        """
        Permite cambiar una tecla de control en el futuro.
        Ejemplo: set_key('player1', 'up', pygame.K_z)
        """
        if player in self.controls and action in self.controls[player]:
            self.controls[player][action] = new_key
            print(f"Tecla para {player} '{action}' cambiada a {pygame.key.name(new_key)}")

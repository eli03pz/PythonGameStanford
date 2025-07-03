
# ======================================================================
# ARCHIVO: scenes/base_scene.py (NUEVO Y RECOMENDADO)
# RESPONSABILIDAD: Definir la "interfaz" que todas las escenas deben seguir.
# ======================================================================
class BaseScene:
    def __init__(self, game):
        self.game = game # Proporciona acceso a screen, world, game_state_manager, etc.
    
    def setup(self):
        """Se llama una vez cuando la escena se vuelve activa. Crear entidades y sistemas aquí."""
        pass
    
    def cleanup(self):
        """Se llama una vez cuando la escena se desactiva. Limpiar entidades aquí."""
        pass

    def handle_events(self, events):
        """Maneja la lista de eventos de Pygame en cada fotograma."""
        pass

    def update(self, dt):
        """Actualiza la lógica de la escena en cada fotograma."""
        pass

    def draw(self, screen):
        """Dibuja la escena en la pantalla."""
        pass

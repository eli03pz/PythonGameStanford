# ARCHIVO: components/game_components.py
# RESPONSABILIDAD: Definir los componentes específicos de la lógica de juego.

class VelocityComponent:
    """Guarda la velocidad de una entidad en píxeles por segundo."""
    def __init__(self, vx, vy):
        self.vx = vx
        self.vy = vy

class PaddleComponent:
    """Marca una entidad como una pala controlada por un jugador."""
    def __init__(self, player_number):
        self.player_number = player_number # 1 o 2

class BallComponent:
    """Marca una entidad como la pelota."""
    pass

class ScoreComponent:
    """Guarda la puntuación para un jugador."""
    def __init__(self, player_number):
        self.player_number = player_number
        self.score = 0

class AIControlledComponent:
    """Marca una entidad como controlada por la IA."""
    pass

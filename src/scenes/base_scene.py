"""
base_scene.py
-------------
Defines the BaseScene class, which acts as an interface for all game scenes.
All scenes should inherit from this class and implement its methods.

Classes:
    BaseScene: Abstract base class for game scenes, providing a standard interface.
"""
class BaseScene:
    """
    Abstract base class for all game scenes.

    Attributes:
        game: Reference to the main game object, providing access to screen, world, game_state_manager, etc.

    Methods:
        setup():
            Called once when the scene becomes active. Create entities and systems here.

        cleanup():
            Called once when the scene is deactivated. Clean up entities here.

        handle_events(events):
            Handles the list of Pygame events each frame.

        update(dt):
            Updates the scene logic each frame.

        draw(screen):
            Draws the scene to the screen.
    """
    def __init__(self, game):
        self.game = game # Proporciona acceso a screen, world, game_state_manager, etc.
    
    def setup(self):
        """Called once when the scene becomes active. Create entities and systems here."""
        pass
    
    def cleanup(self):
        """Called once when the scene is deactivated. Clean up entities here."""
        pass

    def handle_events(self, events):
        """Handles the list of Pygame events each frame."""
        pass

    def update(self, dt):
        """Updates the scene logic each frame."""
        pass

    def draw(self, screen):
        """Draws the scene to the screen."""
        pass


import pygame

def load_image(file_path):
    """Load an image from the specified file path."""
    try:
        image = pygame.image.load(file_path)
        return image
    except pygame.error as e:
        print(f"Error loading image: {e}")
        return None

def check_collision(rect1, rect2):
    """Check if two rectangles collide."""
    return rect1.colliderect(rect2)

def reset_game_settings():
    """Reset game settings to default values."""
    settings = {
        'screen_width': 800,
        'screen_height': 600,
        'fps': 60,
        'player_health': 100,
        'enemy_health': 50,
        'powerup_duration': 10
    }
    return settings

def draw_text(surface, text, position, font, color=(255, 255, 255)):
    """Draw text on the given surface at the specified position."""
    text_surface = font.render(text, True, color)
    surface.blit(text_surface, position)
"""
utils.py
--------
Contains global constants, helper functions, and utility code for the game.

Constants:
    SCREEN_WIDTH (int): Width of the game window.
    SCREEN_HEIGHT (int): Height of the game window.
    WINNING_SCORE (int): Score required to win the game.

    COLOR_BACKGROUND (tuple): RGB color for the background.
    COLOR_WHITE (tuple): RGB color for white elements.
    COLOR_GRAY (tuple): RGB color for gray elements.

    COLOR_BUTTON_NORMAL (tuple): RGB color for normal menu buttons.
    COLOR_BUTTON_HOVER (tuple): RGB color for hovered menu buttons.
    COLOR_BUTTON_CLICKED (tuple): RGB color for clicked menu buttons.

    COLOR_PADDLE (tuple): RGB color for paddles.
    COLOR_BALL (tuple): RGB color for the ball.
    COLOR_HIT_FLASH (tuple): RGB color for hit flash effect.
    COLOR_POWERUP (tuple): RGB color for powerup items.

    CONFETTI_COLORS (list): List of RGB colors for confetti particles.

Functions:
    clamp(value, min_val, max_val): Clamps a value between a minimum and maximum.
"""


# --- Dimension and Game Constants ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WINNING_SCORE = 5

# --- Color Constants ---
COLOR_BACKGROUND = (21, 33, 44)
COLOR_WHITE = (236, 240, 241)
COLOR_GRAY = (120, 120, 120)

# Menu button colors
COLOR_BUTTON_NORMAL = (41, 128, 185)
COLOR_BUTTON_HOVER = (52, 152, 219)
COLOR_BUTTON_CLICKED = (35, 110, 155)

# Game element colors
COLOR_PADDLE = COLOR_WHITE
COLOR_BALL = COLOR_WHITE
COLOR_HIT_FLASH = (255, 255, 0) # Yellow
COLOR_POWERUP = (0, 255, 255)   # Cyan

# Confetti colors for celebration
CONFETTI_COLORS = [
    (255, 192, 203), # Pink
    (173, 216, 230), # Light blue
    (255, 255, 0),   # Yellow
    (144, 238, 144)  # Light green
]

# --- Helper Functions ---

def clamp(value, min_val, max_val):
    """
    Ensures a value stays within a minimum and maximum range.
    Useful for keeping paddles within screen bounds.

    Example usage in MovementSystem:
        pos.y = clamp(pos.y, 0, SCREEN_HEIGHT - paddle_height)

    Args:
        value (float): The value to clamp.
        min_val (float): Minimum allowed value.
        max_val (float): Maximum allowed value.

    Returns:
        float: The clamped value.
    """
    return max(min_val, min(value, max_val))

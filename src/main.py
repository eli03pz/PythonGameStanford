# ======================================================================
# main.py
# ----------------------------------------------------------------------
# Main entry point for the game. Initializes and runs the Game class.
#
# Responsibility:
#   - Acts as the entry point for the application.
#   - Imports the Game class and executes the main game loop.
# ======================================================================

from scenes.game import Game

def main():
    """
    Main function that initializes and runs the game.

    Handles unexpected exceptions and prints error messages.
    """
    try:
        juego = Game()
        juego.run()
    except Exception as e:
        print(f"ERROR: An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
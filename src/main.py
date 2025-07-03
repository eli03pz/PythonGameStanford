# ======================================================================
# File: main.py
# Description: Main entry point for the game, initializes and runs the game.
# RESPONSABILIDAD: Ser el punto de entrada de la aplicación.
#                  Importa la clase Game y la ejecuta.
# ======================================================================

from scenes.game import Game

def main():
    """
    Función principal que inicializa y corre el juego.
    """
    try:
        juego = Game()
        juego.run()
    except Exception as e:
        print(f"ERROR: Ocurrió un error inesperado: {e}")

if __name__ == "__main__":
    main()

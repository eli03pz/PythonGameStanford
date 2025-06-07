
import pygame
from scenes.game import Game

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Arcade Shooter Game")
    
    game = Game(screen)
    # show_menu(screen)
    game.run()

    pygame.quit()

if __name__ == "__main__":
    main()
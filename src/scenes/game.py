"""
game.py
-------
Main game class that initializes and manages the game loop, scenes, and global systems.

Classes:
    Game: Handles initialization, scene management, and the main game loop.
"""

import pygame
import sys
from utils.game_state import GameState
from engine.game_state_manager import GameStateManager
from engine.ecs_world import ECSWorld
from config.config_manager import ConfigManager
from scenes.menu.main_menu_scene import MainMenuScene
from scenes.game_scene import GameScene
from scenes.options_escene import OptionsScene
from scenes.pause_scene import PauseScene
from utils.utils import SCREEN_WIDTH, SCREEN_HEIGHT, COLOR_BACKGROUND

class Game:
    """
    Main game class responsible for initializing Pygame, managing scenes,
    and running the main game loop.

    Attributes:
        screen_width (int): Width of the game window.
        screen_height (int): Height of the game window.
        screen (pygame.Surface): The main display surface.
        clock (pygame.time.Clock): Controls the frame rate.
        running (bool): Indicates if the game loop is running.
        world (ECSWorld): The ECS world instance.
        game_state_manager (GameStateManager): Manages current and previous game states.
        config_manager (ConfigManager): Handles game configuration and controls.
        current_scene: The currently active scene.
        previous_game_state: Stores the previous game state for pause transitions.
        scenes (dict): Maps game states to scene instances.

    Methods:
        run():
            Main game loop. Handles scene transitions, events, updates, and rendering.
    """
    def __init__(self):
        pygame.init()
        # Usamos las constantes de utils.py
        self.screen_width = SCREEN_WIDTH
        self.screen_height = SCREEN_HEIGHT
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Mi Juego Modular")
        self.clock = pygame.time.Clock()
        self.running = True

        self.world = ECSWorld()
        self.game_state_manager = GameStateManager()
        self.config_manager = ConfigManager()
        
        self.current_scene = None
        self.previous_game_state = None

        self.scenes = {
            GameState.MENU_PRINCIPAL: MainMenuScene(self),
            GameState.JUGANDO_SINGLE_PLAYER: GameScene(self, num_players=1, mode='classic'),
            GameState.JUGANDO_TWO_PLAYERS: GameScene(self, num_players=2, mode='classic'),
            GameState.JUGANDO_SHRINK_MODE: GameScene(self, num_players=1, mode='shrink'),
            GameState.OPCIONES: OptionsScene(self),
            GameState.PAUSA: PauseScene(self)
        }
        
        self.current_scene = self.scenes[self.game_state_manager.state]
        self.current_scene.setup()

    def run(self):
        """
        Main game loop. Handles scene transitions, events, updates, and rendering.
        """
        while self.running:
            current_state = self.game_state_manager.state
            previous_state = self.game_state_manager.previous_state

            if current_state != previous_state:
                if current_state == GameState.PAUSA:
                    self.previous_game_state = previous_state
                    self.current_scene = self.scenes[GameState.PAUSA]
                    self.current_scene.setup()
                elif previous_state == GameState.PAUSA:
                    self.scenes[GameState.PAUSA].cleanup()
                    if current_state == GameState.MENU_PRINCIPAL:
                        self.scenes[self.previous_game_state].cleanup()
                        self.current_scene = self.scenes[GameState.MENU_PRINCIPAL]
                        self.current_scene.setup()
                    else:
                        self.current_scene = self.scenes[current_state]
                else:
                    if previous_state is not None: self.scenes[previous_state].cleanup()
                    self.current_scene = self.scenes[current_state]
                    self.current_scene.setup()
            
            self.game_state_manager.previous_state = current_state
            if current_state == GameState.SALIR: self.running = False; continue
            
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT: self.running = False

            dt = self.clock.tick(60) / 1000.0
            self.screen.fill(COLOR_BACKGROUND)

            if current_state == GameState.PAUSA:
                self.scenes[self.previous_game_state].draw(self.screen)
                self.current_scene.handle_events(events)
                self.current_scene.draw(self.screen)
            elif self.current_scene:
                self.current_scene.handle_events(events)
                self.current_scene.update(dt)
                self.current_scene.draw(self.screen)

            pygame.display.flip()
        pygame.quit(); sys.exit()

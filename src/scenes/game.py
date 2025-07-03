# ARCHIVO: game.py
# RESPONSABILIDAD: Definir la clase principal del juego que contiene
# el bucle principal y gestiona las escenas.

import pygame
import sys

from config.config_manager import ConfigManager
from utils.game_state import GameState
from engine.game_state_manager import GameStateManager
from engine.ecs_world import ECSWorld
from scenes.menu.main_menu_scene import MainMenuScene
from scenes.game_scene import GameScene
from scenes.options_escene import OptionsScene

class Game:
    def __init__(self):
        pygame.init()
        self.screen_width = 800
        self.screen_height = 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Ping Pong")
        self.clock = pygame.time.Clock()
        self.running = True

        self.world = ECSWorld()
        self.game_state_manager = GameStateManager()
        self.config_manager = ConfigManager()
        
        self.previous_state = None

        self.scenes = {
            GameState.MENU_PRINCIPAL: MainMenuScene(self),
            GameState.JUGANDO_SINGLE_PLAYER: GameScene(self, num_players=1),
            GameState.JUGANDO_TWO_PLAYERS: GameScene(self, num_players=2),
            GameState.OPCIONES: OptionsScene(self),
            # GameState.PAUSA: PauseScene(self),
            GameState.SALIR: None  # No hay escena para salir, se maneja
        }
        self.current_scene = None
        self._change_scene(GameState.MENU_PRINCIPAL)

    def _change_scene(self, new_state: GameState):
        if self.current_scene:
            self.current_scene.cleanup()
        self.current_scene = self.scenes.get(new_state)
        
        if new_state == GameState.PAUSA:
            self.previous_state = self.game_state_manager.state
        if self.game_state_manager.state == GameState.PAUSA and (new_state == GameState.JUGANDO_SINGLE_PLAYER or new_state == GameState.JUGANDO_TWO_PLAYERS):
            self.scenes[GameState.PAUSA].cleanup() # Limpiar los botones de pausa
        else:
            self.current_scene = self.scenes.get(new_state)
            if self.current_scene: self.current_scene.setup()
            else: self.running = False

        if self.current_scene:
            self.current_scene.setup()
        else:
            print(f"ADVERTENCIA: No se encontró escena para el estado {new_state.name}")
            self.running = False
    def run(self):
        previous_state = self.game_state_manager.state
        while self.running:
            current_state = self.game_state_manager.state
            if current_state != previous_state:
                self._change_scene(current_state)
                previous_state = current_state

            if current_state == GameState.SALIR: self.running = False; continue
            
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT: self.running = False

            dt = self.clock.tick(60) / 1000.0
            
            # --- MODIFICACIÓN CLAVE DEL BUCLE PRINCIPAL ---
            self.screen.fill((21, 33, 44))

            if current_state == GameState.PAUSA:
                # Si estamos en pausa, dibujamos la escena de juego DEBAJO...
                if self.previous_game_state in self.scenes:
                    game_scene = self.scenes[self.previous_game_state]
                    game_scene.draw(self.screen)
                # ...y luego la escena de pausa ENCIMA. NO actualizamos la lógica del juego.
                self.current_scene.handle_events(events)
                self.current_scene.draw(self.screen)
            elif self.current_scene:
                # Comportamiento normal para todas las demás escenas
                self.current_scene.handle_events(events)
                self.current_scene.update(dt)
                self.current_scene.draw(self.screen)

        pygame.quit()
        sys.exit()

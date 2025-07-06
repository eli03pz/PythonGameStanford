# ARCHIVO: game.py

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

class Game:
    def __init__(self):
        pygame.init()
        self.screen_width, self.screen_height = 800, 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Mi Juego Modular")
        self.clock = pygame.time.Clock()
        self.running = True

        self.world = ECSWorld()
        self.game_state_manager = GameStateManager()
        self.config_manager = ConfigManager()
        
        self.current_scene = None
        # CORRECCIÓN: Renombrado y inicializado correctamente
        self.previous_game_state = None

        self.scenes = {
            GameState.MENU_PRINCIPAL: MainMenuScene(self),
            GameState.JUGANDO_SINGLE_PLAYER: GameScene(self, num_players=1),
            GameState.JUGANDO_TWO_PLAYERS: GameScene(self, num_players=2),
            GameState.OPCIONES: OptionsScene(self),
            GameState.PAUSA: PauseScene(self)
        }
        # Iniciar la primera escena
        self.current_scene = self.scenes[self.game_state_manager.state]
        self.current_scene.setup()

    def run(self):
        while self.running:
            current_state = self.game_state_manager.state
            previous_state = self.game_state_manager.previous_state

            # --- Lógica de Transición de Escena ---
            if current_state != previous_state:
                # Caso 1: Estamos pausando el juego
                if current_state == GameState.PAUSA:
                    # CORRECCIÓN: Usamos el nombre de atributo corregido
                    self.previous_game_state = previous_state
                    self.current_scene = self.scenes[GameState.PAUSA]
                    self.current_scene.setup()
                
                # Caso 2: Estamos saliendo de la pausa
                elif previous_state == GameState.PAUSA:
                    self.scenes[GameState.PAUSA].cleanup() # Siempre limpiar el menú de pausa
                    # Si volvemos al menú principal, debemos limpiar la escena de juego pausada
                    if current_state == GameState.MENU_PRINCIPAL:
                        # CORRECCIÓN: Usamos el nombre de atributo corregido
                        self.scenes[self.previous_game_state].cleanup()
                        self.current_scene = self.scenes[GameState.MENU_PRINCIPAL]
                        self.current_scene.setup()
                    # Si reanudamos, simplemente volvemos a la escena de juego
                    else:
                        self.current_scene = self.scenes[current_state]
                
                # Caso 3: Cualquier otra transición normal
                else:
                    if previous_state is not None:
                        self.scenes[previous_state].cleanup()
                    self.current_scene = self.scenes[current_state]
                    self.current_scene.setup()
            
            # Reseteamos el estado previo en el manager para detectar el siguiente cambio
            self.game_state_manager.previous_state = current_state

            if current_state == GameState.SALIR: self.running = False; continue
            
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT: self.running = False

            dt = self.clock.tick(60) / 1000.0
            self.screen.fill((21, 33, 44))

            # --- Lógica de Actualización y Dibujado ---
            if current_state == GameState.PAUSA:
                # Dibujar la escena de juego DEBAJO (sin actualizarla)
                # CORRECCIÓN: Usamos el nombre de atributo corregido
                self.scenes[self.previous_game_state].draw(self.screen)
                # Manejar y dibujar la escena de pausa ENCIMA
                self.current_scene.handle_events(events)
                self.current_scene.draw(self.screen)
            elif self.current_scene:
                self.current_scene.handle_events(events)
                self.current_scene.update(dt)
                self.current_scene.draw(self.screen)

            pygame.display.flip()
        pygame.quit(); sys.exit()

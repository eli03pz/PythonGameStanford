# ARCHIVO: scenes/options_scene.py

import pygame
import sys
from scenes.base_scene import BaseScene
from utils.game_state import GameState

# --- Componentes específicos para la escena de Opciones ---
# Por simplicidad, los definimos aquí. En un proyecto más grande, podrían ir a components/options_components.py
class PositionComponent:
    def __init__(self, x, y): self.x, self.y = x, y

class DimensionsComponent:
    def __init__(self, w, h): self.width, self.height = w, h

class ButtonComponent:
    def __init__(self, action=None): self.state = 'normal'

class KeyBindingComponent:
    """Guarda la información de qué control representa esta entidad."""
    def __init__(self, player, action):
        self.player = player  # 'player1' o 'player2'
        self.action = action  # 'up' o 'down'
        self.is_listening = False # True si está esperando una nueva tecla

# --- Sistemas específicos para la escena de Opciones ---

class OptionsInputSystem:
    def __init__(self, world, game_state_manager, config_manager):
        self.world = world
        self.gsm = game_state_manager
        self.config = config_manager
        self.listening_entity = None # Entidad que está esperando una tecla

    def process(self, events):
        for event in events:
            # 1. Si estamos esperando una tecla, la capturamos
            if self.listening_entity is not None and event.type == pygame.KEYDOWN:
                binding_comp = self.world.get_component(self.listening_entity, KeyBindingComponent)
                
                # Evitar que se asigne la tecla ESC
                if event.key == pygame.K_ESCAPE:
                    binding_comp.is_listening = False
                    self.listening_entity = None
                    continue

                # Actualizamos la configuración
                self.config.set_key(binding_comp.player, binding_comp.action, event.key)
                
                # Dejamos de escuchar
                binding_comp.is_listening = False
                self.listening_entity = None
                return # Salimos para no procesar más eventos este frame

            # 2. Manejar clics para empezar a escuchar
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = event.pos
                # Si ya estábamos escuchando, lo cancelamos
                if self.listening_entity is not None:
                    self.world.get_component(self.listening_entity, KeyBindingComponent).is_listening = False
                    self.listening_entity = None

                for entity in self.world.get_entities_with_components(PositionComponent, DimensionsComponent, KeyBindingComponent):
                    pos = self.world.get_component(entity, PositionComponent)
                    dim = self.world.get_component(entity, DimensionsComponent)
                    if pos.x <= mx <= pos.x + dim.width and pos.y <= my <= pos.y + dim.height:
                        binding_comp = self.world.get_component(entity, KeyBindingComponent)
                        binding_comp.is_listening = True
                        self.listening_entity = entity
                        return # Solo podemos escuchar una tecla a la vez
            
            # 3. Volver al menú principal con ESCAPE
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                if self.listening_entity is None: # Solo si no estamos esperando una tecla
                    self.gsm.set_state(GameState.MENU_PRINCIPAL)

class OptionsRenderSystem:
    def __init__(self, world, screen, config_manager):
        self.world = world
        self.screen = screen
        self.config = config_manager
        self.font_label = pygame.font.Font(None, 40)
        self.font_key = pygame.font.Font(None, 40)
        self.font_title = pygame.font.Font(None, 74)
        self.font_footer = pygame.font.Font(None, 28)

    def process(self):
        # Dibujar título e instrucciones
        title_surf = self.font_title.render("Opciones de Control", True, "white")
        self.screen.blit(title_surf, title_surf.get_rect(centerx=self.screen.get_width()/2, y=50))
        
        footer_surf = self.font_footer.render("Haz clic en una tecla para cambiarla. Presiona ESC para salir.", True, "gray")
        self.screen.blit(footer_surf, footer_surf.get_rect(centerx=self.screen.get_width()/2, y=self.screen.get_height()-40))

        # Dibujar cada una de las opciones de control
        for entity in self.world.get_entities_with_components(PositionComponent, DimensionsComponent, KeyBindingComponent):
            pos = self.world.get_component(entity, PositionComponent)
            dim = self.world.get_component(entity, DimensionsComponent)
            binding = self.world.get_component(entity, KeyBindingComponent)

            # Dibujar el fondo del botón
            bg_color = (50, 50, 90) if binding.is_listening else (40, 40, 60)
            pygame.draw.rect(self.screen, bg_color, (pos.x, pos.y, dim.width, dim.height), border_radius=8)

            # Dibujar la etiqueta (ej. "Jugador 1 - Arriba")
            label_text = f"Jugador {binding.player[-1]} - {'Arriba' if binding.action == 'up' else 'Abajo'}"
            label_surf = self.font_label.render(label_text, True, (200, 200, 200))
            self.screen.blit(label_surf, (pos.x + 20, pos.y + dim.height/2 - label_surf.get_height()/2))

            # Dibujar la tecla actual
            if binding.is_listening:
                key_text = "???"
            else:
                key_code = self.config.controls[binding.player][binding.action]
                key_text = pygame.key.name(key_code).upper()
            
            key_surf = self.font_key.render(key_text, True, "white")
            key_rect = pygame.Rect(pos.x + dim.width - 120, pos.y, 100, dim.height)
            pygame.draw.rect(self.screen, (20, 20, 40), key_rect, border_radius=8)
            self.screen.blit(key_surf, key_surf.get_rect(center=key_rect.center))

# --- Clase Principal de la Escena de Opciones ---

class OptionsScene(BaseScene):
    def setup(self):
        self.entities = []
        
        # --- 1. Crear sistemas para esta escena ---
        self.input_system = OptionsInputSystem(self.game.world, self.game.game_state_manager, self.game.config_manager)
        self.render_system = OptionsRenderSystem(self.game.world, self.game.screen, self.game.config_manager)

        # --- 2. Crear las entidades para las opciones de control ---
        bindings = [
            ('player1', 'up'), ('player1', 'down'),
            ('player2', 'up'), ('player2', 'down')
        ]
        
        width, height = 500, 60
        start_x = (self.game.screen_width - width) / 2
        start_y = 150
        spacing = 70

        for i, (player, action) in enumerate(bindings):
            entity_id = self.game.world.create_entity()
            self.entities.append(entity_id)
            
            self.game.world.add_component(entity_id, PositionComponent(start_x, start_y + i * spacing))
            self.game.world.add_component(entity_id, DimensionsComponent(width, height))
            self.game.world.add_component(entity_id, KeyBindingComponent(player, action))
            self.game.world.add_component(entity_id, ButtonComponent()) # Para que sea "clicable"

    def cleanup(self):
        for entity_id in self.entities:
            self.game.world.remove_entity(entity_id)
        self.entities.clear()

    def handle_events(self, events):
        self.input_system.process(events)

    def update(self, dt):
        pass

    def draw(self, screen):
        self.render_system.process()

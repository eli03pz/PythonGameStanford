"""
options_escene.py
-----------------
Implements the options scene for configuring player controls.
Includes ECS components and systems for input handling and rendering.

Classes:
    PositionComponent: Stores the position (x, y) of an entity.
    DimensionsComponent: Stores the width and height of an entity.
    ButtonComponent: Represents a button with an action and state.
    KeyBindingComponent: Stores key binding info for a player and action.
    OptionsInputSystem: Handles input events for key rebinding and navigation.
    OptionsRenderSystem: Renders the options menu, key bindings, and buttons.
    OptionsScene: Main scene class for options, manages setup, cleanup, events, and rendering.
"""

import pygame
from scenes.base_scene import BaseScene
from utils.game_state import GameState

# --- Componentes específicos para la escena de Opciones ---
class PositionComponent:
    """
    Stores the position of an entity.

    Attributes:
        x (int): X coordinate.
        y (int): Y coordinate.
    """
    def __init__(self, x, y): self.x, self.y = x, y

class DimensionsComponent:
    """
    Stores the dimensions of an entity.

    Attributes:
        width (int): Width of the entity.
        height (int): Height of the entity.
    """
    def __init__(self, w, h): self.width, self.height = w, h

class ButtonComponent:
    """
    Represents a button with an action and state.

    Attributes:
        state (str): Current button state ('normal', 'hover', etc.).
        action: The action to trigger when clicked (usually a GameState).
    """
    def __init__(self, action=None):
        self.state = 'normal'
        self.action = action

class KeyBindingComponent:
    """
    Stores key binding info for a player and action.

    Attributes:
        player (str): Player identifier ('player1', 'player2').
        action (str): Action name ('up', 'down').
        is_listening (bool): True if waiting for a new key input.
    """
    def __init__(self, player, action):
        self.player = player
        self.action = action
        self.is_listening = False

# --- Sistemas específicos para la escena de Opciones ---

class OptionsInputSystem:
    """
    Handles input events for key rebinding and navigation in the options menu.

    Attributes:
        world: Reference to the ECS world.
        gsm: Reference to the GameStateManager.
        config: Reference to the ConfigManager.
        listening_entity: Entity currently waiting for key input.
    """
    def __init__(self, world, gsm, config_manager):
        self.world = world
        self.gsm = gsm
        self.config = config_manager
        self.listening_entity = None

    def process(self, events):
        """
        Processes input events for key rebinding, button clicks, and ESC navigation.

        Args:
            events (list): List of Pygame events.
        """
        for event in events:
            # 1. Si estamos esperando una tecla, la capturamos
            if self.listening_entity is not None and event.type == pygame.KEYDOWN:
                binding_comp = self.world.get_component(self.listening_entity, KeyBindingComponent)
                if event.key != pygame.K_ESCAPE:
                    self.config.set_key(binding_comp.player, binding_comp.action, event.key)
                binding_comp.is_listening = False
                self.listening_entity = None
                return

            # 2. Manejar clics del ratón
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mx, my = event.pos
                if self.listening_entity is not None:
                    self.world.get_component(self.listening_entity, KeyBindingComponent).is_listening = False
                    self.listening_entity = None

                # Revisar si se hizo clic en un binding de tecla
                for entity in self.world.get_entities_with_components(KeyBindingComponent, PositionComponent, DimensionsComponent):
                    pos = self.world.get_component(entity, PositionComponent)
                    dim = self.world.get_component(entity, DimensionsComponent)
                    if pos.x <= mx <= pos.x + dim.width and pos.y <= my <= pos.y + dim.height:
                        self.world.get_component(entity, KeyBindingComponent).is_listening = True
                        self.listening_entity = entity
                        return

                # Revisar si se hizo clic en el botón de "Volver"
                for entity in self.world.get_entities_with_components(ButtonComponent):
                    if not self.world.get_component(entity, KeyBindingComponent): # Asegurarse de que no es un binding
                        pos = self.world.get_component(entity, PositionComponent)
                        dim = self.world.get_component(entity, DimensionsComponent)
                        if pos.x <= mx <= pos.x + dim.width and pos.y <= my <= pos.y + dim.height:
                            btn = self.world.get_component(entity, ButtonComponent)
                            self.gsm.set_state(btn.action)
                            return
            
            # 3. Volver al menú principal con ESCAPE
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE and self.listening_entity is None:
                self.gsm.set_state(GameState.MENU_PRINCIPAL)

class OptionsRenderSystem:
    """
    Renders the options menu, key bindings, and buttons.

    Attributes:
        world: Reference to the ECS world.
        screen: Pygame surface to draw on.
        config: Reference to the ConfigManager.
        font_label, font_key, font_title, font_footer: Font objects for rendering text.
    """
    def __init__(self, world, screen, config_manager):
        self.world, self.screen, self.config = world, screen, config_manager
        self.font_label = pygame.font.Font(None, 40)
        self.font_key = pygame.font.Font(None, 40)
        self.font_title = pygame.font.Font(None, 74)
        self.font_footer = pygame.font.Font(None, 28)

    def process(self):
        """
        Renders the options menu, key bindings, and the "Back" button.
        """
        # Título e instrucciones
        title_surf = self.font_title.render("Opciones de Control", True, "white")
        self.screen.blit(title_surf, title_surf.get_rect(centerx=self.screen.get_width()/2, y=50))
        footer_surf = self.font_footer.render("Haz clic en una tecla para cambiarla. Presiona ESC para salir.", True, "gray")
        self.screen.blit(footer_surf, footer_surf.get_rect(centerx=self.screen.get_width()/2, y=self.screen.get_height()-40))

        # Dibujar bindings de teclas
        for entity in self.world.get_entities_with_components(KeyBindingComponent, PositionComponent, DimensionsComponent):
            pos, dim, binding = self.world.get_component(entity, PositionComponent), self.world.get_component(entity, DimensionsComponent), self.world.get_component(entity, KeyBindingComponent)
            bg_color = (50, 50, 90) if binding.is_listening else (40, 40, 60)
            pygame.draw.rect(self.screen, bg_color, (pos.x, pos.y, dim.width, dim.height), border_radius=8)
            pygame.draw.rect(self.screen, (100, 100, 120), (pos.x, pos.y, dim.width, dim.height), 1, border_radius=8)
            label_text = f"Jugador {binding.player[-1]} - {'Arriba' if binding.action == 'up' else 'Abajo'}"
            label_surf = self.font_label.render(label_text, True, (200, 200, 200))
            self.screen.blit(label_surf, (pos.x + 20, pos.y + dim.height/2 - label_surf.get_height()/2))
            key_text = "???" if binding.is_listening else pygame.key.name(self.config.controls[binding.player][binding.action]).upper()
            key_surf = self.font_key.render(key_text, True, "white")
            key_rect = pygame.Rect(pos.x + dim.width - 120, pos.y + 5, 100, dim.height - 10)
            pygame.draw.rect(self.screen, (20, 20, 40), key_rect, border_radius=8)
            self.screen.blit(key_surf, key_surf.get_rect(center=key_rect.center))

        # Dibujar botón de Volver
        for entity in self.world.get_entities_with_components(ButtonComponent):
            if self.world.get_component(entity, KeyBindingComponent): continue
            pos, dim, btn = self.world.get_component(entity, PositionComponent), self.world.get_component(entity, DimensionsComponent), self.world.get_component(entity, ButtonComponent)
            mx, my = pygame.mouse.get_pos()
            is_hover = pos.x <= mx <= pos.x + dim.width and pos.y <= my <= pos.y + dim.height
            color = (52, 152, 219) if is_hover else (41, 128, 185)
            pygame.draw.rect(self.screen, color, (pos.x, pos.y, dim.width, dim.height), border_radius=12)
            pygame.draw.rect(self.screen, "white", (pos.x, pos.y, dim.width, dim.height), 2, border_radius=12)
            text_surf = self.font_label.render("Volver al Menú", True, "white")
            self.screen.blit(text_surf, text_surf.get_rect(center=(pos.x + dim.width/2, pos.y + dim.height/2)))

# --- Clase Principal de la Escena ---

class OptionsScene(BaseScene):
    """
    Main scene class for the options menu.

    Methods:
        setup():
            Initializes entities and systems for the options menu.

        cleanup():
            Removes all entities created by this scene.

        handle_events(events):
            Processes input events for the options menu.

        update(dt):
            Updates the scene logic (currently unused).

        draw(screen):
            Renders the options menu.
    """
    def setup(self):
        """
        Initializes entities and systems for the options menu.
        """
        self.entities = []
        self.input_system = OptionsInputSystem(self.game.world, self.game.game_state_manager, self.game.config_manager)
        self.render_system = OptionsRenderSystem(self.game.world, self.game.screen, self.game.config_manager)

        bindings = [('player1', 'up'), ('player1', 'down'), ('player2', 'up'), ('player2', 'down')]
        width, height = 500, 60; start_x = (self.game.screen_width - width) / 2; start_y = 150; spacing = 70
        for i, (player, action) in enumerate(bindings):
            entity_id = self.game.world.create_entity()
            self.entities.append(entity_id)
            self.game.world.add_component(entity_id, PositionComponent(start_x, start_y + i * spacing))
            self.game.world.add_component(entity_id, DimensionsComponent(width, height))
            self.game.world.add_component(entity_id, KeyBindingComponent(player, action))

        back_button_id = self.game.world.create_entity()
        self.entities.append(back_button_id)
        self.game.world.add_component(back_button_id, PositionComponent(start_x, start_y + len(bindings) * spacing + 20))
        self.game.world.add_component(back_button_id, DimensionsComponent(width, height))
        self.game.world.add_component(back_button_id, ButtonComponent(GameState.MENU_PRINCIPAL))

    def cleanup(self):
        """
        Removes all entities created by this scene.
        """
        for entity_id in self.entities: self.game.world.remove_entity(entity_id)
        self.entities.clear()

    def handle_events(self, events): 
        """
        Processes input events for the options menu.

        Args:
            events (list): List of Pygame events.
        """
        self.input_system.process(events)
    def update(self, dt): 
        """
        Updates the scene logic (currently unused).

        Args:
            dt (float): Delta time since last frame.
        """
        pass
    def draw(self, screen): 
        """
        Renders the options menu.

        Args:
            screen: The Pygame surface to draw on.
        """
        self.render_system.process()

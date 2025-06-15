
from components.menu_components import PositionComponent, DimensionsComponent, RenderComponent, TextComponent, ButtonComponent, ClickableComponent
from utils.game_state import GameState
from engine.ecs_world import ECSWorld # Asume que tienes una clase ECSWorld en engine/ecs_world.py

class MainMenuScene:
    def __init__(self, world: ECSWorld, screen, game_state_manager):
        self.world = world
        self.screen = screen
        self.game_state_manager = game_state_manager
        self.entities = [] # Para almacenar las entidades de esta escena y poder limpiarlas.

    def setup(self):
        # Limpia cualquier entidad existente si la escena se recarga
        self.cleanup()

        # Fondo del menú (opcional)
        background_entity = self.world.create_entity()
        self.world.add_component(background_entity, PositionComponent(0, 0))
        self.world.add_component(background_entity, DimensionsComponent(self.screen.get_width(), self.screen.get_height()))
        self.world.add_component(background_entity, RenderComponent(image_path="assets/images/background_menu.png")) # ¡Ruta de tu Pixel Art de fondo!
        self.entities.append(background_entity)

        # Título del juego
        title_entity = self.world.create_entity()
        self.world.add_component(title_entity, PositionComponent(self.screen.get_width() / 2 - 150, 100))
        self.world.add_component(title_entity, TextComponent("MI JUEGO PIXELADO", 48, (255, 255, 255), font_path="assets/fonts/arcadeclassic/ARCADECLASSIC.TTF")) # Fuente Pixel Art
        self.entities.append(title_entity)

        # Botón JUGAR (Single Player)
        play_button_entity = self.world.create_entity()
        self.world.add_component(play_button_entity, PositionComponent(self.screen.get_width() / 2 - 100, 250))
        self.world.add_component(play_button_entity, DimensionsComponent(200, 50))
        self.world.add_component(play_button_entity, RenderComponent(color=(0, 200, 0))) # Color del botón
        self.world.add_component(play_button_entity, TextComponent("JUGAR (1P)", 32, (255, 255, 255), font_path="assets/fonts/arcadeclassic/ARCADECLASSIC.TTF"))
        self.world.add_component(play_button_entity, ClickableComponent())
        self.world.add_component(play_button_entity, ButtonComponent(GameState.JUGANDO_SINGLE_PLAYER))
        self.entities.append(play_button_entity)

        # Botón JUGAR (Two Players)
        two_players_button_entity = self.world.create_entity()
        self.world.add_component(two_players_button_entity, PositionComponent(self.screen.get_width() / 2 - 100, 320))
        self.world.add_component(two_players_button_entity, DimensionsComponent(200, 50))
        self.world.add_component(two_players_button_entity, RenderComponent(color=(0, 150, 0)))
        self.world.add_component(two_players_button_entity, TextComponent("JUGAR (2P)", 32, (255, 255, 255), font_path="assets/fonts/arcadeclassic/ARCADECLASSIC.TTF"))
        self.world.add_component(two_players_button_entity, ClickableComponent())
        self.world.add_component(two_players_button_entity, ButtonComponent(GameState.JUGANDO_TWO_PLAYERS))
        self.entities.append(two_players_button_entity)

        # Botón SALIR
        exit_button_entity = self.world.create_entity()
        self.world.add_component(exit_button_entity, PositionComponent(self.screen.get_width() / 2 - 100, 390))
        self.world.add_component(exit_button_entity, DimensionsComponent(200, 50))
        self.world.add_component(exit_button_entity, RenderComponent(color=(200, 0, 0)))
        self.world.add_component(exit_button_entity, TextComponent("SALIR", 32, (255, 255, 255), font_path="assets/fonts/arcadeclassic/ARCADECLASSIC.TTF"))
        self.world.add_component(exit_button_entity, ClickableComponent())
        self.world.add_component(exit_button_entity, ButtonComponent(GameState.SALIR))
        self.entities.append(exit_button_entity)

    def cleanup(self):
        # Elimina todas las entidades creadas por esta escena
        for entity_id in self.entities:
            self.world.remove_entity(entity_id)
        self.entities = []

    def handle_event(self, event):
        # No hay lógica de eventos directa en la escena, los sistemas de input la manejan.
        pass

    def update(self, dt):
        # La lógica de actualización del menú es mínima, principalmente renderizado y entrada.
        pass

    def draw(self):
        # El sistema de renderizado se encarga de dibujar.
        pass
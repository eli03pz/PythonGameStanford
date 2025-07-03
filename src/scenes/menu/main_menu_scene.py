from scenes.base_scene import BaseScene
from utils.game_state import GameState
from systems.menu_systems import MenuInputSystem, MenuRenderSystem
from components.menu_components import (
    PositionComponent,
    DimensionsComponent,
    RenderComponent,
    TextComponent,
    ButtonComponent
)

class MainMenuScene(BaseScene):
    def setup(self):
        """
        Crea los sistemas y entidades específicas para esta escena.
        """
        print("MainMenuScene: Configurando sistemas y entidades del menú.")
        self.input_system = MenuInputSystem(self.game.world, self.game.game_state_manager)
        self.render_system = MenuRenderSystem(self.game.world, self.game.screen, self.game.game_state_manager)
        
        self.menu_entities = []
        
        button_width, button_height = 300, 60
        start_x = (self.game.screen_width - button_width) / 2
        button_spacing = 20
        # Corregimos el cálculo para centrarlo perfectamente
        num_buttons = 3
        total_menu_height = (num_buttons * button_height) + ((num_buttons - 1) * button_spacing)
        start_y = (self.game.screen_height / 2) - (total_menu_height / 2)
        
        buttons_to_create = [
            ("Play", GameState.JUGANDO_SINGLE_PLAYER),
            ("Two players", GameState.JUGANDO_TWO_PLAYERS),
            ("Opciones", GameState.OPCIONES),
            ("Salir", GameState.SALIR)
        ]
        
        for i, (text, action) in enumerate(buttons_to_create):
            entity_id = self.game.world.create_entity()
            self.menu_entities.append(entity_id)
            
            y_pos = start_y + i * (button_height + button_spacing)
            self.game.world.add_component(entity_id, PositionComponent(start_x, y_pos))
            self.game.world.add_component(entity_id, DimensionsComponent(button_width, button_height))
            self.game.world.add_component(entity_id, RenderComponent((41, 128, 185), (52, 152, 219), (35, 110, 155)))
            self.game.world.add_component(entity_id, TextComponent(text, 40, (236, 240, 241)))
            self.game.world.add_component(entity_id, ButtonComponent(action))

    def cleanup(self):
        """
        Elimina las entidades de esta escena para que no persistan en la siguiente.
        """
        print(f"MainMenuScene: Limpiando {len(self.menu_entities)} entidades.")
        for entity_id in self.menu_entities:
            self.game.world.remove_entity(entity_id)
        self.menu_entities.clear()

    def handle_events(self, events):
        self.input_system.process(events)

    def update(self, dt):
        pass 

    def draw(self, screen):
        self.render_system.process()

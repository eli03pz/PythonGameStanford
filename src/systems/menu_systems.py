import pygame
from components.menu_components import PositionComponent, DimensionsComponent, RenderComponent, TextComponent, ButtonComponent, ClickableComponent
from utils.game_state import GameState

class MenuInputSystem:
    def __init__(self, world, current_game_state):
        self.world = world
        self.current_game_state = current_game_state # Referencia al GameState actual

    def process(self, event):
        if self.current_game_state.state != GameState.MENU_PRINCIPAL:
            return

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            for entity in self.world.get_entities_with_components(PositionComponent, DimensionsComponent, ClickableComponent, ButtonComponent):
                pos = self.world.get_component(entity, PositionComponent)
                dim = self.world.get_component(entity, DimensionsComponent)
                button = self.world.get_component(entity, ButtonComponent)

                # Detección de colisión simple (rectángulo)
                if pos.x <= mouse_x <= pos.x + dim.width and \
                   pos.y <= mouse_y <= pos.y + dim.height:
                    print(f"Botón '{button.action.name}' clicado!")
                    self.current_game_state.set_state(button.action)
                    return # Solo procesar un clic por vez

class MenuRenderSystem:
    def __init__(self, world, screen):
        self.world = world
        self.screen = screen
        self.fonts = {} # Caché para fuentes cargadas

    def get_font(self, font_path, size):
        if (font_path, size) not in self.fonts:
            try:
                self.fonts[(font_path, size)] = pygame.font.Font(font_path, size)
            except FileNotFoundError:
                print(f"Advertencia: Fuente no encontrada en {font_path}. Usando fuente por defecto.")
                self.fonts[(font_path, size)] = pygame.font.Font(None, size)
        return self.fonts[(font_path, size)]

    def process(self):
        # Asegúrate de que solo se renderice el menú si el estado es MENU_PRINCIPAL
        # Esto se gestionará mejor en el bucle principal del juego al activar/desactivar sistemas.
        # Por ahora, asumimos que este sistema solo se llama cuando el estado es MENU_PRINCIPAL.

        for entity in self.world.get_entities_with_components(PositionComponent, DimensionsComponent, RenderComponent):
            pos = self.world.get_component(entity, PositionComponent)
            dim = self.world.get_component(entity, DimensionsComponent)
            render = self.world.get_component(entity, RenderComponent)

            if render.image_path:
                try:
                    image = pygame.image.load(render.image_path).convert_alpha()
                    image = pygame.transform.scale(image, (dim.width, dim.height))
                    self.screen.blit(image, (pos.x, pos.y))
                except pygame.error as e:
                    print(f"Error al cargar imagen {render.image_path}: {e}")
            elif render.color:
                pygame.draw.rect(self.screen, render.color, (pos.x, pos.y, dim.width, dim.height))

        for entity in self.world.get_entities_with_components(PositionComponent, TextComponent):
            pos = self.world.get_component(entity, PositionComponent)
            text = self.world.get_component(entity, TextComponent)

            font = self.get_font(text.font_path, text.font_size)
            text_surface = font.render(text.text, True, text.color)
            self.screen.blit(text_surface, (pos.x, pos.y))
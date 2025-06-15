import pygame
from utils.game_state import GameState
from game_state_manager import GameStateManager
from engine.ecs_world import ECSWorld
from systems.menu_systems import MenuInputSystem, MenuRenderSystem
from scenes.menu.main_menu_scene import MainMenuScene
# from scenes.game import GameScene # Tu escena de juego existente

# Inicializar Pygame
pygame.init()

# Configuración de la ventana
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Mi Videojuego ECS")

# Crear el mundo ECS
world = ECSWorld()

# Gestor de estados del juego
game_state_manager = GameStateManager()

# Inicializar escenas
scenes = {
    GameState.MENU_PRINCIPAL: MainMenuScene(world, screen, game_state_manager),
    # GameState.JUGANDO_SINGLE_PLAYER: GameScene(world, screen, game_state_manager, players=1), # Ajusta GameScene según necesites
    # GameState.JUGANDO_TWO_PLAYERS: GameScene(world, screen, game_state_manager, players=2)  # Ajusta GameScene según necesites
}

# Sistemas globales (que podrían estar activos en varios estados, o activarse/desactivarse)
menu_input_system = MenuInputSystem(world, game_state_manager)
menu_render_system = MenuRenderSystem(world, screen)
# Aquí añadirías tus sistemas de juego (MovimientoSystem, CollisionSystem, etc.)
# Por ahora, solo tenemos los de menú.

# Bucle principal del juego
running = True
clock = pygame.time.Clock()
FPS = 60

current_scene = None

while running:
    dt = clock.tick(FPS) / 1000.0  # Delta time en segundos

    # 1. Manejo de eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Los sistemas de entrada procesan eventos solo si están activos en el estado actual
        if game_state_manager.state == GameState.MENU_PRINCIPAL:
            menu_input_system.process(event)
        # Puedes añadir condiciones para otros sistemas de input de juego aquí:
        # elif game_state_manager.state in [GameState.JUGANDO_SINGLE_PLAYER, GameState.JUGANDO_TWO_PLAYERS]:
        #    game_input_system.process(event) # Necesitarías un GameInputSystem

    # 2. Actualización de escenas y sistemas basada en el estado del juego
    if game_state_manager.state == GameState.SALIR:
        running = False
        continue

    # Transición entre escenas
    if current_scene is None or current_scene.__class__.__name__ != scenes[game_state_manager.state].__class__.__name__:
        if current_scene:
            current_scene.cleanup() # Limpia entidades de la escena anterior
            print(f"Limpiando escena: {current_scene.__class__.__name__}")
        current_scene = scenes[game_state_manager.state]
        current_scene.setup() # Configura la nueva escena
        print(f"Cargando escena: {current_scene.__class__.__name__}")

    # Lógica de actualización (si la hay para la escena actual)
    current_scene.update(dt)

    # Limpiar pantalla
    screen.fill((0, 0, 0)) # Fondo negro, puedes cambiarlo

    # 3. Renderizado de sistemas activos
    if game_state_manager.state == GameState.MENU_PRINCIPAL:
        menu_render_system.process()
    elif game_state_manager.state in [GameState.JUGANDO_SINGLE_PLAYER, GameState.JUGANDO_TWO_PLAYERS]:
        # Aquí llamarías a tus sistemas de renderizado del juego
        current_scene.draw() # Suponiendo que GameScene tiene un método draw que llama a sus sistemas de renderizado
    # Puedes añadir más estados y sus sistemas de renderizado aquí

    # Actualizar la pantalla
    pygame.display.flip()

pygame.quit()
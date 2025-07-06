# ARCHIVO: scenes/pause_scene.py

import pygame
import sys
from scenes.base_scene import BaseScene
from utils.game_state import GameState

# Componentes y Sistemas locales para la escena de Pausa
class PositionComponent:
    def __init__(self, x, y): self.x, self.y = x, y
class DimensionsComponent:
    def __init__(self, w, h): self.width, self.height = w, h
class ButtonComponent:
    def __init__(self, action): self.state, self.action = 'normal', action

class PauseInputSystem:
    def __init__(self, world, gsm): self.world, self.gsm = world, gsm
    def process(self, events):
        mx, my = pygame.mouse.get_pos()
        for e in self.world.get_entities_with_components(PositionComponent, DimensionsComponent, ButtonComponent):
            pos, dim, btn = (self.world.get_component(e, c) for c in (PositionComponent, DimensionsComponent, ButtonComponent))
            btn.state = 'hover' if pos.x <= mx <= pos.x + dim.width and pos.y <= my <= pos.y + dim.height else 'normal'
        for event in events:
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                for e in self.world.get_entities_with_components(ButtonComponent):
                    btn = self.world.get_component(e, ButtonComponent)
                    if btn.state == 'hover': self.gsm.set_state(btn.action); return

class PauseRenderSystem:
    def __init__(self, world, screen):
        self.world, self.screen = world, screen
        self.font_title = pygame.font.Font(None, 90)
        self.font_button = pygame.font.Font(None, 50)
    def process(self):
        overlay = pygame.Surface((self.screen.get_width(), self.screen.get_height()), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180)); self.screen.blit(overlay, (0, 0))
        title_surf = self.font_title.render("PAUSA", True, "white")
        self.screen.blit(title_surf, title_surf.get_rect(centerx=self.screen.get_width()/2, y=150))
        for e in self.world.get_entities_with_components(PositionComponent, DimensionsComponent, ButtonComponent):
            pos, dim, btn = (self.world.get_component(e, c) for c in (PositionComponent, DimensionsComponent, ButtonComponent))
            color = (52, 152, 219) if btn.state == 'hover' else (41, 128, 185)
            pygame.draw.rect(self.screen, color, (pos.x, pos.y, dim.width, dim.height), border_radius=12)
            pygame.draw.rect(self.screen, (236, 240, 241), (pos.x, pos.y, dim.width, dim.height), 2, border_radius=12)
            text = "Reanudar" if btn.action != GameState.MENU_PRINCIPAL else "Menú Principal"
            text_surf = self.font_button.render(text, True, "white")
            self.screen.blit(text_surf, text_surf.get_rect(center=(pos.x + dim.width/2, pos.y + dim.height/2)))

class PauseScene(BaseScene):
    def setup(self):
        self.entities = []
        self.input_system = PauseInputSystem(self.game.world, self.game.game_state_manager)
        self.render_system = PauseRenderSystem(self.game.world, self.game.screen)
        
        # CORRECCIÓN: Guardar el estado previo para saber a dónde volver
        self.resume_state = self.game.previous_game_state
        
        # CORRECCIÓN: Asignar las acciones correctas a los botones
        buttons = [
            (self.resume_state, "Reanudar"),
            (GameState.MENU_PRINCIPAL, "Menú Principal")
        ]
        
        width, height = 400, 70; start_x = (self.game.screen_width - width) / 2; start_y = 300
        for i, (action, text) in enumerate(buttons):
            entity_id = self.game.world.create_entity()
            self.entities.append(entity_id)
            self.game.world.add_component(entity_id, PositionComponent(start_x, start_y + i * 85))
            self.game.world.add_component(entity_id, DimensionsComponent(width, height))
            self.game.world.add_component(entity_id, ButtonComponent(action))

    def cleanup(self):
        for entity_id in self.entities: self.game.world.remove_entity(entity_id)
    def handle_events(self, events): self.input_system.process(events)
    def update(self, dt): pass
    def draw(self, screen): self.render_system.process()

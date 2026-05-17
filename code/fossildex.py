"""
fossildex.py – The interactive encyclopedia for discovered fossils.
"""

import pygame
from settings import WIDTH, HEIGHT

class FossilDex:
    def __init__(self, level_ref):
        self.display_surface = pygame.display.get_surface()
        self.level_ref = level_ref  # Used to check the excavated_fossils list

        # ── Load Graphics ────────────────────────────────────────────────────
        self.img_body = pygame.image.load('graphics/fossildex/device/dexbody.png').convert_alpha()
        self.img_cursor = pygame.image.load('graphics/fossildex/device/dexcursor.png').convert_alpha()
        
        self.infographics = []
        for i in range(1, 7):
            surf = pygame.image.load(f'graphics/fossildex/infographics/fossil{i}.png').convert_alpha()
            self.infographics.append(surf)

        # ── Fonts & Text ─────────────────────────────────────────────────────
        self.font = pygame.font.Font(None, 60)
        
        self.fossil_names = [
            "Fossil 1", "Fossil 2", "Fossil 3", 
            "Fossil 4", "Fossil 5", "Fossil 6"
        ]

        self.selection = 0
        self.viewing_info = False

    def is_unlocked(self, index):
        """Only returns True if this exact fossil was successfully excavated."""
        # This checks the new list we are adding to level.py!
        return index in self.level_ref.excavated_fossils

    def handle_event(self, event):
        """Handles keyboard input passed from main.py"""
        if event.type == pygame.KEYDOWN:
            if self.viewing_info:
                self.viewing_info = False
                return

            if event.key == pygame.K_UP or event.key == pygame.K_w:
                self.selection = (self.selection - 1) % 6
            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                self.selection = (self.selection + 1) % 6
            
            elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                if self.is_unlocked(self.selection):
                    self.viewing_info = True

    def draw(self):
        if self.viewing_info:
            self.display_surface.blit(self.infographics[self.selection], (0, 0))
            return

        self.display_surface.blit(self.img_body, (0, 0))

        start_x = 200
        start_y = 230
        spacing = 60

        for i in range(6):
            y_pos = start_y + (i * spacing)

            if self.is_unlocked(i):
                text = self.fossil_names[i]
                color = 'Black'
            else:
                text = "-----------"
                color = 'Gray'

            text_surf = self.font.render(text, True, color)
            self.display_surface.blit(text_surf, (start_x, y_pos))

            if i == self.selection:
                cursor_x = start_x - 80 
                cursor_y = y_pos - 10
                self.display_surface.blit(self.img_cursor, (cursor_x, cursor_y))
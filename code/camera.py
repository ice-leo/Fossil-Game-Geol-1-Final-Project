"""
camera.py  –  YSortCameraGroup
              Draws sprites sorted by their rect.centery so taller objects
              appear behind shorter ones (depth illusion).
              Also offsets every draw call so the player is centred.
"""

import pygame
from settings import WIDTH, HEIGHT


class YSortCameraGroup(pygame.sprite.Group):

    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()

        # Half-screen offset used to keep the camera centred on the player
        self.half_w = self.display_surface.get_size()[0] // 2
        self.half_h = self.display_surface.get_size()[1] // 2
        self.offset  = pygame.math.Vector2()

        # ── Optional ground / floor image ────────────────────────────────
        # If you have a big background image place it here; otherwise a
        # solid colour fill in level.py handles the background.
        self.floor_surf = None
        self.floor_rect = None

    def load_floor(self, path: str):
        """Load an optional static floor/background image."""
        try:
            self.floor_surf = pygame.image.load(path).convert()
            self.floor_rect = self.floor_surf.get_rect(topleft=(0, 0))
        except Exception:
            self.floor_surf = None

    def custom_draw(self, player):
        # Camera offset: shift world so player is at screen centre
        self.offset.x = player.rect.centerx - self.half_w
        self.offset.y = player.rect.centery - self.half_h

        # Draw floor first (if any)
        if self.floor_surf:
            floor_offset_pos = self.floor_rect.topleft - self.offset
            self.display_surface.blit(self.floor_surf, floor_offset_pos)

        # Draw sprites sorted by bottom-y for depth
        for sprite in sorted(self.sprites(), key=lambda s: s.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)

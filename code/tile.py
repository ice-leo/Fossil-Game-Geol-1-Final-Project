"""
tile.py  –  Static tile sprites used when building the island map.
"""

import pygame
from settings import TILESIZE


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, groups, sprite_type, surface=None):
        super().__init__(groups)
        self.sprite_type = sprite_type

        if surface is None:
            surface = pygame.Surface((TILESIZE, TILESIZE))
            surface.fill((100, 180, 100))   # fallback green

        self.image = surface
        self.rect  = self.image.get_rect(topleft=pos)

        # Collision hitbox – shrink vertically for objects/boundaries
        if sprite_type == 'object':
            self.hitbox = self.rect.inflate(0, -40)
        elif sprite_type == 'invisible':
            self.hitbox = self.rect
        else:
            self.hitbox = self.rect.inflate(0, -10)

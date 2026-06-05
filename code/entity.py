"""
entity.py  –  Base class shared by Player and NPC.
              Handles movement and hitbox-based collision.
"""

import pygame
import math


class Entity(pygame.sprite.Sprite):

    def __init__(self, groups):
        super().__init__(groups)
        self.frame_index = 0
        self.animation_speed = 0.15
        self.direction = pygame.math.Vector2()

    # ── Movement ─────────────────────────────────────────────────────────────

    def move(self, speed: float, obstacle_sprites: pygame.sprite.Group):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.hitbox.x += self.direction.x * speed
        self._collision('horizontal', obstacle_sprites)

        self.hitbox.y += self.direction.y * speed
        self._collision('vertical', obstacle_sprites)

        self.rect.center = self.hitbox.center

    def _collision(self, direction: str, obstacle_sprites: pygame.sprite.Group):
        if direction == 'horizontal':
            for sprite in obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0:
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction.x < 0:
                        self.hitbox.left = sprite.hitbox.right

        elif direction == 'vertical':
            for sprite in obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0:
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.direction.y < 0:
                        self.hitbox.top = sprite.hitbox.bottom

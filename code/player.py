"""
player.py  –  Player character.
              Movement + directional animation only.
              No combat, no health bar, no magic.
"""

import pygame
from entity   import Entity
from settings import PLAYER_SPEED, TILESIZE
from support  import import_folder


class Player(Entity):

    def __init__(self, pos, groups, obstacle_sprites, interact_callback):
        super().__init__(groups)

        # ── Base sprite (placeholder until real art is added) ─────────────
        raw = pygame.image.load('graphics/player/down/0.png').convert_alpha() \
              if self._art_exists('graphics/player/down/0.png') \
              else self._make_placeholder()
        self.image = raw
        self.rect  = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(-6, -26)

        # ── Animations ───────────────────────────────────────────────────
        self.animations = {
            'up': [], 'down': [], 'left': [], 'right': [],
            'up_idle': [], 'down_idle': [], 'left_idle': [], 'right_idle': [],
        }
        self._import_assets()

        self.status = 'down_idle'

        # ── References ───────────────────────────────────────────────────
        self.obstacle_sprites = obstacle_sprites
        self.interact_callback = interact_callback   # called when E is pressed

        # ── State ────────────────────────────────────────────────────────
        self.points           = 0
        self.interacting      = False
        self.interaction_cooldown = 300   # ms
        self.interaction_time     = 0

    # ── Helpers ─────────────────────────────────────────────────────────────

    @staticmethod
    def _art_exists(path: str) -> bool:
        import os
        return os.path.isfile(path)

    def _make_placeholder(self) -> pygame.Surface:
        surf = pygame.Surface((64, 64), pygame.SRCALPHA)
        pygame.draw.ellipse(surf, (80, 140, 200), surf.get_rect())
        return surf

    def _import_assets(self):
        base = 'graphics/player'
        for anim in self.animations:
            path = f'{base}/{anim}'
            frames = import_folder(path)
            self.animations[anim] = frames

    # ── Input ────────────────────────────────────────────────────────────────

    def _handle_input(self):
        keys = pygame.key.get_pressed()

        # Movement
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.direction.y = -1
            self.status = 'up'
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.direction.y = 1
            self.status = 'down'
        else:
            self.direction.y = 0

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.direction.x = -1
            self.status = 'left'
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.direction.x = 1
            self.status = 'right'
        else:
            self.direction.x = 0

        # Idle suffix
        if self.direction.x == 0 and self.direction.y == 0:
            if 'idle' not in self.status:
                self.status += '_idle'

        # Interact
        now = pygame.time.get_ticks()
        if keys[pygame.K_e] or keys[pygame.K_RETURN]:
            if not self.interacting and (now - self.interaction_time) > self.interaction_cooldown:
                self.interacting = True
                self.interaction_time = now
                self.interact_callback()
        else:
            self.interacting = False

    # ── Animation ────────────────────────────────────────────────────────────

    def _animate(self):
        animation = self.animations.get(self.status, self.animations['down_idle'])
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0
        self.image = animation[int(self.frame_index)]
        self.rect  = self.image.get_rect(center=self.hitbox.center)

    # ── Update ───────────────────────────────────────────────────────────────

    def update(self):
        self._handle_input()
        self._animate()
        self.move(PLAYER_SPEED, self.obstacle_sprites)

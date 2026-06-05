"""
player.py  –  Player character.
              Movement + directional animation only.
              Interact key is E only — Enter is reserved for screen transitions.
"""

import pygame
from entity   import Entity
from settings import PLAYER_SPEED
from support  import import_folder, resource_path
import os


class Player(Entity):

    def __init__(self, pos, groups, obstacle_sprites, interact_callback):
        super().__init__(groups)

        # ── Base sprite ───────────────────────────────────────────────────
        art_path = resource_path('graphics/player/down/0.png')
        if os.path.isfile(art_path):
            raw = pygame.image.load(art_path).convert_alpha()
        else:
            raw = self._make_placeholder()

        self.image  = raw
        self.rect   = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(-6, -26)

        # ── Animations ───────────────────────────────────────────────────
        self.animations = {
            'up': [], 'down': [], 'left': [], 'right': [],
            'up_idle': [], 'down_idle': [], 'left_idle': [], 'right_idle': [],
        }
        self._import_assets()
        self.status = 'down_idle'

        # ── References ───────────────────────────────────────────────────
        self.obstacle_sprites  = obstacle_sprites
        self.interact_callback = interact_callback

        # ── State ────────────────────────────────────────────────────────
        self.points               = 0
        self.interacting          = False
        self.interaction_cooldown = 300   # ms
        self.interaction_time     = 0

    # ── Helpers ─────────────────────────────────────────────────────────────

    def _make_placeholder(self):
        surf = pygame.Surface((64, 64), pygame.SRCALPHA)
        pygame.draw.ellipse(surf, (80, 140, 200), surf.get_rect())
        return surf

    def _import_assets(self):
        base = 'graphics/player'
        for anim in self.animations:
            frames = import_folder(f'{base}/{anim}')
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

        # Interact — E key ONLY (Enter is reserved for pre-game screen transitions)
        now = pygame.time.get_ticks()
        if keys[pygame.K_e]:
            if not self.interacting and (now - self.interaction_time) > self.interaction_cooldown:
                self.interacting      = True
                self.interaction_time = now
                self.interact_callback()
        else:
            self.interacting = False

    # ── Animation ────────────────────────────────────────────────────────────

    def _animate(self):
        animation    = self.animations.get(self.status, self.animations['down_idle'])
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

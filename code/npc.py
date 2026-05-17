"""
npc.py  –  NPC sprites.
           Two NPCs live on the island:
             • 'excavation_npc'  →  triggers excavation menu
             • 'quiz_npc'        →  triggers quiz (locked until excavation done)
"""

import pygame
from entity  import Entity
from support import import_folder
from settings import NPC_DATA, TILESIZE


INTERACT_RADIUS = 90   # pixels from centre to centre


class NPC(Entity):

    def __init__(self, pos, groups, obstacle_sprites, npc_type: str,
                 trigger_callback):
        super().__init__(groups)

        self.npc_type = npc_type
        self.data     = NPC_DATA[npc_type]
        self.trigger_callback = trigger_callback   # called when player interacts

        # ── Sprite ───────────────────────────────────────────────────────
        self.animations = {'idle': []}
        self._import_assets()
        self.status = 'idle'

        self.image  = self.animations['idle'][0]
        self.rect   = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(-6, -26)

        self.obstacle_sprites = obstacle_sprites

        # ── State ────────────────────────────────────────────────────────
        self.completed = False   # set True once the linked game is done

    # ── Asset loading ────────────────────────────────────────────────────────

    def _import_assets(self):
        path = self.data['graphic']
        frames = import_folder(path)
        self.animations['idle'] = frames

    # ── Check proximity ──────────────────────────────────────────────────────

    def is_player_near(self, player_rect: pygame.Rect) -> bool:
        dx = self.rect.centerx - player_rect.centerx
        dy = self.rect.centery - player_rect.centery
        dist = (dx * dx + dy * dy) ** 0.5
        return dist <= INTERACT_RADIUS

    # ── Dialogue text ─────────────────────────────────────────────────────────

    def get_dialogue(self, excavation_done: bool = False) -> str:
        if self.completed:
            return self.data.get('dialogue_done', '...')
        if self.npc_type == 'quiz_npc' and not excavation_done:
            return self.data.get('dialogue_locked', '...')
        return self.data.get('dialogue_idle', '...')

    # ── Animation ────────────────────────────────────────────────────────────

    def _animate(self):
        animation = self.animations['idle']
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0
        self.image = animation[int(self.frame_index)]
        self.rect  = self.image.get_rect(center=self.hitbox.center)

    # ── Update ───────────────────────────────────────────────────────────────

    def update(self):
        self._animate()

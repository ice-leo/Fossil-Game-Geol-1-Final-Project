"""
level.py – Sets up the overworld map, spawns the player and NPCs,
           and handles the interactions between them.
"""

import pygame
import csv
from settings import TILESIZE
from tile import Tile
from player import Player
from npc import NPC
from camera import YSortCameraGroup
from ui import UI
from support import resource_path


class Level:
    def __init__(self, change_state):
        self.display_surface = pygame.display.get_surface()
        self.change_state = change_state

        # ── Sprite Groups ────────────────────────────────────────────────────
        self.visible_sprites  = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()
        self.interact_sprites = pygame.sprite.Group()

        # ── Game Progress State ──────────────────────────────────────────────
        self.exc_levels_done   = []
        self.excavated_fossils = []
        self.quiz_done         = False

        # ── Setup ────────────────────────────────────────────────────────────
        self.ui = UI()
        self.setup_level()

    # ── CSV tilemap loader ───────────────────────────────────────────────────

    def _load_csv_blocks(self, path: str):
        """
        Read a Tiled CSV export and spawn an invisible Tile for every cell
        that is NOT -1.  The CSV row = tile-y, column = tile-x.
        Place the file at:  graphics/tilemap/map_FloorBlocks.csv
        """
        try:
            with open(path, newline='') as f:
                reader = csv.reader(f)
                for row_index, row in enumerate(reader):
                    for col_index, cell in enumerate(row):
                        if cell.strip() not in ('-1', ''):
                            x = col_index * TILESIZE
                            y = row_index * TILESIZE
                            Tile((x, y), [self.obstacle_sprites], 'invisible')
        except FileNotFoundError:
            print(f"[Level] WARNING: FloorBlocks CSV not found at {path}")

    def setup_level(self):
        # 1. Load the background map image (resource_path so it works everywhere)
        self.visible_sprites.load_floor(resource_path('graphics/tilemap/ground.png'))

        # 2. Spawn Boundaries (Invisible Walls for 3648×3200 map)
        for x in range(-1, 58):
            Tile((x * TILESIZE, -1 * TILESIZE), [self.obstacle_sprites], 'invisible')
            Tile((x * TILESIZE, 50 * TILESIZE), [self.obstacle_sprites], 'invisible')

        for y in range(-1, 51):
            Tile((-1 * TILESIZE, y * TILESIZE), [self.obstacle_sprites], 'invisible')
            Tile((57 * TILESIZE, y * TILESIZE), [self.obstacle_sprites], 'invisible')

        # 3. Load FloorBlocks from CSV (every non -1 cell becomes a collision tile)
        self._load_csv_blocks(resource_path('graphics/tilemap/map_FloorBlocks.csv'))

        # 3. Spawn the Player
        self.player = Player(
            pos=(640, 360),
            groups=[self.visible_sprites],
            obstacle_sprites=self.obstacle_sprites,
            interact_callback=self.player_interact
        )

        # 4. Spawn NPCs
        self.npc_excavation = NPC(
            pos=(400, 300),
            groups=[self.visible_sprites, self.interact_sprites],
            obstacle_sprites=self.obstacle_sprites,
            npc_type='excavation_npc',
            trigger_callback=self.trigger_excavation
        )

        self.npc_quiz = NPC(
            pos=(2000, 300),
            groups=[self.visible_sprites, self.interact_sprites],
            obstacle_sprites=self.obstacle_sprites,
            npc_type='quiz_npc',
            trigger_callback=self.trigger_quiz
        )

    # ── Interaction Logic ────────────────────────────────────────────────────

    def player_interact(self):
        """Called by the Player class when 'E' is pressed."""
        for sprite in self.interact_sprites:
            if sprite.is_player_near(self.player.rect):
                sprite.trigger_callback(sprite)
                break

    def trigger_excavation(self, npc):
        """Callback for Dr. Pebble."""
        if len(self.exc_levels_done) < 3:
            self.change_state('excavation')
        else:
            npc.completed = True

    def trigger_quiz(self, npc):
        """Callback for Prof. Stratum."""
        if self.quiz_done:
            # Already completed — mark NPC so it shows the done dialogue
            npc.completed = True
        elif len(self.exc_levels_done) == 3:
            self.change_state('quiz')
        # else: quiz_npc will show dialogue_locked automatically via get_dialogue()

    # ── Main Loop for Level ──────────────────────────────────────────────────

    def run(self):
        """Updates and draws everything in the overworld."""
        self.visible_sprites.update()

        hint            = ""
        active_dialogue = ""

        for sprite in self.interact_sprites:
            if sprite.is_player_near(self.player.rect):
                hint = "Press E to talk"

                excavation_done = (len(self.exc_levels_done) == 3)
                active_dialogue = (
                    f"{sprite.data['name']}: "
                    f"{sprite.get_dialogue(excavation_done)}"
                )
                break

        self.visible_sprites.custom_draw(self.player)

        if active_dialogue:
            JOYSTIX = resource_path('graphics/font/joystix.ttf')
            font      = pygame.font.Font(JOYSTIX, 15)
            text_surf = font.render(active_dialogue, True, 'White')
            bg_rect   = text_surf.get_rect(
                midbottom=(self.player.rect.centerx, self.player.rect.top - 20)
            )

            offset_bg_rect          = bg_rect.copy()
            offset_bg_rect.topleft -= self.visible_sprites.offset

            pygame.draw.rect(
                self.display_surface,
                (50, 50, 50),
                offset_bg_rect.inflate(20, 20),
                border_radius=5
            )
            self.display_surface.blit(text_surf, offset_bg_rect)

        self.ui.display(self.player.points, hint, self.exc_levels_done, self.quiz_done)
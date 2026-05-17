"""
level.py – Sets up the overworld map, spawns the player and NPCs, 
           and handles the interactions between them.
"""

import pygame
from settings import TILESIZE
from tile import Tile
from player import Player
from npc import NPC
from camera import YSortCameraGroup
from ui import UI

class Level:
    def __init__(self, change_state):
        self.display_surface = pygame.display.get_surface()
        self.change_state = change_state

        # ── Sprite Groups ────────────────────────────────────────────────────
        # visible_sprites is your custom YSortCameraGroup from camera.py
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()
        self.interact_sprites = pygame.sprite.Group()

        # ── Game Progress State ──────────────────────────────────────────────
        self.exc_levels_done = []
        self.excavated_fossils = []  # <--- ADD THIS LINE HERE!
        self.quiz_done = False

        # ── Setup ────────────────────────────────────────────────────────────
        self.ui = UI()
        self.setup_level()

    def setup_level(self):
        # 1. Load the background map image
        # Make sure the path matches where your ground.png is located!
        self.visible_sprites.load_floor('graphics/tilemap/ground.png')

        # 2. Spawn Boundaries (Invisible Walls for 3648x3200 map)
        # Top and Bottom walls
        for x in range(-1, 58):
            Tile((x * TILESIZE, -1 * TILESIZE), [self.obstacle_sprites], 'invisible')
            Tile((x * TILESIZE, 50 * TILESIZE), [self.obstacle_sprites], 'invisible')
            
        # Left and Right walls
        for y in range(-1, 51):
            Tile((-1 * TILESIZE, y * TILESIZE), [self.obstacle_sprites], 'invisible')
            Tile((57 * TILESIZE, y * TILESIZE), [self.obstacle_sprites], 'invisible')

        # 3. Spawn the Player
        self.player = Player(
            pos=(640, 360), # Spawn near the center
            groups=[self.visible_sprites],
            obstacle_sprites=self.obstacle_sprites,
            interact_callback=self.player_interact
        )

        # 4. Spawn the NPCs (Adjust positions to fit nicely on your map)
        self.npc_excavation = NPC(
            pos=(400, 300), 
            groups=[self.visible_sprites, self.interact_sprites],
            obstacle_sprites=self.obstacle_sprites,
            npc_type='excavation_npc',
            trigger_callback=self.trigger_excavation
        )

        self.npc_quiz = NPC(
            pos=(800, 300), 
            groups=[self.visible_sprites, self.interact_sprites],
            obstacle_sprites=self.obstacle_sprites,
            npc_type='quiz_npc',
            trigger_callback=self.trigger_quiz
        )

    # ── Interaction Logic ────────────────────────────────────────────────────

    def player_interact(self):
        """Called automatically by the Player class when 'E' or 'Enter' is pressed."""
        for sprite in self.interact_sprites:
            if sprite.is_player_near(self.player.rect):
                # Trigger the specific NPC's callback function
                sprite.trigger_callback(sprite)
                break

    def trigger_excavation(self, npc):
        """Callback for Dr. Pebble."""
        if len(self.exc_levels_done) < 3:
            self.change_state('excavation')
        else:
            npc.completed = True
            # The player has already done all 3 levels, so just show dialogue.

    def trigger_quiz(self, npc):
        """Callback for Prof. Stratum."""
        # The player can only play the quiz if they excavated all 3 levels
        if len(self.exc_levels_done) == 3 and not self.quiz_done:
            self.change_state('quiz')
        else:
            # If they haven't finished excavating, the NPC class handles 
            # showing the 'dialogue_locked' text!
            pass 

    # ── Main Loop for Level ──────────────────────────────────────────────────

    def run(self):
        """Updates and draws everything in the overworld."""
        # Update logic
        self.visible_sprites.update()
        
        # Check proximity for the UI hint
        hint = ""
        active_dialogue = ""
        for sprite in self.interact_sprites:
            if sprite.is_player_near(self.player.rect):
                hint = "Press E to talk"
                
                # Fetch their dialogue based on game state
                excavation_done = (len(self.exc_levels_done) == 3)
                active_dialogue = f"{sprite.data['name']}: {sprite.get_dialogue(excavation_done)}"
                break

        # Draw logic
        self.visible_sprites.custom_draw(self.player)
        
        # Draw Dialogue pop-up if near an NPC
        if active_dialogue:
            font = pygame.font.Font(None, 36)
            text_surf = font.render(active_dialogue, True, 'White')
            bg_rect = text_surf.get_rect(midbottom=(self.player.rect.centerx, self.player.rect.top - 20))
            
            # Since the camera offsets the world, we need to apply that offset to our text box
            offset_bg_rect = bg_rect.copy()
            offset_bg_rect.topleft -= self.visible_sprites.offset
            
            pygame.draw.rect(self.display_surface, (50, 50, 50), offset_bg_rect.inflate(20, 20), border_radius=5)
            self.display_surface.blit(text_surf, offset_bg_rect)

        # Draw the permanent UI
        self.ui.display(self.player.points, hint, self.exc_levels_done, self.quiz_done)
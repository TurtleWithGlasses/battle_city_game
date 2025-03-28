import pygame
import gameconfig as gc
from characters import Tank, PlayerTank, EnemyTank, SpecialTank
from game_hud import GameHud
from random import shuffle, choice, randint
from tile import BrickTile, SteelTile, ForestTile, IceTile, WaterTile
from fade_animate import Fade
from score_screen import ScoreScreen
from eagle import Eagle
from game_over import GameOver
import random


class Game:
    def __init__(self, main, assets, player_1=True, player_2=False):
        """The main Game Object when playing"""
        # The main file
        self.main = main
        self.assets = assets

        # Object groups
        self.groups = {
            "Ice_Tiles": pygame.sprite.Group(),
            "Water_Tiles": pygame.sprite.Group(),
            "Player_Tanks": pygame.sprite.Group(),
            "All_Tanks": pygame.sprite.Group(),
            "Bullets": pygame.sprite.Group(),
            "Destructable_Tiles": pygame.sprite.Group(),
            "Eagle": pygame.sprite.GroupSingle(),
            "Impassable_Tiles": pygame.sprite.Group(),
            "Explosion": pygame.sprite.Group(),
            "Forest_Tiles": pygame.sprite.Group(),
            "Power_Ups": pygame.sprite.Group(),
            "Scores": pygame.sprite.Group(),

            }

        # Player attributes
        self.top_score = 20000
        self.player_1_active = player_1
        self.player_1_score = 0
        self.player_2_active = player_2
        self.player_2_score = 0

        # Game HUD
        self.hud = GameHud(self, self.assets)

        # Level information
        self.level_num = 1
        self.level_complete = False
        self.level_transition_timer = None
        self.data = self.main.levels

        # Level Fade
        self.fade = Fade(self, self.assets, 10)
        # Stage Score Screen
        self.score_screen = ScoreScreen(self, self.assets)
        # Game Over
        self.game_over_screen = GameOver(self, self.assets)

        # Player objects
        if self.player_1_active:
            self.player1 = PlayerTank(self, self.assets, self.groups, gc.PL1_position, "Up", "Gold", 0)
        if self.player_2_active:
            self.player2 = PlayerTank(self, self.assets, self.groups, gc.PL2_position, "Up", "Green", 0)
        
        # Number of enemy tanks
        self.enemies = gc.STD_ENEMIES
        self.enemy_tank_spawn_timer = gc.TANK_SPAWNING_TIME
        self.enemy_tank_positions = [gc.Pc1_position, gc.Pc2_position, gc.Pc3_position]

        # Load the stage
        self.create_new_stage()

        # Fortify Base Power
        self.fortify = False
        self.fortify_timer = pygame.time.get_ticks()

        # Game over
        self.end_game = False
        self.game_on = False
        self.game_over = False

    
    def input(self):
        """Handles inputs for the game when it's running.."""
        keypressed = pygame.key.get_pressed()
        if self.player_1_active:
            self.player1.input(keypressed)
        if self.player_2_active:
            self.player2.input(keypressed)

        # pygame event handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.main.run = False
            
            # Keyboard shortcut to quit game
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.end_game = True
                
                if event.key == pygame.K_SPACE:
                    if self.player_1_active:
                        self.player1.shoot()

                if event.key == pygame.K_RCTRL:
                    if self.player_2_active:
                        self.player2.shoot()
                    
    def update(self):
        #Update the hud
        self.hud.update()

        if self.game_over_screen.active:
            self.game_over_screen.update()

        if self.fade.fade_active:
            self.fade.update()
            if not self.fade.fade_active:
                for tank in self.groups["All_Tanks"]:
                    tank.spawn_timer = pygame.time.get_ticks()
            return
        
        if not self.game_over:
            if self.player_1_active and self.player_2_active:
                if self.player1.game_over and self.player2.game_over and not self.game_over_screen.active:
                    self.groups["All_Tanks"].empty()
                    self.game_over = True
                    self.assets.channel_gameover_sound.play(self.assets.gameover_sound)
                    self.game_over_screen.activate()
                    return
            elif self.player_1_active and not self.player_2_active and not self.game_over_screen.active:
                if self.player1.game_over:
                    self.groups["All_Tanks"].empty()
                    self.game_over = True
                    self.assets.channel_gameover_sound.play(self.assets.gameover_sound)
                    self.game_over_screen.activate()
                    return
        elif self.game_over and not self.end_game and not self.game_over_screen.active:
            self.stage_transition(True)
            self.assets.channel_gameover_sound.play(self.assets.gameover_sound)
            return
        
        if self.fortify:
            if pygame.time.get_ticks() - self.fortify_timer >= 10000:
                self.power_up_fortify(start=False, end=True)
                self.fortify = False

        # if self.player_1_active:
        #     self.player1.update()
        # if self.player_2_active:
        #     self.player2.update()
        for dict_key in self.groups.keys():
            if dict_key == "Player_Tanks":
                continue
            for item in self.groups[dict_key]:
                item.update()

        self.spawn_enemy_tanks()

        for tank in self.groups["All_Tanks"]:
            if tank.enemy is True and tank.spawning is False:
                self.assets.channel_enemy_movement_sound.play(self.assets.enemy_movement_sound)
                break

        # Check to see if stage enemies have all been killed
        if self.enemies_killed <= 0 and self.level_complete is False:
            self.level_complete = True
            self.level_transition_timer = pygame.time.get_ticks()
        
        # Stage complete, load next stage
        if self.level_complete:
            if pygame.time.get_ticks() - self.level_transition_timer >= gc.TRANSITION_TIMER:
                self.stage_transition()
                # self.level_num += 1
                # self.create_new_stage()
                    
    def draw(self, window):
        """Drawing to the screen"""
        if self.assets:
            self.hud.draw(window)
            
            if self.score_screen.active:
                self.score_screen.draw(window)
                return
            # if self.player_1_active:
            #     self.player1.draw(window)
            # if self.player_2_active:
            #     self.player2.draw(window)
            for dict_key in self.groups.keys():
                if dict_key == "Impassable_Tiles":
                    continue
                if self.fade.fade_active is True and (dict_key == "All_Tanks" or  dict_key == "Player_Tanks"):
                    continue
                for item in self.groups[dict_key]:
                    item.draw(window)
        else:
            print("[ERROR] Game assets are missing!")
        
        if self.fade.fade_active:
            self.fade.draw(window)
        
        if self.game_over_screen.active:
            self.game_over_screen.draw(window)
    
    def create_new_stage(self):
        # Reset the various sprite groups back to Zero
        for key, value in self.groups.items():
            if key == "Player_Tanks":
                continue
            value.empty()

        # Retreives the specific level data
        self.current_level_data = self.data.level_data[self.level_num-1]

        # Number of enemy tanks to spawn in the stage
        self.enemies = choice([16,17,18,20])
        # self.enemies = 20

        # Track the number of enemies killed back down to zero
        self.enemies_killed = self.enemies
        
        # Load in the level data
        self.load_level_data(self.current_level_data)
        self.eagle = Eagle(self, self.assets, self.groups)
        self.level_complete = False

        self.assets.game_start_sound.play()

        self.fade.level = self.level_num
        self.fade.stage_image = self.fade.create_stage_image()
        self.fade.fade_active = True

        # Generating the spawn queue for the computer tanks
        self.generate_spawn_queue()
        self.spawn_pos_index = 0
        self.spawn_queue_index = 0

        if self.player_1_active:
            self.player1.new_stage_spawn(gc.PL1_position)
        if self.player_2_active:
            self.player2.new_stage_spawn(gc.PL2_position)
    
    def load_level_data(self, level):
        """Load level data"""
        self.grid = []
        for i, row in enumerate(level):
            line = []
            for j, tile in enumerate(row):
                pos = (gc.SCREEN_BORDER_LEFT + (j * gc.image_size // 2),
                       gc.SCREEN_BORDER_TOP + (i * gc.image_size // 2))
                if int(tile) < 0:
                    line.append(" ")
                elif int(tile) == 432:
                    line.append(f"{tile}")
                    map_tile = BrickTile(pos, self.groups["Destructable_Tiles"], self.assets.brick_tiles)
                    self.groups["Impassable_Tiles"].add(map_tile)
                elif int(tile) == 482:
                    line.append(f"{tile}")
                    map_tile = SteelTile(pos, self.groups["Destructable_Tiles"], self.assets.steel_tiles)
                    self.groups["Impassable_Tiles"].add(map_tile)
                elif int(tile) == 483:
                    line.append(f"{tile}")
                    map_tile = ForestTile(pos, self.groups["Forest_Tiles"], self.assets.forest_tiles)
                elif int(tile) == 484:
                    line.append(f"{tile}")
                    map_tile = IceTile(pos, self.groups["Ice_Tiles"], self.assets.ice_tiles)
                elif int(tile) == 533:
                    line.append(f"{tile}")
                    map_tile = WaterTile(pos, self.groups["Water_Tiles"], self.assets.water_tiles)
                    self.groups["Impassable_Tiles"].add(map_tile)
                else:
                    line.append(f"{tile}")
            self.grid.append(line)
    
    def generate_spawn_queue(self):
        """Generate a list of tanks that will be spawning during the level"""
        queue_key = f"queue_{str(min((self.level_num-1 % 36) // 3, 11))}"
        self.spawn_queue_ratios = gc.tank_spawn_queue[queue_key]
        self.spawn_queue = []

        for level, ratio in enumerate(self.spawn_queue_ratios):
            for i in range(int(round(self.enemies * (ratio / 100)))):
                self.spawn_queue.append(f"level_{level}")
        shuffle(self.spawn_queue)

    def spawn_enemy_tanks(self):
        """Spawn enemy tanks, each tank spawns as per the queue"""
        behavior = random.choice(["chaser", "evader","patroller"])
        if self.enemies == 0:
            return
        if pygame.time.get_ticks() - self.enemy_tank_spawn_timer >= gc.TANK_SPAWNING_TIME:
            position = self.enemy_tank_positions[self.spawn_pos_index % 3]
            tank_level = gc.Tank_Criteria[self.spawn_queue[self.spawn_queue_index % len(self.spawn_queue)]]["image"]
            if not self.spawn_queue:
                return
            special_tank = randint(1, len(self.spawn_queue))
            # SpecialTank(self, self.assets, self.groups, position, "Down", "Silver", tank_level)
            if special_tank == self.spawn_queue_index:
                SpecialTank(self, self.assets, self.groups, position, "Down", "Silver", tank_level, behavior)
            else:
                EnemyTank(self, self.assets, self.groups, position, "Down", "Silver", tank_level, behavior)
            # Reset the enemy tank spawn timer
            self.enemy_tank_spawn_timer = pygame.time.get_ticks()
            self.spawn_pos_index += 1
            self.spawn_queue_index += 1
            self.enemies -= 1

            print(f"{behavior} tank has respwaned")

    def stage_transition(self, game_over=False):
        if not self.score_screen.active:
            self.score_screen.timer = pygame.time.get_ticks()
            if self.player_1_active:
                self.score_screen.p1_score = self.player_1_score
                self.score_screen.p1_kill_list = sorted(self.player1.score_list)
            if self.player_2_active:
                self.score_screen.p2_score = self.player_2_score
                self.score_screen.p2_kill_list = sorted(self.player2.score_list)
            self.score_screen.update_basic_info(self.top_score, self.level_num)
        self.score_screen.active = True
        self.score_screen.update(game_over)
    
    def change_level(self, p1_score, p2_score):
        self.level_num += 1
        self.level_num = self.level_num % len(self.data.level_data)
        self.player_1_score = p1_score
        self.player_2_score = p2_score
        self.create_new_stage()
    
    def power_up_fortify(self, start=True, end=False):
        off_x, off_y = gc.SCREEN_BORDER_LEFT, gc.SCREEN_BORDER_TOP
        positions = [
            (off_x + gc.image_size // 2 * 11, off_y + gc.image_size // 2 * 25),
            (off_x + gc.image_size // 2 * 11, off_y + gc.image_size // 2 * 24),
            (off_x + gc.image_size // 2 * 11, off_y + gc.image_size // 2 * 23),
            (off_x + gc.image_size // 2 * 12, off_y + gc.image_size // 2 * 23),
            (off_x + gc.image_size // 2 * 13, off_y + gc.image_size // 2 * 23),
            (off_x + gc.image_size // 2 * 14, off_y + gc.image_size // 2 * 23),
            (off_x + gc.image_size // 2 * 14, off_y + gc.image_size // 2 * 24),
            (off_x + gc.image_size // 2 * 14, off_y + gc.image_size // 2 * 25),
        ]

        if start:
            for pos in positions:
                pos_rect = pygame.rect.Rect(pos[0], pos[1], gc.image_size // 2, gc.image_size // 2)
                for rectangle in self.groups["Impassable_Tiles"]:
                    if rectangle.rect.colliderect(pos_rect):
                        rectangle.kill()
                map_tile = SteelTile(pos, self.groups["Destructable_Tiles"], self.assets.steel_tiles)
                self.groups["Impassable_Tiles"].add(map_tile)
        elif end:
            for pos in positions:
                pos_rect = pygame.rect.Rect(pos[0], pos[1], gc.image_size // 2, gc.image_size // 2)
                for rectangle in self.groups["Impassable_Tiles"]:
                    if rectangle.rect.colliderect(pos_rect):
                        rectangle.kill()
                map_tile = BrickTile(pos, self.groups["Destructable_Tiles"], self.assets.brick_tiles)
                self.groups["Impassable_Tiles"].add(map_tile) 

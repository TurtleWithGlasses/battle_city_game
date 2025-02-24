import pygame
import gameconfig as gc
from characters import Tank, PlayerTank
from game_hud import GameHud
from random import choice, shuffle


class Game:
    def __init__(self, main, assets, player_1=True, player_2=False):
        """The main Game Object when playing"""
        # The main file
        self.main = main
        self.assets = assets

        # Object groups
        self.groups = {"All_Tanks": pygame.sprite.Group(),
                       "Bullets": pygame.sprite.Group()}

        # Player attributes
        self.player_1_active = player_1
        self.player_2_active = player_2

        # Game HUD
        self.hud = GameHud(self, self.assets)

        # Level information
        self.level_num = 1
        self.data = self.main.levels

        # Player objects
        if self.player_1_active:
            self.player1 = PlayerTank(self, self.assets, self.groups, gc.PL1_position, "Up", "Gold", 0)
        if self.player_2_active:
            self.player2 = PlayerTank(self, self.assets, self.groups, gc.PL2_position, "Up", "Green", 1)
        
        # Number of enemy tanks
        self.enemies = gc.STD_ENEMIES

        # Load the stage
        self.create_new_stage()

        # Game over
        self.end_game = False

    
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
                    
                if event.key == pygame.K_RETURN and self.enemies > 0:
                    new_tank = Tank(self, self.assets, self.groups, (400, 400), "Down")
                    self.groups["All_Tanks"].add(new_tank)
                    self.enemies -= 1

    def update(self):
        #Update the hud
        self.hud.update()
        # if self.player_1_active:
        #     self.player1.update()
        # if self.player_2_active:
        #     self.player2.update()
        for dict_key in self.groups.keys():
            for item in self.groups[dict_key]:
                item.update()
    
    def draw(self, window):
        """Drawing to the screen"""
        if self.assets:
            self.hud.draw(window)
            if self.player_1_active:
                self.player1.draw(window)
            if self.player_2_active:
                self.player2.draw(window)
            for dict_key in self.groups.keys():
                for item in self.groups[dict_key]:
                    item.draw(window)
        else:
            print("[ERROR] Game assets are missing!")
    
    def create_new_stage(self):
        # Retreives the specific level data
        self.current_level_data = self.data.level_data[self.level_num-1]

        # Number of enemy tanks to spawn in the stage
        # self.enemies = random.choice([16,17,18,20])
        self.enemies = 5

        # Track the number of enemies killed back down to zero
        self.enemies_killed = self.enemies
        
        # Load in the level data
        self.load_level_data(self.current_level_data)

        # Generating the spawn queue for the computer tanks
        self.generate_spawn_queue()
        self.spawn_pos_index = 0
        self.spawn_queue = 0

        if self.player_1_active:
            self.player1.new_stage_spawn(gc.PL1_position)
    
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
                elif int(tile) == 482:
                    line.append(f"{tile}")
                elif int(tile) == 483:
                    line.append(f"{tile}")
                elif int(tile) == 484:
                    line.append(f"{tile}")
                elif int(tile) == 533:
                    line.append(f"{tile}")
                else:
                    line.append(f"{tile}")
            self.grid.append(line)
        for row in self.grid:
            print(row)
    
    def generate_spawn_queue(self):
        """Generate a list of tanks that will be spawning during the level"""
        self.spawn_queue_ratios = gc.tank_spawn_queue[f"queue_{str((self.level_num-1 % 36) // 3)}"]
        self.spawn_queue = []

        for level, ratio in enumerate(self.spawn_queue_ratios):
            for i in range(int(round(self.enemies * (ratio / 100)))):
                self.spawn_queue.append(f"level_{level}")
        shuffle(self.spawn_queue)

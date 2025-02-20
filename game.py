import pygame
import gameconfig as gc
from characters import Tank, PlayerTank
from game_hud import GameHud


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

        # Player objects
        if self.player_1_active:
            self.player1 = PlayerTank(self, self.assets, self.groups, (200, 200), "Up", "Gold", 0)
        if self.player_2_active:
            self.player2 = PlayerTank(self, self.assets, self.groups, (400, 200), "Up", "Green", 1)
        
        # Number of enemy tanks
        self.enemies = gc.STD_ENEMIES

    
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
                    self.main.run = False
                
                if event.key == pygame.K_SPACE:
                    if self.player_1_active:
                        self.player1.shoot()

                if event.key == pygame.K_RCTRL:
                    if self.player_2_active:
                        self.player2.shoot()
                    
                
                if event.key == pygame.K_RETURN:
                    self.enemies -= 1


    def update(self):
        #Update the hud
        self.hud.update()
        # if self.player_1_active:
        #     self.player1.update()
        # if self.player_2_active:
        #     self.player2.update()
        for dict_key in self.groups.keys():
            self.groups[dict_key].update()
    
    def draw(self, window):
        """Drawing to the screen"""
        if self.assets:
            self.hud.draw(window)
            if self.player_1_active:
                self.player1.draw(window)
            if self.player_2_active:
                self.player2.draw(window)
            for dict_key in self.groups.keys():
                self.groups[dict_key].draw(window)
        else:
            print("[ERROR] Game assets are missing!")

import pygame
import gameconfig as gc
from characters import Tank, PlayerTank


class Game:
    def __init__(self, main, assets):
        """The main Game Object when playing"""
        # The main file
        self.main = main
        self.assets = assets

        # Object groups
        self.groups = {"All_Tanks": pygame.sprite.Group()}

        # Player objects
        self.player1 = PlayerTank(self, self.assets, self.groups, (200, 200), "Up", "Gold", 0)
        self.player2 = PlayerTank(self, self.assets, self.groups, (400, 200), "Up", "Green", 1)
    
    def input(self):
        """Handles inputs for the game when it's running.."""
        keypressed = pygame.key.get_pressed()
        self.player1.input(keypressed)
        self.player2.input(keypressed)

        # pygame event handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.main.run = False
            
            # Keyboard shortcut to quit game
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.main.run = False

    def update(self):
        self.player1.update()
        self.player2.update()
    
    def draw(self, window):
        """Drawing to the screen"""
        if self.assets:
            self.player1.draw(window)
            self.player2.draw(window)
        else:
            print("[ERROR] Game assets are missing!")

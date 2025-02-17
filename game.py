import pygame
import gameconfig as gc


class Game:
    def __init__(self, main, assets):
        """The main Game Object when playing"""
        # The main file
        self.main = main
        self.assets = assets
    
    def input(self):
        """Handles inputs for the game when it's running.."""
        # pygame event handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.main.run = False
            
            # Keyboard shortcut to quit game
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.main.run = False

    def update(self):
        print("The game is being run..")
    
    def draw(self, window):
        """Drawing to the screen"""
        if self.assets:
            pass
        else:
            print("[ERROR] Game assets are missing!")

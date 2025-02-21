import pygame
import gameconfig as gc
from game_assets import GameAssets
from game import Game
from level_editor import LevelEditor


class Main:
    def __init__(self):
        """"Main Game Object"""
        # Initialize pygame module
        pygame.init()
        print("[INFO] Initializing game...")

        self.screen = pygame.display.set_mode((gc.SCREENWIDTH, gc.SCREENHEIGHT))
        pygame.display.set_caption("Battle City Clone")

        self.clock = pygame.time.Clock()
        self.run = True

        self.assets = GameAssets()

        # Game object loading
        self.game_on = False
        self.game = Game(self, self.assets, True, True)

        # Level editor loading 
        self.level_editor_on = True
        self.level_creator = LevelEditor(self, self.assets)

    def run_game(self):
        """Main game while loop"""
        while self.run:
            self.input()
            self.update()
            self.draw()

    def input(self):
        """Input handling for the game"""
        # Event handler while the game is True
        if self.game_on:
            self.game.input()
        
        # Input controls for when level creator is running
        if self.level_editor_on:
            self.level_creator.input()
            
        # Main game controls
        if not self.game_on and not self.level_editor_on:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
    
    def update(self):
        """Update the program and all objects within"""
        self.clock.tick(gc.FPS)

        # If game is running, update game
        if self.game_on:
            self.game.update()
        
        # If level editor is on, update level editor
        if self.level_editor_on:
            self.level_creator.update()

    def draw(self):
        """Handle all of the drawing of the game to the screen"""
        self.screen.fill(gc.BLACK)

        # If game is running, draw game screen
        if self.game_on:
            self.game.draw(self.screen)

        # If level editor is running, draw to screen
        if self.level_editor_on:
            self.level_creator.draw(self.screen)

        pygame.display.update()


if __name__ == "__main__":
    battle_city = Main()
    battle_city.run_game()
    pygame.quit()
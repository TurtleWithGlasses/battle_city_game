import pygame
import gameconfig as gc
from game_assets import GameAssets
from game import Game


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

        self.game_on = True
        self.game = Game(self, self.assets, True, True)

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
            

        # Main game controls
        if not self.game_on:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
    
    def update(self):
        """Update the program and all objects within"""
        self.clock.tick(gc.FPS)

        # If game is running, update game
        if self.game_on:
            self.game.update()

    def draw(self):
        """Handle all of the drawing of the game to the screen"""
        self.screen.fill(gc.BLACK)

        # If game is running, draw game screen
        if self.game_on:
            self.game.draw(self.screen)
        
        pygame.display.update()


if __name__ == "__main__":
    battle_city = Main()
    battle_city.run_game()
    pygame.quit()
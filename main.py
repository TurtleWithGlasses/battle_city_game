import pygame
import gameconfig as gc
from game_assets import GameAssets
from game import Game
from level_editor import LevelEditor
from levels import LevelData
from start_screen import StartScreen


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
        self.levels = LevelData()

        # Game start screen object and check
        self.start_screen = StartScreen(self, self.assets)
        self.start_screen_active = True

        # Game object loading
        self.game_on = False
        self.game = None

        # Level editor loading and check
        self.level_editor_on = False
        self.level_creator = None

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
        
        # Input controls for the start screen
        if self.start_screen_active:
            self.start_screen_active = self.start_screen.input()
        
        # Input controls for when level creator is running
        if self.level_editor_on:
            self.level_creator.input()
            
        # Main game controls
        if not self.game_on and not self.level_editor_on and not self.start_screen_active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
    
    def update(self):
        """Update the program and all objects within"""
        self.clock.tick(gc.FPS)

        # Start screen updating
        if self.start_screen_active:
            self.start_screen.update()

        # If game is running, update game
        if self.game_on:
            self.game.update()
        
        if self.game:
            if self.game.end_game is True:
                self.start_screen = StartScreen(self, self.assets)
                self.start_screen_active = True

                self.game_on = False
                self.game = None
        
        # If level editor is on, update level editor
        if self.level_editor_on:
            self.level_creator.update()
        
        if self.level_creator:
            if self.level_creator.active is False:
                self.start_screen = StartScreen(self, self.assets)
                self.start_screen_active = True

                self.level_editor_on = False
                self.level_creator = None

    def draw(self):
        """Handle all of the drawing of the game to the screen"""
        self.screen.fill(gc.BLACK)

        # If self start screen active, draw the start screen
        if self.start_screen_active:
            self.start_screen.draw(self.screen)

        # If game is running, draw game screen
        if self.game_on:
            self.game.draw(self.screen)

        # If level editor is running, draw to screen
        if self.level_editor_on:
            self.level_creator.draw(self.screen)

        pygame.display.update()
    
    def start_new_game(self, player1, player2):
        """This method starts the game"""
        self.game_on = True
        self.game = Game(self, self.assets, player1, player2)
        self.start_screen_active = False
        return

    def start_level_creator(self):
        self.level_editor_on = True
        self.level_creator = LevelEditor(self, self.assets)
        self.start_screen_active = False


if __name__ == "__main__":
    battle_city = Main()
    battle_city.run_game()
    pygame.quit()
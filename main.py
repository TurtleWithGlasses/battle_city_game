import pygame
import gameconfig as gc


class Main:
    def __init__(self):
        """"Main Game Object"""
        # Initialize pygame module
        pygame.init()

        self.screen = pygame.display.set_mode((gc.SCREENWIDTH, gc.SCREENHEIGHT))
        pygame.display.set_caption("Battle City Clone")

        self.Clock = pygame.time.Clock()
        self.run = True

    def run_game(self):
        """Mainb game while loop"""
        while self.run:
            self.input()
            self.update()
            self.draw()

    def input(self):
        """Input handling for the game"""
        # Main game controls

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False
    
    def update(self):
        """Update the program and all objects within"""
        self.Clock.tick(gc.FPS)

    def draw(self):
        """Handle all of the drawing of the game to the screen"""
        self.screen.fill(gc.BLACK)

        pygame.display.update()


if __name__ == "__main__":
    battle_city = Main()
    battle_city.run_game()
    pygame.quit()
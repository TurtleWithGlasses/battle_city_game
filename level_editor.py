import pygame
import gameconfig as gc


class LevelEditor:
    def __init__(self, main, assets):
        self.main = main
        self.assets = assets
        self.active = True

        self.level_data = None
        self.all_levels = []

        self.overlay_screen = self.draw_screen()
    
    def input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.main.run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.main.run = False
    
    def update(self):
        pass

    def draw(self, window):
        window.blit(self.overlay_screen, (0, 0))

    def draw_screen(self):
        """Create the game screen"""
        overlay_screen = pygame.Surface((gc.SCREENWIDTH, gc.SCREENHEIGHT))
        overlay_screen.fill(gc.GREY)
        pygame.draw.rect(overlay_screen, gc.BLACK, (gc.GAME_SCREEN))
        return overlay_screen
import pygame
import gameconfig as gc


class GameHud:
    def __init__(self, game, assets):
        self.game = game
        self.assets = assets
        self.images = self.assets.hud_images
        self.hud_overlay = self.generate_hud_overlay_screen()
    
    # Generate the base HUD overlay image
    def generate_hud_overlay_screen(self):
        """Generate a fixed hud overlay screen image"""
        overlay_screen = pygame.Surface((gc.SCREENWIDTH, gc.SCREENHEIGHT))
        overlay_screen.fill(gc.GREY)
        pygame.draw.rect(overlay_screen, gc.BLACK, (gc.GAME_SCREEN))
        overlay_screen.blit(self.images["info_panel"], (gc.INFO_PANEL_X, gc.INFO_PANEL_Y))
        overlay_screen.set_colorkey(gc.BLACK)
        return overlay_screen
    
    def update(self):
        pass

    def draw(self, window):
        window.blit(self.hud_overlay, (0, 0))
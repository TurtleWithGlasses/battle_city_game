import pygame
import gameconfig as gc


class ScoreScreen:
    def __init__(self, game, assets):
        self. game = game
        self.assets = assets
        self.white_nums = self.assets.number_black_white
        self.orange_nums = self.assets.number_black_orange
        
        self.active = False
        self.timer = pygame.time.get_ticks()

        self.images = self.assets.score_sheet_images
        self.scoresheet = self.generate_scoresheet_screen()

    def update(self):
        if not pygame.time.get_ticks() - self.timer >= 10000:
            return
        
        self.active = False
    
    def draw(self, window):
        window.fill(gc.BLACK)
        window.blit(self.scoresheet, (0, 0))
    
    def generate_scoresheet_screen(self):
        """Generate a basic template screen for the score card transition"""
        surface = pygame.Surface((gc.SCREENWIDTH, gc.SCREENHEIGHT))
        surface.fill(gc.BLACK)
        new_img = gc.image_size // 2
        surface.blit(self.images["hiScore"], (new_img * 8, new_img * 4))
        surface.blit(self.images["stage"], (new_img * 12, new_img * 6))
        
        arrow_left = self.images["arrow"]
        arrow_right = pygame.transform.flip(arrow_left, True, False)

        if self.game.player_1_active:
            surface.blit(self.images["player1"], (new_img * 3, new_img * 8))
        if self.game.player_2_active:
            surface.blit(self.images["player2"], (new_img * 21, new_img * 8))
        
        surface.blit(self.images["pts"], (new_img * 8, new_img * 12.5))
        surface.blit(arrow_left, (new_img * 14, new_img * 12.5))
        surface.blit(self.assets.tank_images["Tank_4"]["Silver"]["Up"][0], (new_img * 15, new_img * 12.5))

        surface.blit(self.images["total"], (new_img * 6, new_img * 22))
        return surface
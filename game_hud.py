import pygame
import gameconfig as gc


class GameHud:
    def __init__(self, game, assets):
        self.game = game
        self.assets = assets
        self.images = self.assets.hud_images
        self.hud_overlay = self.generate_hud_overlay_screen()

        # Player lives and display
        self.player_1_active = False
        self.player_1_lives = 0
        self.player_1_lives_image = self.display_player_lives(self.player_1_lives, self.player_1_active)

        self.player_2_active = False
        self.player_2_lives = 0
        self.player_2_lives_image = self.display_player_lives(self.player_2_lives, self.player_2_active)
    
    # Generate the base HUD overlay image
    def generate_hud_overlay_screen(self):
        """Generate a fixed hud overlay screen image"""
        overlay_screen = pygame.Surface((gc.SCREENWIDTH, gc.SCREENHEIGHT))
        overlay_screen.fill(gc.GREY)
        pygame.draw.rect(overlay_screen, gc.BLACK, (gc.GAME_SCREEN))
        overlay_screen.blit(self.images["info_panel"], (gc.INFO_PANEL_X, gc.INFO_PANEL_Y))
        overlay_screen.set_colorkey(gc.BLACK)
        return overlay_screen
    
    # Generate player lives image on the HUD
    def display_player_lives(self, playerlives, player_active):
        width, height = gc.image_size, gc.image_size // 2
        surface = pygame.Surface((width, height))
        surface.fill(gc.BLACK)
        if playerlives > 99:
            playerlives = 99
        if not player_active:
            surface.blit(self.images["grey_square"], (0, 0))
            surface.blit(self.images["grey_square"], (gc.image_size // 2, 0))
            return surface

        if playerlives < 10:
            image = pygame.transform.rotate(self.images["life"], 180)
        else:
            num = str(playerlives)[0]
            image = self.images[f"num_{num}"]
        surface.blit(image, (0, 0))
        num = str(playerlives)[-1]
        image_2 = self.images[f"num_{num}"]
        surface.blit(image_2, (gc.image_size // 2, 0))
        return surface
    
    def update(self):
        # Update thenumber of player lives available
        self.player_1_active = self.game.player_1_active
        if self.player_1_active:
            if self.player_1_lives != self.game.player1.lives:
                self.player_1_lives = self.game.player1.lives
                self.player_1_lives_image = self.display_player_lives(self.player_1_lives, self.player_1_active)
        
        self.player_2_active = self.game.player_2_active
        if self.player_2_active:
            if self.player_2_lives != self.game.player2.lives:
                self.player_2_lives = self.game.player2.lives
                self.player_2_lives_image = self.display_player_lives(self.player_2_lives, self.player_2_active)


    def draw(self, window):
        window.blit(self.hud_overlay, (0, 0))
        window.blit(self.player_1_lives_image, (14.5 * gc.image_size, 9.5 * gc.image_size))
        window.blit(self.player_2_lives_image, (14.5 * gc.image_size, 11 * gc.image_size))
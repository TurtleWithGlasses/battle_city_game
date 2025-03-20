import pygame
import random
import gameconfig as gc


class PowerUps(pygame.sprite.Sprite):
    def __init__(self, game, assets, groups):
        super().__init__()
        self.game = game
        self.assets = assets
        self.powerup_images = self.assets.power_up_images

        self.groups = groups
        self.groups["Power_Ups"].add(self)

        self.power_up = self.randomly_select_power_up()
        self.power_up_timer = pygame.time.get_ticks()

        self.x_pos = random.randint(gc.SCREEN_BORDER_LEFT, gc.SCREEN_BORDER_RIGHT - gc.image_size)
        self.y_pos = random.randint(gc.SCREEN_BORDER_TOP, gc.SCREEN_BORDER_BOTTOM - gc.image_size)

        self.image = self.powerup_images[self.power_up]
        self.rect = self.image.get_rect(topleft=(self.x_pos, self.y_pos))

    
    def randomly_select_power_up(self):
        """Randomly select a power up from ability"""
        powerups = list(gc.POWER_UPS.keys())
        selected_powerup = random.choice(powerups)
        return selected_powerup
    
    def power_up_collected(self):
        self.kill()
    
    def update(self):
        if pygame.time.get_ticks() - self.power_up_timer >= 5000:
            self.kill()
        player_tank = pygame.sprite.spritecollideany(self, self.groups["Player_Tanks"])
        if player_tank:
            print(self.power_up)
            self.power_up_collected()
    
    def draw(self, window):
        window.blit(self.image, self.rect)
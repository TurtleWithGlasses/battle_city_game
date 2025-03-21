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

        # self.power_up = self.randomly_select_power_up()
        self.power_up = "extra_life"
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
    
    def shield(self, player):
        """The player tank is protected by a shield for a certain amount of time"""
        player.shield_start = True

    def freeze(self):
        "Freeze all of the currently spawned enemy tanks"
        for tank in self.groups["All_Tanks"]:
            if tank.enemy:
                tank.paralyze_tank(5000)
    
    def explosion(self, player):
        "Destroys all enemy tanks currently spawned"
        for tank in self.groups["All_Tanks"]:
            if tank.enemy:
                score = tank.score
                player.score_list.append(score)
                tank.destroy_tank()

    def extra_life(self, player):
        """Give player an extra life"""
        player.lives += 1
    
    def update(self):
        if pygame.time.get_ticks() - self.power_up_timer >= 5000:
            self.kill()
        player_tank = pygame.sprite.spritecollideany(self, self.groups["Player_Tanks"])
        if player_tank:
            if self.power_up == "shield":
                self.shield(player_tank)
            elif self.power_up == "freeze":
                self.freeze()
            elif self.power_up == "explosion":
                self.explosion(player_tank)
            elif self.power_up == "extra_life":
                self.extra_life(player_tank)
            print(self.power_up)
            self.power_up_collected()
    
    def draw(self, window):
        window.blit(self.image, self.rect)
import pygame

class Explosion(pygame.sprite.Sprite):
    def __init__(self, assets, group, position, explode_type=1):
        super().__init__()
        self.assets = assets
        self.group = group
        self.explosion_group = self.group["Explosion"]
        self.explosion_group.add(self)

        self.position = position
        self.explode_type = explode_type
        self.frame_index = 1
        self.images = self.assets.explosions
        self.image = self.images["explode_1"]
        self.rect = self.image.get_rect(center=self.position)

        self.anim_timer = pygame.time.get_ticks()
    
    def update(self):
        if pygame.time.get_ticks() - self.anim_timer >= 100:
            self.frame_index += 1
            if self.frame_index >= len(self.images):
                self.kill()
            if self.explode_type == 1 and self.frame_index > 3:
                self.kill()
            self.anim_timer = pygame.time.get_ticks()
            self.image = self.images[f"explode_{self.frame_index}"]
            self.rect = self.image.get_rect(center=self.position)
    
    def draw(self, window):
        window.blit(self.image, self.rect)
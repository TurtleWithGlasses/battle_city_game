import pygame
import gameconfig as gc


class Bullet(pygame.sprite.Sprite):
    def __init__(self, groups, owner, position, direction, assets):
        super().__init__()
        self.assets = assets
        self.group = groups
        
        # Groups for collision detection
        self.tanks = self.group["All_Tanks"]
        self.bullet_group = self.group["Bullets"]

        # Bulley position and direction
        self.x_pos, self.y_pos = position
        self.direction = direction

        # Bullet attributes
        self.owner = owner

        # Bullet image
        self.images = self.assets.bullet_images
        self.image = self.images[self.direction]
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))

        # Add bullet to the bullets group
        self.bullet_group.add(self)
    
    def update(self):
        pass

    def draw(self, window):
        # Draw bullet on the screen
        window.blit(self.image, self.rect)
        pygame.draw.rect(window, gc.GREEN, self.rect, 1)
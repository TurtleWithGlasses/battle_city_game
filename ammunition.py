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
        # Bullet movement
        self.move()
        # Check if bullet has reached the edge of the screen
        self.collide_edge_of_screen()

    def draw(self, window):
        # Draw bullet on the screen
        window.blit(self.image, self.rect)
        pygame.draw.rect(window, gc.GREEN, self.rect, 1)
    
    def move(self):
        """Move the bullet in the direction indicated in the init method"""
        speed = gc.TANK_SPEED * 3
        if self.direction == "Up":
            self.y_pos -= speed
        elif self.direction == "Down":
            self.y_pos += speed
        elif self.direction == "Left":
            self.x_pos -= speed
        elif self.direction == "Right":
            self.x_pos += speed
        self.rect.center = (self.x_pos, self.y_pos)
    
    # Collisions
    def collide_edge_of_screen(self):
        """Chech for collision with the screen edge"""
        if self.rect.top <= gc.SCREEN_BORDER_TOP or \
            self.rect.bottom >= gc.SCREEN_BORDER_BOTTOM or \
            self.rect.left <= gc.SCREEN_BORDER_LEFT or \
            self.rect.right >= gc.SCREEN_BORDER_RIGHT:
            self.update_owner()
            self.kill()
    
    def update_owner(self):
        if self.owner.bullet_sum > 0:
            self.owner.bullet_sum -= 1
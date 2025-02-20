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
        # Check for bullet collision with a tank
        self.collide_with_tank()
        # Check for bullet collision
        self.collision_with_bullet()

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
    
    def collide_with_tank(self):
        """Check if the bullet collides with a tank"""
        tank_collisions = pygame.sprite.spritecollide(self, self.tanks, False)
        for tank in tank_collisions:
            if self.owner == tank or tank.spawning == True:
                continue
            # Player owned bullet collides with a player tank
            if self.owner.enemy == False and tank.enemy == False:
                self.update_owner()
                tank.paralyze_tank(gc.TANK_PARALYSIS)
                self.kill()
                break
            # Check for player bullet collision with AI tank or AI bullet with player tank
            if (self.owner.enemy == False and tank.enemy == True) or \
                  (self.owner.enemy == True and tank.enemy == False):
                self.update_owner()
                tank.destroy_tank()
                self.kill()
                break

    def collision_with_bullet(self):
        """Check if bullet collides with another bullet"""
        bullet_hit = pygame.sprite.spritecollide(self, self.bullet_group, False)
        if len(bullet_hit) == 1:
            return 
        for bullet in bullet_hit:
            if bullet == self:
                continue
            bullet.update_owner()
            bullet.kill()
            self.update_owner()
            self.kill()
            break            

    def update_owner(self):
        if self.owner.bullet_sum > 0:
            self.owner.bullet_sum -= 1
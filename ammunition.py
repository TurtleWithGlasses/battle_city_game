import pygame
from explosions import Explosion
import gameconfig as gc


class Bullet(pygame.sprite.Sprite):
    def __init__(self, groups, owner, position, direction, assets):
        super().__init__()
        self.assets = assets
        self.group = groups
        
        # Groups for collision detection
        self.tanks = self.group["All_Tanks"]
        self.bullet_group = self.group["Bullets"]

        # Bullet position and direction
        self.x_pos, self.y_pos = position
        self.direction = direction

        # Bullet attributes
        self.owner = owner
        self.power = self.owner.power
        self.speed = self.owner.bullet_speed

        # Bullet image
        self.images = self.assets.bullet_images
        self.image = self.images[self.direction]
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))

        # Get bullet mask
        self.mask = pygame.mask.from_surface(self.image)
        # self.mask_image = self.mask.to_surface()

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
        # Check for collision with destructable tiles
        self.collision_with_obstacle()
        # Check for collision with the base flag
        self.base_collision()

    def draw(self, window):
        # Draw bullet on the screen
        window.blit(self.image, self.rect)
        # window.blit(self.mask_image, self.rect)
        # pygame.draw.rect(window, gc.GREEN, self.rect, 1)
    
    def move(self):
        """Move the bullet in the direction indicated in the init method"""
        if self.direction == "Up":
            self.y_pos -= self.speed
        elif self.direction == "Down":
            self.y_pos += self.speed
        elif self.direction == "Left":
            self.x_pos -= self.speed
        elif self.direction == "Right":
            self.x_pos += self.speed
        self.rect.center = (self.x_pos, self.y_pos)
    
    # Collisions
    def collide_edge_of_screen(self):
        """Check for collision with the screen edge"""
        if self.rect.top <= gc.SCREEN_BORDER_TOP or \
            self.rect.bottom >= gc.SCREEN_BORDER_BOTTOM or \
            self.rect.left <= gc.SCREEN_BORDER_LEFT or \
            self.rect.right >= gc.SCREEN_BORDER_RIGHT:
            Explosion(self.assets, self.group, self.rect.center, 1)
            self.assets.channel_steel_sound.play(self.assets.steel_sound)
            self.update_owner()
            self.kill()
    
    def collide_with_tank(self):
        """Check if the bullet collides with a tank"""
        tank_collisions = pygame.sprite.spritecollide(self, self.tanks, False)
        for tank in tank_collisions:
            if self.owner == tank or tank.spawning is True:
                continue
            # Player owned bullet collides with a player tank
            if self.owner.enemy is False and tank.enemy is False:
                if pygame.sprite.collide_mask(self, tank):
                    self.update_owner()
                    tank.paralyze_tank(gc.TANK_PARALYSIS)
                    Explosion(self.assets, self.group, self.rect.center, 1)
                    self.kill()
                    break
            # Check for player bullet collision with AI tank or AI bullet with player tank
            if (self.owner.enemy is False and tank.enemy is True) or \
                  (self.owner.enemy is True and tank.enemy is False):
                if pygame.sprite.collide_mask(self, tank):
                    self.update_owner()
                    if not self.owner.enemy:
                        self.owner.score_list.append(gc.Tank_Criteria[tank.level]["score"])
                    tank.destroy_tank()
                    Explosion(self.assets, self.group, self.rect.center, 1)
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
            if pygame.sprite.collide_mask(self, bullet):
                bullet.update_owner()
                bullet.kill()
                self.update_owner()
                self.kill()
                break   

    def collision_with_obstacle(self):
        """Check for bullet collision with any of the tiles"""
        obstacle_collide = pygame.sprite.spritecollide(self, self.group["Destructable_Tiles"], False)
        for obstacle in obstacle_collide:
            if obstacle.name == "Brick":
                self.assets.channel_brick_sound.play(self.assets.brick_sound)
            elif obstacle.name == "Steel":
                self.assets.channel_steel_sound.play(self.assets.steel_sound)
            obstacle.hit_by_bullet(self)
            Explosion(self.assets, self.group, self.rect.center, 1)
        # self.kill()
    
    def base_collision(self):
        """If base is hit by a bullet"""
        if self.rect.colliderect(self.group["Eagle"].sprite.rect):
            Explosion(self.assets, self.group, self.rect.center, 1)
            self.update_owner()
            self.group["Eagle"].sprite.destroy_base()
            self.kill()

    def update_owner(self):
        if self.owner.bullet_num > 0:
            self.owner.bullet_num -= 1
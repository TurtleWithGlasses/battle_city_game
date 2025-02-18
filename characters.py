import pygame
import gameconfig as gc


class Tank(pygame.sprite.Sprite):
    def __init__(self, game, assets, groups, position, direction, color="Silver", tank_level=0):
        super().__init__()
        # Game object and assets
        self.game = game
        self.assets = assets
        self.groups = groups

        # Sprite groups that may interact with tank
        self.tank_group = self.groups["All_Tanks"]

        # Add tank object to the sprite group
        self.tank_group.add(self)

        # Tank images
        self.tank_images = self.assets.tank_images
        self.spawn_images = self.assets.spawn_star_images

        # Tank position and direction
        self.spawn_pos = position
        self.x_pos, self.y_pos = self.spawn_pos
        self.direction = direction

        # Tank spawning
        self.spawning = True
        self.active = False

        # Common tank attributes
        self.tank_level = tank_level
        self.color = color
        self.tank_speed = gc.TANK_SPEED

        # Tank image, rectangle and frame index
        self.frame_index = 0
        self.image = self.tank_images[f"Tank_{self.tank_level}"][self.color][self.direction][self.frame_index]
        self.rect = self.image.get_rect(topleft=(self.spawn_pos))

        # Spawn images
        self.spawn_image = self.spawn_images[f"star_{self.frame_index}"]
        self.spawn_timer = pygame.time.get_ticks() # Overall spawn timer
        self.spawn_animation_timer = pygame.time.get_ticks() # Spawn star animation timer

    def input(self):
        pass

    def update(self):
        # Update the spawn animation
        if self.spawning:
            # Update the spawning star animations if the required amount of time has passed
            if pygame.time.get_ticks() - self.spawn_animation_timer >= 50:
                self.spawn_animation()
            # If total spawn timer seconds passed, change the spawning
            if pygame.time.get_ticks() - self.spawn_timer > 2000:
                self.frame_index = 0
                self.spawning = False
                self.active = True
        
        return

    def draw(self, window):
        # If tank is spawning in, draw the spawn star
        if self.spawning:
            window.blit(self.spawn_image, self.rect)

        # If the tank is set to active, draw to screen
        if self.active:
            window.blit(self.image, self.rect)
            pygame.draw.rect(window, gc.RED, self.rect, 1)
    
    def move_tank(self, direction):
        """Move the tank in the passed direction"""
        if self.spawning:
            return
        
        self.direction = direction

        if direction == "Up":
            self.y_pos -= self.tank_speed
        elif direction == "Down":
            self.y_pos += self.tank_speed
        elif direction == "Left":
            self.x_pos -= self.tank_speed
        elif direction == "Right":
            self.x_pos += self.tank_speed
        
        # Update the tank rectangle position
        self.rect.topleft = (self.x_pos, self.y_pos)
        # Update the Tank Animation
        self.tank_movement_animation()
        # Check for tank collisions with other tanks
        self.tank_on_tank_collision()
    
    # Tank animations
    def tank_movement_animation(self):
        """Update the animation images to simulate tank moving"""
        self.frame_index += 1
        image_listlength = len(self.tank_images[f"Tank_{self.tank_level}"][self.color][self.direction])
        self.frame_index = self.frame_index % image_listlength
        self.image = self.tank_images[f"Tank_{self.tank_level}"][self.color][self.direction][self.frame_index]
    
    def spawn_animation(self):
        """Cycle through the spawn star images to stimulate a spawning icon"""
        self.frame_index += 1
        self.frame_index = self.frame_index % len(self.spawn_images)
        self.spawn_image = self.spawn_images[f"star_{self.frame_index}"]
        self.spawn_animation_timer = pygame.time.get_ticks()

    # Tank collision
    def tank_on_tank_collision(self):
        """Check if the the collides with another tank"""

        tank_collision = pygame.sprite.spritecollide(self, self.tank_group, False)
        if len(tank_collision) == 1:
            return
        
        for tank in tank_collision:
            # Skip tank if it is the current object
            if tank == self:
                continue

            if self.direction == "Right":
                if self.rect.right >= tank.rect.left and \
                    self.rect.bottom > tank.rect.top and self.rect.top < tank.rect.bottom:
                    self.rect.right = tank.rect.left
                    self.x_pos = self.rect.x
            elif self.direction == "Left":
                if self.rect.left <= tank.rect.right and \
                    self.rect.bottom > tank.rect.top and self.rect.top < tank.rect.bottom:
                    self.rect.left = tank.rect.right
                    self.x_pos = self.rect.x
            elif self.direction == "Up":
                if self.rect.top <= tank.rect.bottom and \
                    self.rect.left < tank.rect.right and self.rect.right > tank.rect.left:
                    self.rect.top = tank.rect.bottom
                    self.y_pos = self.rect.y
            elif self.direction == "Down":
                if self.rect.bottom >= tank.rect.top and \
                    self.rect.left < tank.rect.right and self.rect.right > tank.rect.left:
                    self.rect.bottom = tank.rect.top
                    self.y_pos = self.rect.y


class PlayerTank(Tank):
    def __init__(self, game, assets, groups, position, direction, color, tank_level):
        super().__init__(game, assets, groups, position, direction, color, tank_level)
    
    def input(self, keypressed):
        """Move the player tanks"""
        if self.color == "Gold":
            if keypressed[pygame.K_w]:
                self.move_tank("Up")
            elif keypressed[pygame.K_s]:
                self.move_tank("Down")
            elif keypressed[pygame.K_a]:
                self.move_tank("Left")
            elif keypressed[pygame.K_d]:
                self.move_tank("Right")
        
        elif self.color == "Green":
            if keypressed[pygame.K_UP]:
                self.move_tank("Up")
            elif keypressed[pygame.K_DOWN]:
                self.move_tank("Down")
            elif keypressed[pygame.K_LEFT]:
                self.move_tank("Left")
            elif keypressed[pygame.K_RIGHT]:
                self.move_tank("Right")
        

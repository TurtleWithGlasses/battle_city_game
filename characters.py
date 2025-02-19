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

        # Tank position and direction
        self.spawn_pos = position
        self.x_pos, self.y_pos = self.spawn_pos
        self.direction = direction

        # Common tank attributes
        self.active = True
        self.tank_level = tank_level
        self.color = color
        self.tank_speed = gc.TANK_SPEED

        # Tank image, rectangle and frame index
        self.frame_index = 0
        self.image = self.tank_images[f"Tank_{self.tank_level}"][self.color][self.direction][self.frame_index]
        self.rect = self.image.get_rect(topleft=(self.spawn_pos))

    def input(self):
        pass

    def update(self):
        pass

    def draw(self, window):
        # If the tank is set to active, draw to screen
        if self.active:
            window.blit(self.image, self.rect)
    
    def move_tank(self, direction):
        """Move the tank in the passed direction"""
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
    
    # Tank animations
    def tank_movement_animation(self):
        """Update the animation images to simulate tank moving"""
        self.frame_index += 1
        image_listlength = len(self.tank_images[f"Tank_{self.tank_level}"][self.color][self.direction])
        self.frame_index = self.frame_index % image_listlength
        self.image = self.tank_images[f"Tank_{self.tank_level}"][self.color][self.direction][self.frame_index]

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
        
